import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { loadRenderers } from 'astro:container';
import { getContainerRenderer } from '@astrojs/react';
import { JSDOM } from 'jsdom';
import { describe, expect, it } from 'vitest';

import ProposeRoute from '../pages/[locale]/wisdom/propose.astro';

const render = async (path: string, params: Record<string, string>, headers: Record<string, string> = {}) => {
  const renderers = await loadRenderers([getContainerRenderer()]);
  const container = await AstroContainer.create({ renderers });
  const html = await container.renderToString(ProposeRoute, {
    params, request: new Request(`http://localhost${path}`, { headers }),
  });
  const main = new JSDOM(html).window.document.querySelector('main');
  if (!main) throw new Error('route rendered no <main>');
  return main;
};

describe('propose page session gate', () => {
  it('without a session: shows the translated login prompt, no form in the markup', async () => {
    const main = await render('/en/wisdom/propose/', { locale: 'en' });
    expect(main.textContent).toContain('Log in to propose a quote.');
    expect(main.querySelector('form')).toBeNull();
    expect(main.querySelector('a[href="/en/login/"]')).not.toBeNull();
  });

  it('with a session cookie: renders the ProposeForm mount point, not the login prompt', async () => {
    const cookie = `ttod_session=${encodeURIComponent(JSON.stringify({ userId: 'demo-student' }))}`;
    const main = await render('/en/wisdom/propose/', { locale: 'en' }, { cookie });
    expect(main.textContent).not.toContain('Log in to propose a quote.');
    expect(main.querySelector('astro-island')).not.toBeNull();
  });

  it('es: the login prompt is translated', async () => {
    const main = await render('/es/wisdom/propose/', { locale: 'es' });
    expect(main.textContent).toContain('Inicia sesión para proponer una cita.');
  });
});
