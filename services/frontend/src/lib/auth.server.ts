import type { AuthLoginResponse, AuthUser, SessionRole } from '../types/domain';

export const SESSION_COOKIE_NAME = 'ttod_session';

const BACKEND_URL = import.meta.env.BACKEND_URL ?? 'http://backend:8000';
const SESSION_ROLES: readonly SessionRole[] = ['student', 'reviewer', 'instructor'];

export type LoginResult =
  | { ok: true; sessionToken: string; expiresIn: number }
  | { ok: false; reason: 'credentials' | 'service' };

export type RegisterResult =
  | { ok: true; sessionToken: string; expiresIn: number }
  | { ok: false; reason: 'taken' | 'invalid' | 'service' };

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

function readIssuedSession(value: unknown): { sessionToken: string; expiresIn: number } | null {
  const login = value as Partial<AuthLoginResponse>;
  if (
    typeof login.session_token !== 'string' || login.session_token.length === 0 ||
    login.token_type !== 'Session' ||
    typeof login.expires_in !== 'number' || login.expires_in <= 0 ||
    !isAuthUser(login.user)
  ) return null;
  return { sessionToken: login.session_token, expiresIn: login.expires_in };
}

function localeOf(request: Request): 'en' | 'es' {
  return new URL(request.url).pathname.split('/')[1] === 'es' ? 'es' : 'en';
}

export async function loginWithBackend(email: string, password: string): Promise<LoginResult> {
  if (email.trim() === '' || password === '') return { ok: false, reason: 'credentials' };

  try {
    const response = await fetch(`${BACKEND_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: { accept: 'application/json', 'content-type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (response.status === 401 || response.status === 422) return { ok: false, reason: 'credentials' };
    if (!response.ok) return { ok: false, reason: 'service' };

    const session = readIssuedSession(await response.json());
    return session ? { ok: true, ...session } : { ok: false, reason: 'service' };
  } catch (error) {
    console.error('The authentication service could not complete the login request.', error);
    return { ok: false, reason: 'service' };
  }
}

export async function registerWithBackend(email: string, password: string): Promise<RegisterResult> {
  if (email.trim() === '' || password === '') return { ok: false, reason: 'invalid' };

  try {
    const response = await fetch(`${BACKEND_URL}/api/v1/auth/register`, {
      method: 'POST',
      headers: { accept: 'application/json', 'content-type': 'application/json' },
      body: JSON.stringify({ email: email.trim(), password })
    });
    if (response.status === 409) return { ok: false, reason: 'taken' };
    if (response.status === 422) return { ok: false, reason: 'invalid' };
    if (!response.ok) return { ok: false, reason: 'service' };

    const session = readIssuedSession(await response.json());
    return session ? { ok: true, ...session } : { ok: false, reason: 'service' };
  } catch (error) {
    console.error('The authentication service could not complete the sign-up request.', error);
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

/**
 * La ruta a la que volver tras entrar. Solo rutas de este mismo sitio («/algo»):
 * «//otro.com», «/\\otro.com» o una URL completa serían una redirección abierta.
 */
export function safeNextPath(value: unknown, locale: 'en' | 'es'): string {
  const fallback = `/${locale}/account`;
  if (typeof value !== 'string' || !value.startsWith('/') || value.startsWith('//')) return fallback;
  if (/[\\\u0000-\u001f]/.test(value)) return fallback;
  if (/^\/(en|es)\/(login|register)\/?(\?|$)/.test(value)) return fallback;
  return value;
}

// Las guardas devuelven el Response en vez de lanzarlo: en Astro 5 un `throw` de un
// Response desde el frontmatter termina en un 500, no en la redirección esperada.
export async function requireUser(request: Request): Promise<AuthUser | Response> {
  const user = await getSessionUser(request);
  if (user) return user;
  const { pathname, search } = new URL(request.url);
  // Tras entrar se vuelve aquí: el login lee `next` y solo acepta rutas de este sitio.
  const next = encodeURIComponent(pathname + search);
  return new Response(null, { status: 302, headers: { location: `/${localeOf(request)}/login?next=${next}` } });
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
