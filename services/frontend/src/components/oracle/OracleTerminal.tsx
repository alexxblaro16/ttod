import { AnimatePresence, motion, useReducedMotion } from 'framer-motion';
import React from 'react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

import type {
  OfflineLogEntry,
  OracleProposeRequest,
  OracleQueryPayload,
  OracleResponseChunk,
} from '../../types/domain';
import {
  enqueueErrorReport,
  enqueueOracleQuery,
  listUnsyncedEntries,
  markEntrySynced,
} from '../../lib/db';
import { readOracleStream } from './sse';
import './oracle-terminal.css';

type Locale = 'en' | 'es';
// `parts` keeps each chunk as its own text node so the live region announces only the new words (Task 2).
type StreamSegment = OracleResponseChunk & { key: string; parts: string[] };

interface Exchange {
  id: string;
  query: string;
  contextTag?: string;
  segments: StreamSegment[];
  state: 'preparing' | 'streaming' | 'complete' | 'queued' | 'error';
  notice?: string;
  proposalState?: 'saving' | 'saved' | 'error';
  payload: OracleQueryPayload;
}

interface Props {
  locale: Locale;
}

function sameList(left?: string[], right?: string[]): boolean {
  return (left ?? []).join('\u0000') === (right ?? []).join('\u0000');
}

export function appendChunk(segments: StreamSegment[], chunk: OracleResponseChunk): StreamSegment[] {
  const previous = segments.at(-1);
  if (
    previous &&
    previous.mode === chunk.mode &&
    sameList(previous.citedQuoteIds, chunk.citedQuoteIds) &&
    sameList(previous.themes, chunk.themes) &&
    sameList(previous.tags, chunk.tags)
  ) {
    return [...segments.slice(0, -1), {
      ...previous, text: previous.text + chunk.text, parts: [...previous.parts, chunk.text],
    }];
  }
  return [...segments, { ...chunk, key: identifier(), parts: [chunk.text] }];
}

const COPY = {
  en: {
    eyebrow: 'Local oracle', title: 'Ask the Tao', open: 'Open oracle', close: 'Close oracle',
    placeholder: 'Bring a practice question — the Oracle answers with wisdom, not fixes…', submit: 'Ask', streaming: 'Listening…',
    preparing: 'Gathering wisdom…',
    grounded: 'Grounded in the TTOD corpus', creative: 'Oracular voice — no strong TTOD match',
    themes: 'Thematic anchors', tags: 'Nearby tags',
    queued: 'The oracle is unreachable. Your query is safely queued on this device.',
    queueError: 'The oracle is unreachable and this browser could not open its offline queue.',
    unavailable: 'The Oracle is currently unavailable. Please try again.',
    answerFailed: 'The Oracle could not complete this answer. Please try again.',
    syncing: 'Retrying queued queries…', propose: 'Save as a draft proposal', proposing: 'Saving draft…',
    proposed: 'Saved as a draft proposal. The current human acceptance path is not yet operational.',
    proposalError: 'The draft proposal could not be saved.', retryError: 'A queued query could not be retried yet.',
    retry: 'Retry',
    context: 'Context tag', hint: 'Alt+Shift+O opens · Ctrl/⌘+Enter asks · Esc closes',
    citations: 'Cited quotes', viewQuote: 'View quote', exchange: 'Exchange',
  },
  es: {
    eyebrow: 'Oráculo local', title: 'Pregunta al Tao', open: 'Abrir oráculo', close: 'Cerrar oráculo',
    placeholder: 'Trae una pregunta de práctica — el Oráculo responde con sabiduría, no con parches…', submit: 'Preguntar', streaming: 'Escuchando…',
    preparing: 'Reuniendo sabiduría…',
    grounded: 'Fundamentado en el corpus TTOD', creative: 'Voz oracular — sin coincidencia fuerte en TTOD',
    themes: 'Anclas temáticas', tags: 'Etiquetas cercanas',
    queued: 'El oráculo no está disponible. Tu consulta queda guardada en este dispositivo.',
    queueError: 'El oráculo no está disponible y el navegador no pudo abrir la cola sin conexión.',
    unavailable: 'El Oráculo no está disponible en este momento. Inténtalo de nuevo.',
    answerFailed: 'El Oráculo no pudo completar esta respuesta. Inténtalo de nuevo.',
    syncing: 'Reintentando consultas guardadas…', propose: 'Guardar como borrador de propuesta', proposing: 'Guardando borrador…',
    proposed: 'Guardada como borrador de propuesta. La vía actual de aceptación humana aún no está operativa.',
    proposalError: 'No se pudo guardar el borrador.', retryError: 'Todavía no se pudo reintentar una consulta guardada.',
    retry: 'Reintentar',
    context: 'Etiqueta de contexto', hint: 'Alt+Mayús+O abre · Ctrl/⌘+Intro pregunta · Esc cierra',
    citations: 'Citas', viewQuote: 'Ver cita', exchange: 'Intercambio',
  },
} as const;

