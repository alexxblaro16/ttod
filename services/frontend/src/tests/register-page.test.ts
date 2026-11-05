import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { loadRenderers } from 'astro:container';
import { getContainerRenderer } from '@astrojs/react';
import { JSDOM } from 'jsdom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import LoginRoute from '../pages/[locale]/login.astro';
import RegisterRoute from '../pages/[locale]/register.astro';

afterEach(() => vi.restoreAllMocks());

const issued = {
  session_token: 'sid-nuevo',
  token_type: 'Session',
  expires_in: 3600,
  user: { id: 'usr-nuevo', email: 'ana@ttod.local', roles: ['student'] }
};

const container = async () => {
  const renderers = await loadRenderers([getContainerRenderer()]);
  return AstroContainer.create({ renderers });
};

const post = (locale: 'en' | 'es', fields: Record<string, string>) => new Request(
  `http://localhost/${locale}/register`,
  { method: 'POST', body: new URLSearchParams(fields), headers: { 'content-type': 'application/x-www-form-urlencoded' } }
);

const send = async (locale: 'en' | 'es', fields: Record<string, string>) =>
  (await container()).renderToResponse(RegisterRoute, { params: { locale }, request: post(locale, fields) });

const mainOf = async (response: Response) => {
  const main = new JSDOM(await response.text()).window.document.querySelector('main');
  if (!main) throw new Error('route rendered no <main>');
  return main;
};

describe('register page', () => {
  it('creates the account in the backend and returns to where the visitor was', async () => {
    const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json(issued, { status: 201 }));

    const response = await send('es', { email: ' ana@ttod.local ', password: 'una-clave-larga', next: '/es/library' });

    expect(response.status).toBe(303);
    expect(response.headers.get('location')).toBe('/es/library');
    const [url, init] = fetchSpy.mock.calls[0];
    expect(String(url)).toContain('/api/v1/auth/register');
    expect(JSON.parse(String(init?.body))).toEqual({ email: 'ana@ttod.local', password: 'una-clave-larga' });
  });

  it('says so when the email already has an account and keeps the email', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(null, { status: 409 }));

    const response = await send('en', { email: 'ana@ttod.local', password: 'una-clave-larga', next: '/en/account' });

    const main = await mainOf(response);
    expect(main.querySelector('[role="alert"]')?.textContent).toContain('already has an account');
    expect(main.querySelector<HTMLInputElement>('#email')?.value).toBe('ana@ttod.local');
  });

  it('never sends the password back to the page after a failure', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(null, { status: 422 }));

    const response = await send('es', { email: 'ana@ttod.local', password: 'una-clave-larga', next: '/es/account' });

    const html = await response.text();
    expect(html).not.toContain('una-clave-larga');
    expect(html).toContain('entre 8 y 72 caracteres');
  });

  it('tells the visitor the service is down when the backend cannot answer', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new Error('offline'));

    const main = await mainOf(await send('en', { email: 'ana@ttod.local', password: 'una-clave-larga', next: '/en/account' }));

    expect(main.querySelector('[role="alert"]')?.textContent).toContain('not answering');
  });

  it('does not redirect to another site after signing up', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(Response.json(issued, { status: 201 }));

    const response = await send('en', { email: 'ana@ttod.local', password: 'una-clave-larga', next: '//evil.example' });

    expect(response.headers.get('location')).toBe('/en/account');
  });

  it('login and register link to each other and keep the return path', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(null, { status: 401 }));
    const app = await container();

    const login = await mainOf(await app.renderToResponse(LoginRoute, {
      params: { locale: 'es' }, request: new Request('http://localhost/es/login?next=%2Fes%2Flibrary')
    }));
    const register = await mainOf(await app.renderToResponse(RegisterRoute, {
      params: { locale: 'es' }, request: new Request('http://localhost/es/register?next=%2Fes%2Flibrary')
    }));

    expect(login.querySelector('a[href="/es/register?next=%2Fes%2Flibrary"]')?.textContent).toBe('Crear una cuenta');
    expect(register.querySelector('a[href="/es/login?next=%2Fes%2Flibrary"]')?.textContent).toBe('Iniciar sesión');
  });
});
