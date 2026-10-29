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
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, status: 201 });
    vi.stubGlobal('fetch', fetchMock);
    const user = userEvent.setup();
    render(<FavoriteButton quoteId="wis-001" initiallySaved={false} />);

    await user.click(screen.getByRole('button', { name: 'Save to favorites (wis-001)' }));

    const removeButton = await screen.findByRole('button', { name: 'Remove from favorites (wis-001)' });
    expect(fetchMock).toHaveBeenNthCalledWith(1, '/api/v1/favorites', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ quoteId: 'wis-001' }),
    });

    await user.click(removeButton);

    expect(await screen.findByRole('button', { name: 'Save to favorites (wis-001)' })).toBeInTheDocument();
    expect(fetchMock).toHaveBeenNthCalledWith(2, '/api/v1/favorites/wis-001', {
      method: 'DELETE',
      headers: undefined,
      body: undefined,
    });
  });

  it('starts its accessible name with the visible text (WCAG 2.5.3) and is not a toggle', () => {
    render(<FavoriteButton quoteId="wis-001" initiallySaved={false} />);
    const button = screen.getByRole('button');

    expect(button.getAttribute('aria-label')?.startsWith(button.textContent ?? '')).toBe(true);
    expect(button).not.toHaveAttribute('aria-pressed');
  });

  it('speaks Spanish on Spanish pages', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, status: 201 }));
    const user = userEvent.setup();
    render(<FavoriteButton quoteId="wis-001" initiallySaved={false} locale="es" />);

    await user.click(screen.getByRole('button', { name: 'Guardar en favoritos (wis-001)' }));

    expect(await screen.findByRole('button', { name: 'Quitar de favoritos (wis-001)' })).toHaveTextContent('Quitar de favoritos');
    expect(screen.getByRole('status')).toHaveTextContent('Cita guardada en tu biblioteca.');
  });

  it('can be operated with the keyboard alone and keeps focus while saving', async () => {
    let answer: (value: { ok: boolean; status: number }) => void = () => undefined;
    const fetchMock = vi.fn().mockReturnValue(new Promise((resolve) => { answer = resolve; }));
    vi.stubGlobal('fetch', fetchMock);
    const user = userEvent.setup();
    render(<FavoriteButton quoteId="wis-001" initiallySaved={false} />);

    await user.tab();
    const button = screen.getByRole('button', { name: 'Save to favorites (wis-001)' });
    expect(button).toHaveFocus();
    await user.keyboard('{Enter}');

    // Mientras espera al backend el botón sigue enfocado y un segundo Enter no repite la petición.
    expect(button).toHaveAttribute('aria-disabled', 'true');
    expect(button).toHaveFocus();
    await user.keyboard('{Enter}');
    expect(fetchMock).toHaveBeenCalledTimes(1);

    answer({ ok: true, status: 201 });
    expect(await screen.findByRole('button', { name: 'Remove from favorites (wis-001)' })).toHaveFocus();
    expect(screen.getByRole('status')).toHaveTextContent('Quote saved to your library.');
  });

  it('keeps the saved state and announces the failure when the service fails', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 503 }));
    const user = userEvent.setup();
    render(<FavoriteButton quoteId="wis-001" />);

    await user.click(screen.getByRole('button', { name: 'Remove from favorites (wis-001)' }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Your favorites could not be updated. Please try again.');
    expect(screen.getByRole('button', { name: 'Remove from favorites (wis-001)' })).toBeInTheDocument();
    expect(screen.getByRole('status')).toBeEmptyDOMElement();
  });

  it('tells the user to log in again when the session has expired', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 401 }));
    const user = userEvent.setup();
    render(<FavoriteButton quoteId="wis-001" locale="es" />);

    await user.click(screen.getByRole('button', { name: 'Quitar de favoritos (wis-001)' }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Tu sesión ha caducado. Vuelve a entrar para cambiar tus favoritos.');
    expect(screen.getByRole('button', { name: 'Quitar de favoritos (wis-001)' })).toBeInTheDocument();
  });
});
