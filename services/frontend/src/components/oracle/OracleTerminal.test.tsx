// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import React from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import OracleTerminal from './OracleTerminal';
import type { OfflineLogEntry } from '../../types/domain';

const queueMocks = vi.hoisted(() => ({
  enqueueErrorReport: vi.fn(async () => undefined),
  enqueueOracleQuery: vi.fn(async () => undefined),
  listUnsyncedEntries: vi.fn(async (): Promise<import('../../types/domain').OfflineLogEntry[]> => []),
  markEntrySynced: vi.fn(async () => undefined),
}));

vi.mock('../../lib/db', () => queueMocks);
vi.mock('framer-motion', async () => {
  const React = await import('react');
  const component = React.forwardRef<HTMLElement, React.PropsWithChildren<Record<string, unknown>>>((props, ref) => {
    const { children, initial: _initial, animate: _animate, exit: _exit, transition: _transition, ...rest } = props;
    return React.createElement('div', { ...rest, ref }, children as React.ReactNode);
  });
  return { AnimatePresence: ({ children }: { children: React.ReactNode }) => children, motion: { div: component, article: component }, useReducedMotion: () => true };
});

function sseResponse(chunks: unknown[]): Response {
  return new Response(chunks.map((chunk) => `data: ${JSON.stringify(chunk)}\n\n`).join(''), {
    status: 200, headers: { 'Content-Type': 'text/event-stream' },
  });
}

describe('OracleTerminal governance and URL context', () => {
  afterEach(() => cleanup());
  beforeEach(() => {
    vi.clearAllMocks();
    window.history.replaceState({}, '', '/en/oracle?tag=simplicity');
  });

  it('discloses creative mode, reads tag at submission, and proposes only after an explicit click', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(sseResponse([{
        mode: 'creative', text: 'A new reflection.', themes: ['wisdom'], tags: ['simplicity'],
      }]))
      .mockResolvedValueOnce(new Response(JSON.stringify({ status: 'proposed' }), { status: 201 }));
    vi.stubGlobal('fetch', fetchMock);
    render(<OracleTerminal locale="en" />);

    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'How should I simplify?' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));

    expect(await screen.findByText('Oracular voice — no strong TTOD match')).toBeVisible();
    expect(screen.getByText(/Thematic anchors/)).toBeVisible();
    expect(screen.getByText('wisdom')).toBeVisible();
    expect(screen.queryByLabelText('Grounded in the TTOD corpus')).not.toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toMatchObject({
      contextTag: 'simplicity', locale: 'en',
    });

    fireEvent.click(screen.getByRole('button', { name: 'Save as a draft proposal' }));
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(JSON.parse(fetchMock.mock.calls[1][1].body)).toEqual({
      query: 'How should I simplify?',
      creativeAnswer: 'A new reflection.',
      locale: 'en',
      suggestedTags: ['simplicity'],
      suggestedSection: 'wisdom',
    });
    expect(await screen.findByText(/Saved as a draft proposal/)).toHaveTextContent('acceptance path is not yet operational');
  });

  it('renders grounded citations without exposing the proposal action', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(sseResponse([
      { mode: 'grounded', citedQuoteIds: ['wis-001'], text: 'Grounded answer.', themes: ['wisdom'], tags: ['simplicity'] },
    ])));
    render(<OracleTerminal locale="en" />);
    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'A grounded question' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));
    expect(await screen.findByText('Grounded in the TTOD corpus')).toBeVisible();
    expect(screen.getByRole('link', { name: 'View quote wis-001' })).toHaveAttribute('href', '/en/wisdom/wis-001');
    expect(screen.queryByRole('button', { name: /draft proposal/ })).not.toBeInTheDocument();
  });

  it('queues an unreachable query instead of using an alternate inference path', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('network unavailable')));
    render(<OracleTerminal locale="en" />);
    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'Queue this' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));
    expect(await screen.findByText(/safely queued on this device/)).toBeVisible();
    expect(queueMocks.enqueueOracleQuery).toHaveBeenCalledWith(expect.objectContaining({
      query: 'Queue this', contextTag: 'simplicity', sessionHistory: [], locale: 'en',
    }));
  });

  it('keeps previous exchanges and sends them as sessionHistory', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(sseResponse([{ mode: 'creative', text: 'Diversify your portfolio to reduce risk.' }]))
      .mockResolvedValueOnce(sseResponse([{ mode: 'creative', text: 'Build an emergency fund before investing.' }]));
    vi.stubGlobal('fetch', fetchMock);
    render(<OracleTerminal locale="en" />);

    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'How should I invest my savings?' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));
    expect(await screen.findByText('Diversify your portfolio to reduce risk.')).toBeVisible();

    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'What should I do before investing?' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));
    expect(await screen.findByText('Build an emergency fund before investing.')).toBeVisible();
    expect(screen.getByText('Diversify your portfolio to reduce risk.')).toBeVisible();
    // Brief §5: each exchange carries its own heading, so a screen reader can tell turns apart.
    expect(screen.getAllByRole('heading', { level: 2 }).map((heading) => heading.textContent))
      .toEqual(['Exchange 1', 'Exchange 2']);

    const secondBody = JSON.parse(fetchMock.mock.calls[1][1].body);
    expect(secondBody.sessionHistory).toEqual(['Human: How should I invest my savings?', 'Oracle: Diversify your portfolio to reduce risk.']);
  });
});

