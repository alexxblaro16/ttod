import { describe, expect, it } from 'vitest';

import { getSessionClaims, requireRole } from './auth.server';

describe('server session role guard', () => {
  it('rejects an unauthenticated request with 403', async () => {
    await expect(requireRole(new Request('http://localhost/en/account/reviewer'), ['reviewer']))
      .rejects.toMatchObject({ status: 403 });
  });

  it('rejects a student session', async () => {
    const request = new Request('http://localhost/en/account/reviewer', {
      headers: { cookie: 'ttod_session=%7B%22userId%22%3A%22student-1%22%2C%22roles%22%3A%5B%22student%22%5D%7D' },
    });
    await expect(requireRole(request, ['reviewer', 'instructor'])).rejects.toMatchObject({ status: 403 });
  });

  it.each(['reviewer', 'instructor'])('allows the %s role', async (role) => {
    const request = new Request('http://localhost/en/account/reviewer', {
      headers: { authorization: `Bearer ${JSON.stringify({ userId: `${role}-1`, roles: [role] })}` },
    });
    await expect(requireRole(request, ['reviewer', 'instructor'])).resolves.toMatchObject({
      userId: `${role}-1`, roles: [role],
    });
  });

  it('keeps legacy plain sessions authenticated without granting reviewer access', () => {
    expect(getSessionClaims(new Request('http://localhost', { headers: { authorization: 'Bearer student-1' } })))
      .toEqual({ userId: 'student-1', roles: [] });
  });
});