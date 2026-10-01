export function requireUser(request: Request): string | null {
  const session = request.headers.get('cookie')?.match(/(?:^|;\s*)ttod_session=([^;]+)/)?.[1];
  if (session?.trim() === 'seeded-user-token') return 'usr-001';

  const authorization = request.headers.get('authorization');
  if (authorization?.startsWith('Bearer ')) {
    const userId = authorization.slice('Bearer '.length).trim();
    if (userId === 'usr-001' || userId === 'usr-002') return userId;
  }

  return null;
}