describe('OracleTerminal streamed rendering (Task 1)', () => {
  afterEach(() => cleanup());
  beforeEach(() => vi.clearAllMocks());

  it('paints each chunk as it arrives and blocks a second submit mid-stream', async () => {
    const encoder = new TextEncoder();
    let controller!: ReadableStreamDefaultController<Uint8Array>;
    const body = new ReadableStream<Uint8Array>({ start: (c) => { controller = c; } });
    const send = (chunk: unknown) => controller.enqueue(encoder.encode(`data: ${JSON.stringify(chunk)}\n\n`));
    const fetchMock = vi.fn().mockResolvedValue(new Response(body, {
      status: 200, headers: { 'Content-Type': 'text/event-stream' },
    }));
    vi.stubGlobal('fetch', fetchMock);
    render(<OracleTerminal locale="en" />);
    const input = screen.getByPlaceholderText(/practice question/);
    const ask = screen.getByRole('button', { name: 'Ask' });

    fireEvent.change(input, { target: { value: 'First question' } });
    fireEvent.click(ask);
    send({ mode: 'grounded', citedQuoteIds: ['wis-001'], text: 'Water ' });
    expect(await screen.findByText('Water')).toBeVisible();
    expect(screen.getByText('Listening…')).toBeVisible();
    // Incremental paint: the first chunk is on screen while the second has not been sent yet.
    expect(screen.queryByText(/finds its way/)).not.toBeInTheDocument();

    fireEvent.change(input, { target: { value: 'Second question' } });
    expect(ask).toBeDisabled();
    fireEvent.keyDown(input, { key: 'Enter', ctrlKey: true });
    fireEvent.submit(input.closest('form')!);
    expect(fetchMock).toHaveBeenCalledTimes(1);

    send({ mode: 'grounded', citedQuoteIds: ['wis-001'], text: 'finds its way.' });
    expect(await screen.findByText((_, element) => element?.tagName === 'P' && element.textContent === 'Water finds its way.')).toBeVisible();
    controller.close();
    await waitFor(() => expect(screen.queryByText('Listening…')).not.toBeInTheDocument());
    expect(ask).toBeEnabled();
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });
});

describe('OracleTerminal live-region announcement (Task 2)', () => {
  afterEach(() => cleanup());
  beforeEach(() => vi.clearAllMocks());

  it('grows the answer live region chunk by chunk and clears aria-busy when the stream closes', async () => {
    const encoder = new TextEncoder();
    let controller!: ReadableStreamDefaultController<Uint8Array>;
    const body = new ReadableStream<Uint8Array>({ start: (c) => { controller = c; } });
    const send = (chunk: unknown) => controller.enqueue(encoder.encode(`data: ${JSON.stringify(chunk)}\n\n`));
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(body, {
      status: 200, headers: { 'Content-Type': 'text/event-stream' },
    })));
    const { container } = render(<OracleTerminal locale="en" />);
    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'Speak slowly' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));

    const liveRegions = () => container.querySelectorAll('[aria-live]');
    await waitFor(() => expect(liveRegions()).toHaveLength(1));
    const answer = liveRegions()[0];
    expect(answer).toHaveAttribute('aria-live', 'polite');
    expect(answer).toHaveAttribute('aria-atomic', 'false');
    expect(answer).toHaveAttribute('aria-busy', 'true');
    expect(answer).not.toHaveTextContent('Speak slowly');
    expect(answer).not.toHaveTextContent('Listening…');

    send({ mode: 'creative', text: 'The river ' });
    await waitFor(() => expect(answer).toHaveTextContent('The river'));
    expect(answer).not.toHaveTextContent('bends.');
    expect(answer).toHaveAttribute('aria-busy', 'true');

    send({ mode: 'creative', text: 'bends.' });
    await waitFor(() => expect(answer).toHaveTextContent('The river bends.'));
    // Each chunk is its own node, so with aria-atomic="false" only the new words are announced.
    expect([...answer.querySelectorAll('p > span')].map((span) => span.textContent)).toEqual(['The river ', 'bends.']);
    controller.close();
    await waitFor(() => expect(answer).toHaveAttribute('aria-busy', 'false'));
    expect(liveRegions()).toHaveLength(1);
  });
});

