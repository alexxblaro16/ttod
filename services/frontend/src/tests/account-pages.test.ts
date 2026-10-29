import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { loadRenderers } from 'astro:container';
import { getContainerRenderer } from '@astrojs/react';
import { JSDOM } from 'jsdom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import type { WisdomEntry } from '../types/domain';

import AccountRoute from '../pages/[locale]/account.astro';
import LibraryRoute from '../pages/[locale]/library.astro';
import ReviewerRoute from '../pages/[locale]/account/reviewer/index.astro';
import { ALL as logoutOther, POST as logout } from '../pages/[locale]/logout';

const student = { id: 'usr-002', email: 'student@example.com', roles: ['student'] };
const reviewer = { id: 'usr-001', email: 'admin@example.com', roles: ['reviewer', 'instructor'] };
const quote: WisdomEntry = {
  id: 'arch-001', section: 'architecture', level: 'advanced', tags: ['boundaries'],
  text: 'The module that knows its boundaries serves the whole.',
  teaches: 'Boundaries', related: [], origin: 'human', lang: 'en',
  rights: { license: 'CC-BY-NC-SA-4.0', holder: 'ruvebal@crea-comm.net' },
};
const cookie = 'ttod_session=opaque-session-id';

afterEach(() => vi.restoreAllMocks());

type Answer = unknown | Error | { status: number };
// Cada ruta del backend contesta por separado: un Error simula que no responde y
// `{ status }` una respuesta de error.
function mockBackend(routes: Record<string, Answer>) {
  return vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
    const url = String(input);
    const key = Object.keys(routes).find((path) => url.includes(path));
    if (!key) throw new Error(`unexpected backend call: ${url}`);
    const answer = routes[key];
    if (answer instanceof Error) throw answer;
    if (answer && typeof answer === 'object' && 'status' in answer && Object.keys(answer).length === 1) {
      return new Response(null, { status: (answer as { status: number }).status });
    }
    return Response.json(answer);
  });
}

async function render(route: unknown, path: string, locale: 'en' | 'es' = 'en') {
  const renderers = await loadRenderers([getContainerRenderer()]);
  const container = await AstroContainer.create({ renderers });
  const response = await container.renderToResponse(route as never, {
    params: { locale },
    request: new Request(`http://localhost/${locale}${path}`, { headers: { cookie } }),
  });
  const main = new JSDOM(await response.text()).window.document.querySelector('main');
  return { status: response.status, main };
}

function logoutContext(locale: string, withCookie = true) {
  const cookies = { delete: vi.fn() };
  const context = {
    params: { locale },
    request: new Request(`http://localhost/${locale}/logout`, {
      method: 'POST', headers: withCookie ? { cookie } : {},
    }),
    cookies,
    redirect: (location: string, status = 302) => new Response(null, { status, headers: { location } }),
  };
  return { context: context as never, cookies };
}

describe('logging out', () => {
  it('revokes the session in the backend, deletes the cookie and goes home', async () => {
    const fetchSpy = mockBackend({ '/api/v1/auth/logout': { status: 204 } });
    const { context, cookies } = logoutContext('es');

    const response = await logout(context);

    expect(response.status).toBe(303);
    expect(response.headers.get('location')).toBe('/es/');
    expect(cookies.delete).toHaveBeenCalledWith('ttod_session', { path: '/' });
    const [url, init] = fetchSpy.mock.calls[0];
    expect(String(url)).toMatch(/\/api\/v1\/auth\/logout$/);
    expect(init).toMatchObject({ method: 'POST', headers: { cookie } });
  });

  it('keeps the cookie and says so when the backend cannot revoke the session', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => undefined);
    for (const failure of [{ status: 503 }, new Error('network unavailable')]) {
      mockBackend({ '/api/v1/auth/logout': failure });
      const { context, cookies } = logoutContext('en');

      const response = await logout(context);

      expect(response.headers.get('location')).toBe('/en/account?logout=failed');
      expect(cookies.delete).not.toHaveBeenCalled();
    }
  });

  it('without a session there is nothing to revoke: it just goes home', async () => {
    const fetchSpy = mockBackend({});
    const { context } = logoutContext('en', false);

    expect((await logout(context)).headers.get('location')).toBe('/en/');
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it('only answers POST, so a link or an image cannot log anyone out', async () => {
    const response = await logoutOther(logoutContext('en').context);

    expect(response.status).toBe(405);
    expect(response.headers.get('allow')).toBe('POST');
  });
});

