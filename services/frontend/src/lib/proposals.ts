import type { ProposalPayload } from './proposeForm';

// Real fetch against the real path — same pattern as content/wisdom.ts's fetchWisdom(). The
// endpoint already exists, implemented and tested, in PR #57 (upstream, not merged into main):
// today this legitimately 404s until that PR lands, and "endpoint doesn't exist yet" is one of
// the error states this task's own brief explicitly asks the UI to handle — so there is nothing
// to "swap out" later, this function already is the real integration.
export type ProposalResult =
  | { ok: true; id: string }
  | { ok: false; reason: 'unauthenticated' | 'validation' | 'server' | 'not-found' | 'network' };

export async function submitProposal(payload: ProposalPayload): Promise<ProposalResult> {
  const backend = import.meta.env.BACKEND_URL ?? 'http://backend:8000';
  let response: Response;
  try {
    response = await fetch(`${backend}/api/v1/proposals`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'content-type': 'application/json', accept: 'application/json' },
      body: JSON.stringify(payload),
    });
  } catch {
    return { ok: false, reason: 'network' };
  }

  if (response.status === 201) {
    const body = (await response.json().catch(() => null)) as { id?: unknown } | null;
    return { ok: true, id: typeof body?.id === 'string' ? body.id : 'pending' };
  }
  if (response.status === 401) return { ok: false, reason: 'unauthenticated' };
  if (response.status === 422 || response.status === 400) return { ok: false, reason: 'validation' };
  if (response.status === 404) return { ok: false, reason: 'not-found' };
  return { ok: false, reason: 'server' };
}
