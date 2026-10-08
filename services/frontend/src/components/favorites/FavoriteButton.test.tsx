// @vitest-environment jsdom
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom/vitest';
// Vitest compila el JSX con el runtime clásico, que necesita React en el ámbito.
import React from 'react';

import FavoriteButton from './FavoriteButton';

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe('FavoriteButton', () => {
  it('saves and then removes a quote through the favorites API', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true });
    vi.stubGlobal('fetch', fetchMock);
    const user = userEvent.setup();
    render(<FavoriteButton quoteId="wis-001" initiallySaved={false} />);

    await user.click(screen.getByRole('button', { name: 'Save quote wis-001 to favorites' }));

    const removeButton = await screen.findByRole('button', { name: 'Remove quote wis-001 from favorites' });
    expect(removeButton).toHaveAttribute('aria-pressed', 'true');
    expect(fetchMock).toHaveBeenNthCalledWith(1, '/api/v1/favorites', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ quoteId: 'wis-001' }),
    });

    await user.click(removeButton);

    const saveButton = await screen.findByRole('button', { name: 'Save quote wis-001 to favorites' });
    expect(saveButton).toHaveAttribute('aria-pressed', 'false');
    expect(fetchMock).toHaveBeenNthCalledWith(2, '/api/v1/favorites/wis-001', {
      method: 'DELETE',
      headers: undefined,
      body: undefined,
    });
  });

  it('can be operated with the keyboard alone', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true });
    vi.stubGlobal('fetch', fetchMock);
    const user = userEvent.setup();
    render(<FavoriteButton quoteId="wis-001" initiallySaved={false} />);

    await user.tab();
    expect(screen.getByRole('button', { name: 'Save quote wis-001 to favorites' })).toHaveFocus();
    await user.keyboard('{Enter}');

    expect(await screen.findByRole('button', { name: 'Remove quote wis-001 from favorites' })).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('keeps the saved state and announces the failure when the session is rejected', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 401 }));
    const user = userEvent.setup();
    render(<FavoriteButton quoteId="wis-001" />);

    await user.click(screen.getByRole('button', { name: 'Remove quote wis-001 from favorites' }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Unable to update favorites.');
    expect(screen.getByRole('button', { name: 'Remove quote wis-001 from favorites' })).toHaveAttribute(
      'aria-pressed',
      'true'
    );
  });
});
