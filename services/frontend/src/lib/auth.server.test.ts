import { afterEach, describe, expect, it, vi } from 'vitest';

import { getSessionClaims, requireRole } from './auth.server';

afterEach(() => {
  vi.restoreAllMocks();
});

describe('server session role guard', () => {
  it('rejects an unauthenticated request without contacting the backend', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch');
    await expect(requireRole(new Request('http://localhost/en/account/reviewer'), ['reviewer']))
      .rejects.toMatchObject({ status: 403 });
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it('rejects unsigned JSON session data', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(null, { status: 401 }));
    const request = new Request('http://localhost/en/account/reviewer', {
      headers: { cookie: 'ttod_session=%7B%22userId%22%3A%22reviewer-1%22%2C%22roles%22%3A%5B%22reviewer%22%5D%7D' },
    });
    await expect(getSessionClaims(request)).resolves.toBeNull();
    expect(fetchSpy).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/auth/session'),
      expect.objectContaining({
        headers: expect.objectContaining({
          authorization: expect.stringMatching(/^Bearer /),
        }),
      }),
    );
  });

  it('rejects a valid student session', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({
      id: 'student-1',
      email: 'student@ttod.local',
      role: 'user',
      roles: ['student'],
    }));
    const request = new Request('http://localhost/en/account/reviewer', {
      headers: { cookie: 'ttod_session=signed-session-token' },
    });
    await expect(requireRole(request, ['reviewer', 'instructor'])).rejects.toMatchObject({ status: 403 });
  });

  it.each(['reviewer', 'instructor'])('allows a verified %s role', async (role) => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({
      id: `${role}-1`,
      email: `${role}@ttod.local`,
      role: 'user',
      roles: [role],
    }));
    const request = new Request('http://localhost/en/account/reviewer', {
      headers: { cookie: 'ttod_session=signed-session-token' },
    });
    await expect(requireRole(request, ['reviewer', 'instructor'])).resolves.toMatchObject({
      userId: `${role}-1`,
      roles: [role],
    });
  });

  it('does not accept an unsigned bearer identity as a web session', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch');
    const request = new Request('http://localhost', {
      headers: { authorization: 'Bearer reviewer-1' },
    });
    await expect(getSessionClaims(request)).resolves.toBeNull();
    expect(fetchSpy).not.toHaveBeenCalled();
  });
});
