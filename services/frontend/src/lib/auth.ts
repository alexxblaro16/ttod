import type { AstroGlobal } from 'astro';
import type { AuthRole, AuthUser } from '../types/domain';

export const AUTH_COOKIE_NAME = 'ttod_access_token';
const BACKEND_URL = import.meta.env.BACKEND_URL ?? 'http://localhost:8000';

export async function getSessionUser(cookies: AstroGlobal['cookies']): Promise<AuthUser | null> {
  return getSessionUserFromToken(cookies.get(AUTH_COOKIE_NAME)?.value);
}

export async function getSessionUserFromToken(token?: string): Promise<AuthUser | null> {
  if (!token) return null;
  try {
    const response = await fetch(`${BACKEND_URL}/api/v1/auth/session`, {
      headers: { accept: 'application/json', authorization: `Bearer ${token}` }
    });
    if (!response.ok) return null;

    const user: unknown = await response.json();
    if (typeof user !== 'object' || user === null) return null;
    const candidate = user as Partial<AuthUser>;
    if (
      typeof candidate.id !== 'string' ||
      typeof candidate.email !== 'string' ||
      (candidate.role !== 'admin' && candidate.role !== 'user')
    ) return null;

    return candidate as AuthUser;
  } catch (error) {
    console.error('Unable to verify the server-side session.', error);
    return null;
  }
}

export async function requireUser(astro: AstroGlobal): Promise<AuthUser | Response> {
  const user = await getSessionUser(astro.cookies);

  if (!user) {
    const locale = astro.params.locale === 'es' ? 'es' : 'en';
    return astro.redirect(`/${locale}/login`);
  }

  return user;
}

export async function requireRole(astro: AstroGlobal, requiredRole: AuthRole): Promise<AuthUser | Response> {
  const user = await requireUser(astro);
  if (user instanceof Response) return user;

  if (user.role !== requiredRole) {
    const locale = astro.params.locale === 'es' ? 'es' : 'en';
    return astro.redirect(`/${locale}/unauthorized`);
  }

  return user;
}
