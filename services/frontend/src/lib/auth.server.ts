import type { AuthLoginResponse, AuthUser, SessionRole } from '../types/domain';

export const SESSION_COOKIE_NAME = 'ttod_session';

const BACKEND_URL = import.meta.env.BACKEND_URL ?? 'http://backend:8000';
const SESSION_ROLES: readonly SessionRole[] = ['student', 'reviewer', 'instructor'];

export type LoginResult =
  | { ok: true; sessionToken: string; expiresIn: number }
  | { ok: false; reason: 'credentials' | 'service' };

function isAuthUser(value: unknown): value is AuthUser {
  if (typeof value !== 'object' || value === null) return false;
  const candidate = value as Partial<AuthUser>;
  return (
    typeof candidate.id === 'string' &&
    typeof candidate.email === 'string' &&
    Array.isArray(candidate.roles) &&
    candidate.roles.every((role) => SESSION_ROLES.includes(role))
  );
}

function readSessionToken(request: Request): string | null {
  const cookieHeader = request.headers.get('cookie');
  if (!cookieHeader) return null;
  for (const pair of cookieHeader.split(';')) {
    const separator = pair.indexOf('=');
    if (separator === -1) continue;
    if (pair.slice(0, separator).trim() === SESSION_COOKIE_NAME) {
      return pair.slice(separator + 1).trim() || null;
    }
  }
  return null;
}

function localeOf(request: Request): 'en' | 'es' {
  return new URL(request.url).pathname.split('/')[1] === 'es' ? 'es' : 'en';
}

export async function loginWithBackend(email: string, password: string): Promise<LoginResult> {
  try {
    const response = await fetch(`${BACKEND_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: { accept: 'application/json', 'content-type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (response.status === 401 || response.status === 422) return { ok: false, reason: 'credentials' };
    if (!response.ok) return { ok: false, reason: 'service' };

    const login = await response.json() as Partial<AuthLoginResponse>;
    if (
      typeof login.session_token !== 'string' || login.session_token.length === 0 ||
      login.token_type !== 'Session' ||
      typeof login.expires_in !== 'number' || login.expires_in <= 0 ||
      !isAuthUser(login.user)
    ) return { ok: false, reason: 'service' };

    return { ok: true, sessionToken: login.session_token, expiresIn: login.expires_in };
  } catch (error) {
    console.error('The authentication service could not complete the login request.', error);
    return { ok: false, reason: 'service' };
  }
}

export async function getSessionUser(request: Request): Promise<AuthUser | null> {
  const sessionToken = readSessionToken(request);
  if (!sessionToken) return null;
  try {
    // La firma solo la comprueba el backend: Astro reenvía la cookie y no confía en su contenido.
    const response = await fetch(`${BACKEND_URL}/api/v1/auth/session`, {
      headers: { accept: 'application/json', cookie: `${SESSION_COOKIE_NAME}=${sessionToken}` }
    });
    if (!response.ok) return null;
    const user: unknown = await response.json();
    return isAuthUser(user) ? user : null;
  } catch (error) {
    // Si el backend no responde se deniega el acceso en lugar de dejar pasar la petición.
    console.error('Unable to verify the server-side session.', error);
    return null;
  }
}

// Las guardas devuelven el Response en vez de lanzarlo: en Astro 5 un `throw` de un
// Response desde el frontmatter termina en un 500, no en la redirección esperada.
export async function requireUser(request: Request): Promise<AuthUser | Response> {
  const user = await getSessionUser(request);
  if (user) return user;
  return new Response(null, { status: 302, headers: { location: `/${localeOf(request)}/login` } });
}

export async function requireRole(
  request: Request,
  allowed: SessionRole | readonly SessionRole[]
): Promise<AuthUser | Response> {
  const user = await requireUser(request);
  if (user instanceof Response) return user;

  const allowedRoles: readonly SessionRole[] = typeof allowed === 'string' ? [allowed] : allowed;
  if (user.roles.some((role) => allowedRoles.includes(role))) return user;
  return new Response('Forbidden', { status: 403, headers: { 'content-type': 'text/plain; charset=utf-8' } });
}
