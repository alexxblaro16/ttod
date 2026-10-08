import { AUTH_COOKIE_NAME, getSessionUserFromToken } from './auth';
import type { SessionRole } from '../types/domain';

export interface SessionClaims {
  userId: string;
  roles: SessionRole[];
}

export async function getSessionClaims(request: Request): Promise<SessionClaims | null> {
  const encodedToken = request.headers.get('cookie')
    ?.match(new RegExp(`(?:^|;\\s*)${AUTH_COOKIE_NAME}=([^;]+)`))?.[1];
  if (!encodedToken) return null;
  try {
    const user = await getSessionUserFromToken(decodeURIComponent(encodedToken));
    return user ? { userId: user.id, roles: user.roles } : null;
  } catch (error) {
    console.error('Unable to verify the server-side session.', error);
    return null;
  }
}

export async function requireUser(request: Request): Promise<string | null> {
  return (await getSessionClaims(request))?.userId ?? null;
}

export async function requireRole(request: Request, allowedRoles: SessionRole[]): Promise<SessionClaims> {
  const claims = await getSessionClaims(request);
  if (!claims || !claims.roles.some((role) => allowedRoles.includes(role))) {
    throw new Response('Forbidden', { status: 403, headers: { 'content-type': 'text/plain' } });
  }
  return claims;
}