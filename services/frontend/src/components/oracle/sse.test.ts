import { describe, expect, it } from 'vitest';

import { parseSseEvent, readOracleStream } from './sse';

describe('oracle SSE reader', () => {
  it('parses a valid envelope and ignores the done sentinel', () => {
    expect(parseSseEvent('data: {"mode":"creative","text":"hello"}')).toEqual({
      mode: 'creative', text: 'hello',
    });
    expect(parseSseEvent('data: [DONE]')).toBeNull();
  });

  it('rejects malformed provenance envelopes', () => {
    expect(() => parseSseEvent('data: {"mode":"invented","text":"hello"}')).toThrow(
      'invalid response chunk',
    );
  });

  it('handles response chunks split across byte boundaries', async () => {
    const encoder = new TextEncoder();
    const body = new ReadableStream<Uint8Array>({
      start(controller) {
        controller.enqueue(encoder.encode('data: {"mode":"ground'));
        controller.enqueue(encoder.encode('ed","citedQuoteIds":["wis-001"],"text":"A"}\r\n\r\n'));
        controller.enqueue(encoder.encode('data: {"mode":"creative","text":"B"}\n\n'));
        controller.close();
      },
    });
    const chunks: unknown[] = [];
    const count = await readOracleStream(new Response(body), (chunk) => chunks.push(chunk));
    expect(count).toBe(2);
    expect(chunks).toEqual([
      { mode: 'grounded', citedQuoteIds: ['wis-001'], text: 'A' },
      { mode: 'creative', text: 'B' },
    ]);
  });

  it('delivers earlier chunks before failing on a malformed envelope', async () => {
    const encoder = new TextEncoder();
    const body = new ReadableStream<Uint8Array>({
      start(controller) {
        controller.enqueue(encoder.encode('data: {"mode":"creative","text":"before"}\n\n'));
        // No `text`: not a valid OracleResponseChunk.
        controller.enqueue(encoder.encode('data: {"mode":"creative"}\n\n'));
        controller.close();
      },
    });
    const delivered: unknown[] = [];
    await expect(
      readOracleStream(new Response(body), (chunk) => delivered.push(chunk)),
    ).rejects.toThrow('invalid response chunk');
    // The good chunk already reached the caller — nothing is buffered until the stream closes.
    expect(delivered).toEqual([{ mode: 'creative', text: 'before' }]);
  });

  it('rejects a response with no body instead of resolving with zero chunks', async () => {
    await expect(readOracleStream(new Response(null), () => undefined)).rejects.toThrow(
      'no response body',
    );
  });
});