type Copy = (typeof COPY)[Locale];

// Task 3: the mode is disclosed by text plus a distinct glyph, never by color alone. The glyph is
// aria-hidden so screen readers hear only the label, which also names the segment (aria-labelledby).
const MODE_GLYPH = { grounded: '◆', creative: '✦' } as const;

function ModeLabel({ id, mode, copy }: { id: string; mode: OracleResponseChunk['mode']; copy: Copy }) {
  return (
    <strong id={id} className="oracle-mode">
      <span aria-hidden="true">{MODE_GLYPH[mode]} </span>
      {mode === 'grounded' ? copy.grounded : copy.creative}
    </strong>
  );
}

function CitationLinks({ ids, locale, copy }: { ids: string[]; locale: Locale; copy: Copy }) {
  return (
    <ul className="oracle-citations" aria-label={copy.citations}>
      {ids.map((id) => (
        <li key={id}><a href={`/${locale}/wisdom/${id}`} aria-label={`${copy.viewQuote} ${id}`}>{id}</a></li>
      ))}
    </ul>
  );
}

const identifier = () => globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random()}`;

class UnreachableOracleError extends Error {}

function currentContextTag(): string | undefined {
  if (typeof window === 'undefined') return undefined;
  const value = new URL(window.location.href).searchParams.get('tag')?.trim();
  return value || undefined;
}

function historyFrom(exchanges: Exchange[]): string[] {
  return exchanges
    .filter((exchange) => exchange.state === 'complete')
    .flatMap((exchange) => [
      `Human: ${exchange.query}`,
      `Oracle: ${exchange.segments.map((segment) => segment.text).join('')}`,
    ])
    .slice(-50);
}

export default function OracleTerminal({ locale }: Props) {
  const copy = COPY[locale];
  const reduceMotion = useReducedMotion();
  const [open, setOpen] = useState(true);
  const [query, setQuery] = useState('');
  const [exchanges, setExchanges] = useState<Exchange[]>([]);
  const [syncing, setSyncing] = useState(false);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const exchangesRef = useRef(exchanges);
  const syncingRef = useRef(false);
  const submittingRef = useRef(false);
  exchangesRef.current = exchanges;

  const updateExchange = useCallback((id: string, update: (exchange: Exchange) => Exchange) => {
    setExchanges((current) => current.map((exchange) => exchange.id === id ? update(exchange) : exchange));
  }, []);

  const sendPayload = useCallback(async (
    payload: OracleQueryPayload,
    queuedEntry?: OfflineLogEntry,
    retryOf?: string,
  ) => {
    const id = retryOf ?? identifier();
    // Task 5 §3.5: a browser that already knows it is offline fails before any request exists, so
    // the query goes straight to the offline queue and the exchange never enters `preparing`.
    // `navigator.onLine === true` proves nothing, so every other failure still surfaces after the attempt.
    if (!queuedEntry && typeof navigator !== 'undefined' && !navigator.onLine) {
      const queued = await enqueueOracleQuery(payload).then(() => true, () => false);
      const settled = { state: queued ? 'queued' : 'error', notice: queued ? copy.queued : copy.queueError } as const;
      if (retryOf) {
        updateExchange(retryOf, (exchange) => ({ ...exchange, segments: [], proposalState: undefined, ...settled }));
      } else {
        setExchanges((current) => [...current, {
          id, query: payload.query, contextTag: payload.contextTag, segments: [], payload, ...settled,
        }]);
      }
      return false;
    }
    // `preparing` covers the gap between the request firing and the first chunk arriving
    // (cold start or plain network latency) so the terminal never looks frozen (Task 5).
    if (retryOf) {
      // Task 6: Retry re-runs the *same* exchange, so the failed card does not linger next to its
      // own replacement with a still-clickable button. The state machine stays idle → preparing →
      // streaming → complete | error, one card per question.
      updateExchange(retryOf, (exchange) => ({
        ...exchange, segments: [], state: 'preparing', notice: undefined, proposalState: undefined,
      }));
    } else {
      setExchanges((current) => [...current, {
        id, query: payload.query, contextTag: payload.contextTag, segments: [], state: 'preparing', payload,
      }]);
    }
    let received = 0;
    try {
      const response = await fetch('/api/v1/oracle/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const message = `Oracle stream failed (${response.status})`;
        if (response.status >= 500) throw new UnreachableOracleError(message);
        throw new Error(message);
      }
      // One state update per chunk, never buffering the whole answer before first paint.
      // React 18+ auto-batches updates from the same task, so chunks that arrive in one
      // network read commit in a single render (no layout thrashing), while each new read
      // paints on the next frame. The functional updater keeps concurrent chunks ordered.
      received = await readOracleStream(response, (chunk) => {
        updateExchange(id, (exchange) => ({
          ...exchange,
          state: 'streaming',
          segments: appendChunk(exchange.segments, chunk),
        }));
      });
      if (received === 0) throw new Error('Oracle stream completed without an answer');
      updateExchange(id, (exchange) => ({ ...exchange, state: 'complete' }));
      if (queuedEntry) await markEntrySynced(queuedEntry);
      return true;
    } catch (error) {
      // Two failures that look similar and are not, so they get different UI (Task 6, brief §3):
      // - `TypeError` = the connection is gone. The offline queue owns that case (PWA module): the
      //   query is preserved and replayed on reconnect, so a Retry button would only fail again.
      // - `UnreachableOracleError` = the server answered 5xx. That is the brief's "actually broken"
      //   case: an alert plus a manual Retry, and never a query parked in the offline queue.
      const offline = error instanceof TypeError;
      const serverBroken = error instanceof UnreachableOracleError;
      if (received === 0 && !queuedEntry && offline) {
        try {
          await enqueueOracleQuery(payload);
          updateExchange(id, (exchange) => ({ ...exchange, state: 'queued', notice: copy.queued }));
        } catch {
          updateExchange(id, (exchange) => ({ ...exchange, state: 'error', notice: copy.queueError }));
        }
      } else {
        // The diagnostic detail (status code included) goes to the error report, never to the UI:
        // the brief's success criterion is that a user never reads an HTTP status or a stack trace.
        const detail = error instanceof Error ? error.message : String(error);
        await enqueueErrorReport(detail).catch(() => undefined);
        const notice = serverBroken ? copy.unavailable : queuedEntry ? copy.retryError : copy.answerFailed;
        updateExchange(id, (exchange) => ({ ...exchange, state: 'error', notice }));
      }
      return false;
    }
  }, [copy.answerFailed, copy.queueError, copy.queued, copy.retryError, copy.unavailable, updateExchange]);

  const flushQueue = useCallback(async () => {
    if (syncingRef.current || typeof navigator === 'undefined' || !navigator.onLine) return;
    syncingRef.current = true;
    setSyncing(true);
    try {
      const entries = await listUnsyncedEntries();
      for (const entry of entries) {
        if (entry.kind === 'oracle-query') {
          const succeeded = await sendPayload(entry.payload as OracleQueryPayload, entry);
          if (!succeeded) break;
        }
      }
    } catch {
      // A private-mode/browser IndexedDB failure must not break the terminal or online requests.
    } finally {
      syncingRef.current = false;
      setSyncing(false);
    }
  }, [sendPayload]);

  useEffect(() => {
    const onOnline = () => void flushQueue();
    window.addEventListener('online', onOnline);
    if (navigator.onLine) void flushQueue();
    return () => window.removeEventListener('online', onOnline);
  }, []); // The online listener deliberately binds once; flushQueue reads the durable queue.

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.altKey && event.shiftKey && !event.ctrlKey && !event.metaKey && event.key.toLowerCase() === 'o') {
        event.preventDefault();
        setOpen(true);
        requestAnimationFrame(() => inputRef.current?.focus());
      } else if (event.key === 'Escape' && open) {
        setOpen(false);
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [open]);

  const busy = useMemo(
    () => exchanges.some((exchange) => exchange.state === 'preparing' || exchange.state === 'streaming'),
    [exchanges],
  );

  // Task 6: a hard failure (not an offline queue) gets a manual way back in, distinct from the
  // automatic reconnect flush that already handles the "unreachable" queued case. The retry
  // re-runs this exchange in place instead of appending a second card for the same question.
  const retry = (exchange: Exchange) => {
    if (busy) return;
    void sendPayload(exchange.payload, undefined, exchange.id);
  };

  const submit = async () => {
    const trimmed = query.trim();
    // `busy` comes from the last render; the ref also blocks a second submit fired before it re-renders.
    if (!trimmed || busy || submittingRef.current) return;
    submittingRef.current = true;
    const payload: OracleQueryPayload = {
      query: trimmed,
      contextTag: currentContextTag(),
      sessionHistory: historyFrom(exchangesRef.current),
      locale,
    };
    setQuery('');
    try {
      await sendPayload(payload);
    } finally {
      submittingRef.current = false;
    }
  };

  const propose = async (exchange: Exchange) => {
    const creativeSegments = exchange.segments.filter((segment) => segment.mode === 'creative');
    const creativeAnswer = creativeSegments.map((segment) => segment.text).join('');
    if (!creativeAnswer || exchange.proposalState === 'saving') return;
    updateExchange(exchange.id, (item) => ({ ...item, proposalState: 'saving' }));
    const suggestedTags = creativeSegments.find((segment) => segment.tags?.length)?.tags;
    const suggestedSection = creativeSegments.find((segment) => segment.themes?.length)?.themes?.[0];
    const body: OracleProposeRequest = {
      query: exchange.query,
      creativeAnswer,
      locale,
      ...(suggestedTags ? { suggestedTags } : {}),
      ...(suggestedSection ? { suggestedSection } : {}),
    };
    try {
      const response = await fetch('/api/v1/oracle/propose', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
      });
      if (!response.ok) throw new Error(`Proposal request failed (${response.status})`);
      updateExchange(exchange.id, (item) => ({ ...item, proposalState: 'saved' }));
    } catch (error) {
      await enqueueErrorReport(error instanceof Error ? error.message : String(error)).catch(() => undefined);
      updateExchange(exchange.id, (item) => ({ ...item, proposalState: 'error' }));
    }
  };

  return (
    <section className="oracle-shell" aria-label={copy.title}>
      <button className="oracle-toggle" type="button" onClick={() => setOpen((value) => !value)} aria-expanded={open}>
        {open ? copy.close : copy.open}
      </button>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            className="oracle-terminal"
            initial={reduceMotion ? false : { opacity: 0, y: 18, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={reduceMotion ? { opacity: 0 } : { opacity: 0, y: 12, scale: 0.99 }}
            transition={{ duration: reduceMotion ? 0 : 0.22 }}
          >
            <header><span>{copy.eyebrow}</span><h1>{copy.title}</h1></header>
            <div className="oracle-log">
              <AnimatePresence initial={false}>
                {exchanges.map((exchange, index) => (
                  <motion.article key={exchange.id} className="oracle-exchange" initial={reduceMotion ? false : { opacity: 0 }} animate={{ opacity: 1 }}>
                    {/* Task 4: a visually hidden heading names each turn, so past exchanges can be reached
                        and told apart by heading navigation. It sits outside the Task 2 live region. */}
                    <h2 className="sr-only">{copy.exchange} {index + 1}</h2>
                    <p className="oracle-query"><strong>›</strong> {exchange.query}</p>
                    {exchange.contextTag && <p className="oracle-context">{copy.context}: <code>{exchange.contextTag}</code></p>}
                    {/* Task 2: only the streamed answer is a live region (not the whole log), so the query echo,
                        status and notices are not re-announced. `polite` waits for the screen reader to finish
                        speaking instead of interrupting it; `aria-atomic="false"` announces only what each chunk
                        changed, never the whole accumulated answer; `aria-busy` marks it in progress while streaming. */}
                    <div
                      className="oracle-answer" aria-live="polite" aria-atomic="false"
                      aria-busy={exchange.state === 'preparing' || exchange.state === 'streaming'}
                    >
                    {exchange.segments.map((segment) => (
                      <div
                        key={segment.key} className={`oracle-segment oracle-${segment.mode}`}
                        role="group" aria-labelledby={`oracle-mode-${segment.key}`}
                      >
                        <ModeLabel id={`oracle-mode-${segment.key}`} mode={segment.mode} copy={copy} />
                        {(segment.themes?.length || segment.tags?.length) ? (
                          <p className="oracle-anchors">
                            {segment.themes?.length ? (
                              <><span>{copy.themes}:</span> {segment.themes.map((theme) => <code key={theme}>{theme}</code>)}{' '}</>
                            ) : null}
                            {segment.tags?.length ? (
                              <><span>{copy.tags}:</span> {segment.tags.map((tag) => <code key={tag}>{tag}</code>)}</>
                            ) : null}
                          </p>
                        ) : null}
                        <p>{segment.parts.map((part, index) => <span key={index}>{part}</span>)}</p>
                        {segment.mode === 'grounded' && segment.citedQuoteIds?.length ? (
                          <CitationLinks ids={segment.citedQuoteIds} locale={locale} copy={copy} />
                        ) : null}
                      </div>
                    ))}
                    </div>
                    {/* Task 5: distinct from both idle and streaming, and never shown once a chunk (or an
                        error) has settled the exchange into another state. */}
                    {exchange.state === 'preparing' && <p className="oracle-status oracle-preparing" role="status">{copy.preparing}</p>}
                    {exchange.state === 'streaming' && <p className="oracle-status" role="status">{copy.streaming}</p>}
                    {/* Task 6: a hard failure is announced assertively and offers a manual way back in;
                        the offline-queue notice stays `status` since it is not a failure, just a wait. */}
                    {exchange.notice && (
                      <p className="oracle-notice" role={exchange.state === 'error' ? 'alert' : 'status'}>{exchange.notice}</p>
                    )}
                    {exchange.state === 'error' && (
                      <button type="button" className="oracle-retry" onClick={() => retry(exchange)} disabled={busy}>
                        {copy.retry}
                      </button>
                    )}
                    {exchange.state === 'complete' && exchange.segments.some((segment) => segment.mode === 'creative') && (
                      <div className="oracle-proposal">
                        <button type="button" onClick={() => void propose(exchange)} disabled={exchange.proposalState === 'saving' || exchange.proposalState === 'saved'}>
                          {exchange.proposalState === 'saving' ? copy.proposing : copy.propose}
                        </button>
                        {exchange.proposalState === 'saved' && <p role="status">{copy.proposed}</p>}
                        {exchange.proposalState === 'error' && <p role="alert">{copy.proposalError}</p>}
                      </div>
                    )}
                  </motion.article>
                ))}
              </AnimatePresence>
              {syncing && <p className="oracle-status">{copy.syncing}</p>}
            </div>
            <form onSubmit={(event) => { event.preventDefault(); void submit(); }}>
              <label className="sr-only" htmlFor="oracle-query">{copy.placeholder}</label>
              <textarea
                id="oracle-query" ref={inputRef} value={query} onChange={(event) => setQuery(event.target.value)}
                onKeyDown={(event) => {
                  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
                    event.preventDefault();
                    void submit();
                  }
                }}
                placeholder={copy.placeholder} rows={3} maxLength={8000}
              />
              <button type="submit" disabled={!query.trim() || busy}>{copy.submit}</button>
            </form>
            <p className="oracle-hint">{copy.hint}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}
