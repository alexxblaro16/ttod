import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import React from 'react';

import FavoriteButton from './FavoriteButton';

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe('FavoriteButton', () => {
  it('saves and removes a quote through the favorites API', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true });
    vi.stubGlobal('fetch', fetchMock);

    render(<FavoriteButton quoteId="wis-001" initiallySaved={false} />);

    fireEvent.click(screen.getByRole('button', { name: 'Save quote wis-001 to favorites' }));
    const removeButton = await screen.findByRole('button', {
      name: 'Remove quote wis-001 from favorites',
    });
    expect(removeButton).toHaveAttribute('aria-pressed', 'true');
    expect(fetchMock).toHaveBeenNthCalledWith(1, '/api/v1/favorites', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ quoteId: 'wis-001' }),
    });

    fireEvent.click(removeButton);
    const saveButton = await screen.findByRole('button', {
      name: 'Save quote wis-001 to favorites',
    });
    expect(saveButton).toHaveAttribute('aria-pressed', 'false');
    expect(fetchMock).toHaveBeenNthCalledWith(2, '/api/v1/favorites/wis-001', {
      method: 'DELETE',
      headers: undefined,
      body: undefined,
    });
  });

  it('keeps the saved state and announces an API failure', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 500 }));
    render(<FavoriteButton quoteId="wis-001" />);

    fireEvent.click(screen.getByRole('button', {
      name: 'Remove quote wis-001 from favorites',
    }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Unable to update favorites.');
    expect(screen.getByRole('button', {
      name: 'Remove quote wis-001 from favorites',
    })).toHaveAttribute('aria-pressed', 'true');
  });
});
