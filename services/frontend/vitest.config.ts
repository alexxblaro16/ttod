import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    exclude: [
      'node_modules/**',
      'dist/**',
      'e2e/**',
      'src/components/graph/layout.test.mjs'
    ]
  }
});
