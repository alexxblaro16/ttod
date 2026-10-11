import { describe, expect, it, vi } from 'vitest';

import { loadWisdom } from '../content/wisdom';

describe('loadWisdom', () => {
  it('passes entries through unchanged on success', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue(new Response(JSON.stringify([{ id: 'a', lang: 'en' }]), { status: 200 }));
    const result = await loadWisdom('en');
    expect(result).toEqual({ entries: [{ id: 'a', lang: 'en' }], failed: false });
    vi.restoreAllMocks();
  });

  it('catches a non-OK response and reports failed, never throwing', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue(new Response(null, { status: 500 }));
    const result = await loadWisdom('en');
    expect(result).toEqual({ entries: [], failed: true });
    vi.restoreAllMocks();
  });

  it('catches a network failure and reports failed, never throwing', async () => {
    vi.spyOn(global, 'fetch').mockRejectedValue(new Error('network down'));
    await expect(loadWisdom('en')).resolves.toEqual({ entries: [], failed: true });
    vi.restoreAllMocks();
  });
});
