import { afterEach, describe, expect, it, vi } from 'vitest';

import { submitProposal } from './proposals';
import type { ProposalPayload } from './proposeForm';

const payload: ProposalPayload = { text: 'A useful quote', section: 'wisdom', lang: 'en' };

afterEach(() => vi.restoreAllMocks());

describe('submitProposal', () => {
  it('sends exactly the given payload to the real endpoint path', async () => {
    const fetchMock = vi.spyOn(global, 'fetch').mockResolvedValue(new Response(JSON.stringify({ id: 'p-1' }), { status: 201 }));
    await submitProposal(payload);
    const [url, init] = fetchMock.mock.calls[0];
    expect(String(url)).toMatch(/\/api\/v1\/proposals$/);
    expect(init?.method).toBe('POST');
    expect(JSON.parse(init?.body as string)).toEqual(payload);
  });

  it('201 -> ok with the returned id', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue(new Response(JSON.stringify({ id: 'p-1' }), { status: 201 }));
    await expect(submitProposal(payload)).resolves.toEqual({ ok: true, id: 'p-1' });
  });

  it('401 -> unauthenticated', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue(new Response(null, { status: 401 }));
    await expect(submitProposal(payload)).resolves.toEqual({ ok: false, reason: 'unauthenticated' });
  });

  it('422 -> validation', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue(new Response(null, { status: 422 }));
    await expect(submitProposal(payload)).resolves.toEqual({ ok: false, reason: 'validation' });
  });

  it('400 -> validation (same bucket as 422, per this task\'s own brief)', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue(new Response(null, { status: 400 }));
    await expect(submitProposal(payload)).resolves.toEqual({ ok: false, reason: 'validation' });
  });

  it('404 -> not-found (the real endpoint not merged into main yet)', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue(new Response(null, { status: 404 }));
    await expect(submitProposal(payload)).resolves.toEqual({ ok: false, reason: 'not-found' });
  });

  it('500 -> server', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue(new Response(null, { status: 500 }));
    await expect(submitProposal(payload)).resolves.toEqual({ ok: false, reason: 'server' });
  });

  it('a rejected fetch (network down) -> network, never throws', async () => {
    vi.spyOn(global, 'fetch').mockRejectedValue(new Error('network down'));
    await expect(submitProposal(payload)).resolves.toEqual({ ok: false, reason: 'network' });
  });
});
