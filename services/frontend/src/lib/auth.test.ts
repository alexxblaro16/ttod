import type { AstroGlobal } from 'astro';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { getSessionUserFromToken, requireRole, requireUser } from './auth';

afterEach(() => {
  vi.restoreAllMocks();
});

describe('SSR authentication guard', () => {
  it('does not contact the backend when there is no session token', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch');

    await expect(getSessionUserFromToken()).resolves.toBeNull();
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it('accepts only a valid user returned by the backend session endpoint', async () => {
    const user = { id: 'usr-001', email: 'admin@ttod.local', role: 'admin' };
    const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json(user));

    await expect(getSessionUserFromToken('signed-token')).resolves.toEqual(user);
    expect(fetchSpy).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/auth/session'),
      expect.objectContaining({
        headers: expect.objectContaining({ authorization: 'Bearer signed-token' })
      })
    );
  });

  it('rejects malformed session data and non-success backend responses', async () => {
    vi.spyOn(globalThis, 'fetch')
      .mockResolvedValueOnce(Response.json({ id: 'usr-001', email: 'a@b.test', role: 'owner' }))
      .mockResolvedValueOnce(new Response(null, { status: 401 }));

    await expect(getSessionUserFromToken('signed-token')).resolves.toBeNull();
    await expect(getSessionUserFromToken('expired-token')).resolves.toBeNull();
  });

  it('fails closed and logs when the session service cannot be reached', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new Error('network unavailable'));
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => undefined);

    await expect(getSessionUserFromToken('signed-token')).resolves.toBeNull();
    expect(errorSpy).toHaveBeenCalledWith(
      'Unable to verify the server-side session.',
      expect.any(Error)
    );
  });

  it('allows the required role and redirects users with a different role', async () => {
    const user = { id: 'usr-002', email: 'user@ttod.local', role: 'user' };
    vi.spyOn(globalThis, 'fetch').mockImplementation(async () => Response.json(user));
    const redirect = vi.fn((path: string) => new Response(null, {
      status: 302,
      headers: { location: path }
    }));
    const astro = {
      params: { locale: 'es' },
      cookies: { get: () => ({ value: 'signed-token' }) },
      redirect
    } as unknown as AstroGlobal;

    await expect(requireRole(astro, 'user')).resolves.toEqual(user);
    const denied = await requireRole(astro, 'admin');
    expect(denied).toBeInstanceOf(Response);
    expect((denied as Response).headers.get('location')).toBe('/es/unauthorized');
  });

  it('redirects an anonymous request to the localized login without rendering protected content', async () => {
    const redirect = vi.fn((path: string) => new Response(null, {
      status: 302,
      headers: { location: path }
    }));
    const astro = {
      params: { locale: 'es' },
      cookies: { get: () => undefined },
      redirect
    } as unknown as AstroGlobal;

    const result = await requireUser(astro);

    expect(result).toBeInstanceOf(Response);
    expect((result as Response).status).toBe(302);
    expect((result as Response).headers.get('location')).toBe('/es/login');
    await expect((result as Response).text()).resolves.toBe('');
  });

  it('propagates the anonymous redirect from requireUser through requireRole', async () => {
    const redirect = vi.fn((path: string) => new Response(null, {
      status: 302,
      headers: { location: path }
    }));
    const astro = {
      params: { locale: 'en' },
      cookies: { get: () => undefined },
      redirect
    } as unknown as AstroGlobal;

    const result = await requireRole(astro, 'admin');

    expect(result).toBeInstanceOf(Response);
    expect((result as Response).status).toBe(302);
    expect((result as Response).headers.get('location')).toBe('/en/login');
    await expect((result as Response).text()).resolves.toBe('');
  });
});
