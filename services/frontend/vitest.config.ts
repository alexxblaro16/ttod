/// <reference types="vitest/config" />
import { getViteConfig } from 'astro/config';

// getViteConfig (not a bare defineConfig) so vitest can resolve `.astro` imports: component tests
// render real .astro files through Astro's container API.
export default getViteConfig({
  test: {
    exclude: [
      'node_modules/**',
      'dist/**',
      'e2e/**',
      'src/components/graph/layout.test.mjs'
    ]
  }
});
