export function requireUser(request: Request): string | null {
  const session = request.headers.get('cookie')?.match(/(?:^|;\s*)ttod_session=([^;]+)/)?.[1];
  if (session?.trim()) return decodeURIComponent(session.trim());

  const authorization = request.headers.get('authorization');
  if (authorization?.startsWith('Bearer ')) {
    const userId = authorization.slice('Bearer '.length).trim();
    if (userId) return userId;
  }

  return null;
}