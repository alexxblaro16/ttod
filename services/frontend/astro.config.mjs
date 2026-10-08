import { defineConfig } from 'astro/config';
import node from '@astrojs/node';
import mdx from '@astrojs/mdx';
import react from '@astrojs/react';
import svelte from '@astrojs/svelte';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  output: 'server',
  adapter: node({ mode: 'standalone' }),
  integrations: [mdx(), react(), svelte()],
  i18n: {
    locales: ['en', 'es'],
    defaultLocale: 'en',
    routing: { prefixDefaultLocale: true }
  },
  server: { host: true, port: 4321 },
  // El formulario de login hace POST: sin esto el build de Node no confía en la cabecera Host,
  // toma el origen como `http://localhost` sin puerto y rechaza con 403 el POST del stack local.
  security: { allowedDomains: [{ hostname: 'localhost' }, { hostname: '127.0.0.1' }] },
  vite: { plugins: [tailwindcss()] }
});