describe('OracleTerminal grounded vs. creative disclosure (Task 3)', () => {
  afterEach(() => cleanup());
  beforeEach(() => vi.clearAllMocks());

  it('names each segment by its mode in text and links grounded citations to their quote pages', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(sseResponse([
      { mode: 'grounded', citedQuoteIds: ['wis-001', 'arch-038'], text: 'From the corpus.' },
      { mode: 'creative', citedQuoteIds: ['wis-999'], text: 'From the oracle.' },
    ])));
    render(<OracleTerminal locale="es" />);
    fireEvent.change(screen.getByPlaceholderText(/pregunta de práctica/), { target: { value: 'Mixed answer' } });
    fireEvent.click(screen.getByRole('button', { name: 'Preguntar' }));

    const grounded = await screen.findByRole('group', { name: 'Fundamentado en el corpus TTOD' });
    const creative = screen.getByRole('group', { name: 'Voz oracular — sin coincidencia fuerte en TTOD' });
    expect(grounded).toHaveTextContent('From the corpus.');
    expect(creative).toHaveTextContent('From the oracle.');

    const citations = within(grounded).getByRole('list', { name: 'Citas' });
    expect(within(citations).getByRole('link', { name: 'Ver cita wis-001' })).toHaveAttribute('href', '/es/wisdom/wis-001');
    expect(within(citations).getByRole('link', { name: 'Ver cita arch-038' })).toHaveAttribute('href', '/es/wisdom/arch-038');
    expect(within(creative).queryByRole('link')).not.toBeInTheDocument();
  });
});

describe('OracleTerminal cold-start preparing state (Task 5)', () => {
  afterEach(() => cleanup());
  beforeEach(() => vi.clearAllMocks());

  it('shows a preparing status before the first chunk, then switches to streaming', async () => {
    const encoder = new TextEncoder();
    let controller!: ReadableStreamDefaultController<Uint8Array>;
    const body = new ReadableStream<Uint8Array>({ start: (c) => { controller = c; } });
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(body, {
      status: 200, headers: { 'Content-Type': 'text/event-stream' },
    })));
    render(<OracleTerminal locale="en" />);
    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'Cold start' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));

    // Brief §5: the "preparing" element itself must be the live region — asserting the text alone
    // would still pass if the role went missing. `role="status"` implies aria-live="polite".
    const preparing = await screen.findByRole('status');
    expect(preparing).toHaveTextContent('Gathering wisdom…');
    expect(preparing).toBeVisible();
    expect(screen.queryByText('Listening…')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Ask' })).toBeDisabled();

    controller.enqueue(encoder.encode(`data: ${JSON.stringify({ mode: 'creative', text: 'Awake.' })}\n\n`));
    await waitFor(() => expect(screen.queryByText('Gathering wisdom…')).not.toBeInTheDocument());
    expect(screen.getByText('Listening…')).toBeVisible();
    controller.close();
  });

  it('does not show the preparing status when the request fails immediately', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('network unavailable')));
    render(<OracleTerminal locale="en" />);
    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'Fails fast' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));

    expect(await screen.findByText(/safely queued on this device/)).toBeVisible();
    expect(screen.queryByText('Gathering wisdom…')).not.toBeInTheDocument();
  });

  // Brief §3.5: a browser that already knows it is offline never starts a request, so the
  // preparing status must not render even once. The first check runs synchronously after the click.
  it('queues without ever rendering the preparing status when the browser is already offline', async () => {
    const onLine = vi.spyOn(navigator, 'onLine', 'get').mockReturnValue(false);
    const fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    try {
      render(<OracleTerminal locale="en" />);
      fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'Already offline' } });
      fireEvent.click(screen.getByRole('button', { name: 'Ask' }));

      expect(screen.queryByText('Gathering wisdom…')).not.toBeInTheDocument();
      expect(await screen.findByText(/safely queued on this device/)).toBeVisible();
      expect(screen.queryByText('Gathering wisdom…')).not.toBeInTheDocument();
      expect(fetchMock).not.toHaveBeenCalled();
      expect(queueMocks.enqueueOracleQuery).toHaveBeenCalledWith(expect.objectContaining({ query: 'Already offline' }));
    } finally {
      onLine.mockRestore();
    }
  });
});

