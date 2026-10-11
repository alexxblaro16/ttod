import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { JSDOM } from 'jsdom';
import { afterEach, describe, expect, it, vi } from 'vitest';

import type { WisdomEntry } from '../types/domain';

import IndexRoute from '../pages/[locale]/wisdom/index.astro';
import SlugRoute from '../pages/[locale]/wisdom/[slug].astro';
import SectionRoute from '../pages/[locale]/wisdom/sections/[section].astro';

const entry: WisdomEntry = {
  id: 'arch-001', section: 'architecture', level: 'advanced', tags: ['boundaries'],
  text: 'The module that knows its boundaries serves the whole.',
  teaches: 'Boundaries', related: [], origin: 'human', lang: 'en',
  rights: { license: 'CC-BY-NC-SA-4.0', holder: 'ruvebal@crea-comm.net' },
};

// These tests mock the global fetch() call, not the content/wisdom module: loadWisdom() calls
// fetchWisdom() as a same-module reference, which vi.mock('../content/wisdom', ...) cannot
// intercept (it only replaces what OTHER modules import, not wisdom.ts's own internal call).
// Mocking fetch is also the more honest test — it exercises loadWisdom's real try/catch against
// the actual failure surface (network/response), the same thing load-wisdom.test.ts covers in
// isolation.
const mockFetchOk = (payload: unknown) => vi.spyOn(global, 'fetch').mockResolvedValue(new Response(JSON.stringify(payload), { status: 200 }));
const mockFetchDown = () => vi.spyOn(global, 'fetch').mockRejectedValue(new Error('network down'));

afterEach(() => vi.restoreAllMocks());

const render = async (Route: Parameters<AstroContainer['renderToString']>[0], path: string, params: Record<string, string>) => {
  const container = await AstroContainer.create();
  const html = await container.renderToString(Route, { params, request: new Request(`http://localhost${path}`) });
  const main = new JSDOM(html).window.document.querySelector('main');
  if (!main) throw new Error('route rendered no <main>');
  return main;
};

describe('empty and error states never leave a blank page or a stack trace', () => {
  it('index: zero entries -> translated empty state, no crash', async () => {
    mockFetchOk([]);
    const main = await render(IndexRoute, '/en/wisdom/', { locale: 'en' });
    expect(main.querySelector('.ttod-empty h2')?.textContent).toBe('Nothing here yet');
    expect(main.querySelector('.ttod-empty p')?.textContent).toBe('No accepted English wisdom is available yet.');
    expect(main.querySelector('.ttod-empty')?.getAttribute('role')).toBeNull();
  });

  it('index: a failing fetch -> translated error state with role=alert, no stack trace', async () => {
    mockFetchDown();
    const main = await render(IndexRoute, '/en/wisdom/', { locale: 'en' });
    expect(main.textContent).not.toContain('Error:');
    expect(main.textContent).not.toContain('network down');
    expect(main.querySelector('.ttod-empty h2')?.textContent).toBe('Something went wrong');
    expect(main.querySelector('.ttod-empty')?.getAttribute('role')).toBe('alert');
  });

  it('index: real data renders exactly as before (no regression)', async () => {
    mockFetchOk([entry]);
    const main = await render(IndexRoute, '/en/wisdom/', { locale: 'en' });
    expect(main.querySelector('.ttod-empty')).toBeNull();
    expect(main.querySelector('article.ttod-card blockquote')?.textContent).toBe(entry.text);
  });

  it('detail: unknown slug -> "not found" state (not the generic empty copy) with a back link', async () => {
    mockFetchOk([entry]);
    const main = await render(SlugRoute, '/en/wisdom/does-not-exist/', { locale: 'en', slug: 'does-not-exist' });
    expect(main.querySelector('.ttod-empty h2')?.textContent).toBe('Wisdom entry not found');
    expect(main.querySelector('.ttod-empty p')?.textContent).not.toBe('No accepted English wisdom is available yet.');
    expect(main.querySelector('.ttod-empty a')?.getAttribute('href')).toBe('/en/wisdom/');
    expect(main.querySelector('.ttod-empty')?.getAttribute('role')).toBeNull();
  });

  it('detail: a failing fetch -> translated error state, no stack trace', async () => {
    mockFetchDown();
    const main = await render(SlugRoute, '/en/wisdom/arch-001/', { locale: 'en', slug: 'arch-001' });
    expect(main.textContent).not.toContain('network down');
    expect(main.querySelector('.ttod-empty')?.getAttribute('role')).toBe('alert');
  });

  it('detail: existing slug renders exactly as before (no regression)', async () => {
    mockFetchOk([entry]);
    const main = await render(SlugRoute, '/en/wisdom/arch-001/', { locale: 'en', slug: 'arch-001' });
    expect(main.querySelector('article.ttod-card blockquote')?.textContent).toBe(entry.text);
  });

  it('facet route: zero matches -> translated empty state; a failing fetch -> translated error state', async () => {
    mockFetchOk([entry]);
    const empty = await render(SectionRoute, '/en/wisdom/sections/no-such-section/', { locale: 'en', section: 'no-such-section' });
    expect(empty.querySelector('.ttod-empty h2')?.textContent).toBe('Nothing here yet');

    mockFetchDown();
    const errored = await render(SectionRoute, '/en/wisdom/sections/architecture/', { locale: 'en', section: 'architecture' });
    expect(errored.textContent).not.toContain('network down');
    expect(errored.querySelector('.ttod-empty')?.getAttribute('role')).toBe('alert');
  });

  it('es locale: both states are translated, not left in English', async () => {
    mockFetchOk([]);
    const empty = await render(IndexRoute, '/es/wisdom/', { locale: 'es' });
    expect(empty.querySelector('.ttod-empty h2')?.textContent).toBe('Todavía nada aquí');

    mockFetchDown();
    const errored = await render(IndexRoute, '/es/wisdom/', { locale: 'es' });
    expect(errored.querySelector('.ttod-empty h2')?.textContent).toBe('Algo ha fallado');
  });
});