describe('my account', () => {
  it('offers the library and a logout form that posts to the localized route', async () => {
    mockBackend({ '/api/v1/auth/session': student });
    const { main } = await render(AccountRoute, '/account', 'es');

    expect(main?.querySelector('a[href="/es/library"]')?.textContent).toBe('Mi biblioteca');
    const form = main?.querySelector('form');
    expect(form?.getAttribute('method')).toBe('post');
    expect(form?.getAttribute('action')).toBe('/es/logout');
    expect(form?.querySelector('button[type="submit"]')?.textContent).toBe('Cerrar sesión');
  });

  it('links the reviewer queue only for reviewers and instructors', async () => {
    mockBackend({ '/api/v1/auth/session': student });
    expect((await render(AccountRoute, '/account')).main?.querySelector('a[href="/en/account/reviewer"]')).toBeNull();

    vi.restoreAllMocks();
    mockBackend({ '/api/v1/auth/session': reviewer });
    expect((await render(AccountRoute, '/account')).main?.querySelector('a[href="/en/account/reviewer"]')?.textContent)
      .toBe('Reviewer queue');
  });

  it('explains a failed logout instead of pretending it worked', async () => {
    mockBackend({ '/api/v1/auth/session': student });
    const { main } = await render(AccountRoute, '/account?logout=failed');

    expect(main?.querySelector('[role="alert"]')?.textContent).toContain('You are still logged in');
  });
});

describe('personal library', () => {
  it('lists each saved quote with a link to its page and a readable date', async () => {
    mockBackend({
      '/api/v1/auth/session': student,
      '/api/v1/favorites': [{ userId: 'usr-002', quoteId: 'arch-001', savedAt: '2026-10-01T10:00:00Z' }],
      '/api/v1/wisdom/sample': [quote],
    });
    const { status, main } = await render(LibraryRoute, '/library', 'es');

    expect(status).toBe(200);
    expect(main?.querySelector('blockquote')?.textContent).toBe(quote.text);
    expect(main?.querySelector('a[href="/es/wisdom/arch-001/"]')?.textContent).toBe('arch-001');
    const time = main?.querySelector('time');
    expect(time?.getAttribute('datetime')).toBe('2026-10-01T10:00:00.000Z');
    expect(time?.textContent).toBe('1 de octubre de 2026');
    expect(main?.querySelector('astro-island button')?.textContent).toBe('Quitar de favoritos');
  });

  it('an empty library says so and points to the wisdom', async () => {
    mockBackend({ '/api/v1/auth/session': student, '/api/v1/favorites': [], '/api/v1/wisdom/sample': [quote] });
    const { main } = await render(LibraryRoute, '/library');

    expect(main?.textContent).toContain('You have not saved any quotes yet.');
    expect(main?.querySelector('a[href="/en/wisdom/"]')).not.toBeNull();
    expect(main?.querySelector('[role="alert"]')).toBeNull();
  });

  it('when the backend fails it answers 503 with an error, never with "no quotes saved"', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => undefined);
    const failures: Record<string, Answer>[] = [
      { '/api/v1/favorites': { status: 503 }, '/api/v1/wisdom/sample': [quote] },
      { '/api/v1/favorites': [], '/api/v1/wisdom/sample': new Error('network unavailable') },
    ];
    for (const routes of failures) {
      vi.restoreAllMocks();
      vi.spyOn(console, 'error').mockImplementation(() => undefined);
      mockBackend({ '/api/v1/auth/session': student, ...routes });
      const { status, main } = await render(LibraryRoute, '/library');

      expect(status).toBe(503);
      expect(main?.querySelector('[role="alert"]')?.textContent).toContain('could not be loaded');
      expect(main?.textContent).not.toContain('You have not saved any quotes yet.');
    }
  });
});

describe('reviewer queue', () => {
  it('when the backend fails it answers 503 with an error, never with "no pending proposals"', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => undefined);
    mockBackend({ '/api/v1/auth/session': reviewer, '/api/v1/proposals': new Error('network unavailable') });
    const { status, main } = await render(ReviewerRoute, '/account/reviewer', 'es');

    expect(status).toBe(503);
    expect(main?.querySelector('[role="alert"]')?.textContent).toContain('No se ha podido cargar la cola');
    expect(main?.textContent).not.toContain('No hay propuestas pendientes.');
  });

  it('an empty queue is still reported as empty', async () => {
    mockBackend({ '/api/v1/auth/session': reviewer, '/api/v1/proposals': [] });
    const { status, main } = await render(ReviewerRoute, '/account/reviewer');

    expect(status).toBe(200);
    expect(main?.textContent).toContain('There are no pending proposals.');
  });
});
