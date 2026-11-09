import type { OracleResponseChunk } from '../../types/domain';

function isStringList(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === 'string');
}

function isChunk(value: unknown): value is OracleResponseChunk {
  if (!value || typeof value !== 'object') return false;
  const candidate = value as Partial<OracleResponseChunk>;
  return (
    (candidate.mode === 'grounded' || candidate.mode === 'creative') &&
    typeof candidate.text === 'string' &&
    (candidate.citedQuoteIds === undefined || isStringList(candidate.citedQuoteIds)) &&
    (candidate.themes === undefined || isStringList(candidate.themes)) &&
    (candidate.tags === undefined || isStringList(candidate.tags))
  );
}

export function parseSseEvent(block: string): OracleResponseChunk | null {
  const data = block
    .split(/\r?\n/)
    .filter((line) => line.startsWith('data:'))
    .map((line) => line.slice(5).replace(/^ /, ''))
    .join('\n');
  if (!data || data === '[DONE]') return null;
  const parsed: unknown = JSON.parse(data);
  if (!isChunk(parsed)) throw new Error('Oracle stream returned an invalid response chunk');
  return parsed;
}

export async function readOracleStream(
  response: Response,
  onChunk: (chunk: OracleResponseChunk) => void,
): Promise<number> {
  if (!response.body) throw new Error('Oracle stream returned no response body');
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let count = 0;

  const consume = (event: string) => {
    const chunk = parseSseEvent(event);
    if (chunk) {
      count += 1;
      onChunk(chunk);
    }
  };

  try {
    while (true) {
      const { done, value } = await reader.read();
      buffer += decoder.decode(value, { stream: !done }).replace(/\r\n/g, '\n');
      let boundary = buffer.indexOf('\n\n');
      while (boundary >= 0) {
        consume(buffer.slice(0, boundary));
        buffer = buffer.slice(boundary + 2);
        boundary = buffer.indexOf('\n\n');
      }
      if (done) break;
    }
    if (buffer.trim()) consume(buffer);
    return count;
  } catch (error) {
    // Closing the connection lets the backend stop the local model instead of writing an answer
    // nobody will read; the original error is what the caller needs to see.
    await reader.cancel().catch(() => undefined);
    throw error;
  }
}