describe('OracleTerminal recovery/error state (Task 6)', () => {
  afterEach(() => cleanup());
  beforeEach(() => vi.clearAllMocks());

  it('announces a hard failure as an alert with a retry action, and retry resends the query', async () => {
    queueMocks.listUnsyncedEntries.mockResolvedValueOnce([
      {
        id: 'queued-1', timestamp: new Date().toISOString(), kind: 'oracle-query', synced: false,
        payload: { query: 'Still down?', sessionHistory: [], locale: 'en' },
      } satisfies OfflineLogEntry,
    ]);
    const fetchMock = vi.fn()
      .mockRejectedValueOnce(new TypeError('still down'))
      .mockResolvedValueOnce(sseResponse([{ mode: 'creative', text: 'Back online.' }]));
    vi.stubGlobal('fetch', fetchMock);
    render(<OracleTerminal locale="en" />);

    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('A queued query could not be retried yet.');
    const retryButton = screen.getByRole('button', { name: 'Retry' });

    fireEvent.click(retryButton);
    expect(await screen.findByText('Back online.')).toBeVisible();
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(JSON.parse(fetchMock.mock.calls[1][1].body)).toMatchObject({ query: 'Still down?' });
  });

  // Brief §5: "mock `fetch` to return a 5xx error and assert that the 'Unavailable' UI is rendered".
  it('renders the unavailable state — not the offline queue — when the Oracle answers 5xx', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('{"detail":"boom"}', { status: 503 })));
    render(<OracleTerminal locale="en" />);
    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'Server broken?' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));

    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('The Oracle is currently unavailable. Please try again.');
    // No raw status code and no internal error string may reach the user.
    expect(screen.queryByText(/503/)).not.toBeInTheDocument();
    expect(screen.queryByText(/Oracle stream failed/)).not.toBeInTheDocument();
    // A 5xx is a live server that answered, so the query must NOT be parked in the offline queue.
    expect(queueMocks.enqueueOracleQuery).not.toHaveBeenCalled();
    expect(screen.getByRole('button', { name: 'Retry' })).toBeEnabled();
  });

  it('recovers through Retry once the Oracle is back', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(new Response('boom', { status: 500 }))
      .mockResolvedValueOnce(sseResponse([{ mode: 'creative', text: 'Back online.' }]));
    vi.stubGlobal('fetch', fetchMock);
    render(<OracleTerminal locale="en" />);
    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'Are you back?' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));

    fireEvent.click(await screen.findByRole('button', { name: 'Retry' }));
    expect(await screen.findByText('Back online.')).toBeVisible();
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });

  // Retry meets the Task 5 offline shortcut: with the browser offline the failed card itself turns
  // into the queued notice. No second card, no new request, and the alert and its button are gone.
  it('queues the query in the same card when Retry is pressed while the browser is offline', async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce(new Response('boom', { status: 500 }));
    vi.stubGlobal('fetch', fetchMock);
    render(<OracleTerminal locale="en" />);
    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'Offline retry?' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));
    const retryButton = await screen.findByRole('button', { name: 'Retry' });

    const onLine = vi.spyOn(navigator, 'onLine', 'get').mockReturnValue(false);
    try {
      fireEvent.click(retryButton);
      expect(await screen.findByText(/safely queued on this device/)).toBeVisible();
      expect(screen.queryByRole('alert')).not.toBeInTheDocument();
      expect(screen.queryByRole('button', { name: 'Retry' })).not.toBeInTheDocument();
      expect(screen.getAllByRole('heading', { level: 2 })).toHaveLength(1);
      expect(fetchMock).toHaveBeenCalledTimes(1);
      expect(queueMocks.enqueueOracleQuery).toHaveBeenCalledWith(expect.objectContaining({ query: 'Offline retry?' }));
    } finally {
      onLine.mockRestore();
    }
  });
});

describe('OracleTerminal test coverage (Task 7)', () => {
  afterEach(() => cleanup());
  beforeEach(() => vi.clearAllMocks());

  // The 5xx case belongs to Task 6's own brief (§5). What Task 7 adds is the *other* rejected
  // status: a 4xx used to surface the raw `Oracle stream failed (400)` string in the DOM.
  it('turns a rejected request into a human-readable notice, never a raw status code, and stays usable', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('{"detail":"no"}', { status: 400 })));
    render(<OracleTerminal locale="en" />);
    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'Bad request?' } });
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }));

    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('The Oracle could not complete this answer. Please try again.');
    // Neither the status code nor the internal error string may reach the DOM.
    expect(screen.queryByText(/Oracle stream failed/)).not.toBeInTheDocument();
    expect(screen.queryByText(/400/)).not.toBeInTheDocument();
    // A rejected request is not an offline situation: nothing is parked in the queue.
    expect(queueMocks.enqueueOracleQuery).not.toHaveBeenCalled();
    // The terminal is not stuck in `busy`: a new question re-enables the Ask button
    // (it is otherwise disabled only because submitting cleared the textarea).
    fireEvent.change(screen.getByPlaceholderText(/practice question/), { target: { value: 'Again?' } });
    await waitFor(() => expect(screen.getByRole('button', { name: 'Ask' })).not.toBeDisabled());
  });
});
