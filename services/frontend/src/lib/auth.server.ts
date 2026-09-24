export type SessionRole = 'student' | 'reviewer' | 'instructor';

export interface SessionClaims {
  userId: string;
  roles: SessionRole[];
}

function sessionValue(request: Request): string | null {
  const session = request.headers.get('cookie')?.match(/(?:^|;\s*)ttod_session=([^;]+)/)?.[1];
  if (session?.trim()) return decodeURIComponent(session.trim());

  const authorization = request.headers.get('authorization');
  if (authorization?.startsWith('Bearer ')) {
    const userId = authorization.slice('Bearer '.length).trim();
    if (userId) return userId;
  }

  return null;
}

export function getSessionClaims(request: Request): SessionClaims | null {
  const raw = sessionValue(request);
  if (!raw) return null;

  try {
    const parsed = JSON.parse(raw) as { userId?: unknown; role?: unknown; roles?: unknown };
    const userId = typeof parsed.userId === 'string' ? parsed.userId.trim() : '';
    const roles = Array.isArray(parsed.roles)
      ? parsed.roles
      : typeof parsed.role === 'string' ? [parsed.role] : [];
    const validRoles = roles.filter((role): role is SessionRole => (
      role === 'student' || role === 'reviewer' || role === 'instructor'
    ));
    return userId ? { userId, roles: validRoles } : null;
  } catch {
    return { userId: raw, roles: [] };
  }
}

export function requireUser(request: Request): string | null {
  return getSessionClaims(request)?.userId ?? null;
}

export async function requireRole(request: Request, allowedRoles: SessionRole[]): Promise<SessionClaims> {
  const claims = getSessionClaims(request);
  if (!claims || !claims.roles.some((role) => allowedRoles.includes(role))) {
    throw new Response('Forbidden', { status: 403, headers: { 'content-type': 'text/plain' } });
  }
  return claims;
}