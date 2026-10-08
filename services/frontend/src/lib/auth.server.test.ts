import { afterEach, describe, expect, it, vi } from 'vitest';

import { getSessionUser, loginWithBackend, requireRole, requireUser } from './auth.server';

const reviewer = { id: 'usr-001', email: 'admin@ttod.local', roles: ['reviewer', 'instructor'] };
const student = { id: 'usr-002', email: 'student@ttod.local', roles: ['student'] };

function accountRequest(locale: 'en' | 'es', sessionToken?: string): Request {
  return new Request(`http://localhost:4321/${locale}/account`, {
    headers: sessionToken ? { cookie: `theme=dark; ttod_session=${sessionToken}` } : {}
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe('SSR session guard', () => {
  it('redirects an anonymous request to the localized login with an empty body', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch');

    const result = await requireUser(accountRequest('es'));

    expect(result).toBeInstanceOf(Response);
    const response = result as Response;
    expect(response.status).toBe(302);
    expect(response.headers.get('location')).toBe('/es/login');
    await expect(response.text()).resolves.toBe('');
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it('returns the user only after the backend verifies the session cookie', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json(reviewer));

    await expect(requireUser(accountRequest('en', 'signed-session'))).resolves.toEqual(reviewer);

    const [url, init] = fetchSpy.mock.calls[0];
    expect(String(url)).toContain('/api/v1/auth/session');
    expect(init?.headers).toMatchObject({ cookie: 'ttod_session=signed-session' });
    expect(init?.headers).not.toHaveProperty('authorization');
  });

  it('treats a session the backend rejects as anonymous', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(null, { status: 401 }));

    const result = await requireUser(accountRequest('en', 'expired-session'));

    expect((result as Response).status).toBe(302);
    expect((result as Response).headers.get('location')).toBe('/en/login');
  });

  it('rejects a backend payload that does not match the shared AuthUser contract', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      Response.json({ id: 'usr-001', email: 'a@b.test', roles: ['owner'] })
    );

    await expect(getSessionUser(accountRequest('en', 'signed-session'))).resolves.toBeNull();
  });

  it('fails closed and logs when the session service cannot be reached', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new Error('network unavailable'));
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => undefined);

    await expect(getSessionUser(accountRequest('en', 'signed-session'))).resolves.toBeNull();
    expect(errorSpy).toHaveBeenCalledWith('Unable to verify the server-side session.', expect.any(Error));
  });
});

describe('SSR role guard', () => {
  it('lets a user through when one of their roles is allowed', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(async () => Response.json(reviewer));

    await expect(requireRole(accountRequest('en', 'signed-session'), 'reviewer')).resolves.toEqual(reviewer);
    await expect(
      requireRole(accountRequest('en', 'signed-session'), ['student', 'instructor'])
    ).resolves.toEqual(reviewer);
  });

  it('returns 403 without user data when the role is not allowed', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json(student));

    const result = await requireRole(accountRequest('en', 'signed-session'), ['reviewer', 'instructor']);

    expect(result).toBeInstanceOf(Response);
    const response = result as Response;
    expect(response.status).toBe(403);
    expect(await response.text()).not.toContain(student.email);
  });

  it('sends an anonymous request to login instead of answering 403', async () => {
    const result = await requireRole(accountRequest('es'), 'reviewer');

    expect((result as Response).status).toBe(302);
    expect((result as Response).headers.get('location')).toBe('/es/login');
  });
});

describe('login against the backend', () => {
  it('posts the credentials and returns the session token issued by the backend', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json({
      session_token: 'signed-session', token_type: 'Session', expires_in: 3600, user: reviewer
    }));

    await expect(loginWithBackend('admin@ttod.local', 'a-password')).resolves.toEqual({
      ok: true, sessionToken: 'signed-session', expiresIn: 3600
    });

    const [url, init] = fetchSpy.mock.calls[0];
    expect(String(url)).toContain('/api/v1/auth/login');
    expect(init?.method).toBe('POST');
    expect(JSON.parse(String(init?.body))).toEqual({ email: 'admin@ttod.local', password: 'a-password' });
  });

  it('reports wrong credentials when the backend answers 401', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(null, { status: 401 }));

    await expect(loginWithBackend('admin@ttod.local', 'wrong')).resolves.toEqual({
      ok: false, reason: 'credentials'
    });
  });

  it('reports a service failure for an unexpected body or an unreachable backend', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => undefined);
    vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(Response.json({ access_token: 'legacy', token_type: 'Bearer' }))
      .mockRejectedValueOnce(new Error('network unavailable'));

    await expect(loginWithBackend('admin@ttod.local', 'a-password')).resolves.toEqual({
      ok: false, reason: 'service'
    });
    await expect(loginWithBackend('admin@ttod.local', 'a-password')).resolves.toEqual({
      ok: false, reason: 'service'
    });
  });
});
