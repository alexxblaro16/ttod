import React, { useState } from 'react';

interface FavoriteButtonProps {
  quoteId: string;
  initiallySaved?: boolean;
  locale?: 'en' | 'es';
}

const COPY = {
  en: {
    save: 'Save to favorites',
    remove: 'Remove from favorites',
    saved: 'Quote saved to your library.',
    removed: 'Quote removed from your library.',
    expired: 'Your session has expired. Log in again to update your favorites.',
    failed: 'Your favorites could not be updated. Please try again.',
  },
  es: {
    save: 'Guardar en favoritos',
    remove: 'Quitar de favoritos',
    saved: 'Cita guardada en tu biblioteca.',
    removed: 'Cita quitada de tu biblioteca.',
    expired: 'Tu sesión ha caducado. Vuelve a entrar para cambiar tus favoritos.',
    failed: 'No se han podido actualizar tus favoritos. Inténtalo de nuevo.',
  },
} as const;

export default function FavoriteButton({ quoteId, initiallySaved = true, locale = 'en' }: FavoriteButtonProps) {
  const copy = COPY[locale];
  const [saved, setSaved] = useState(initiallySaved);
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');

  async function toggleFavorite() {
    if (busy) return;
    setBusy(true);
    setStatus('');
    setError('');
    try {
      const response = await fetch(`/api/v1/favorites${saved ? `/${encodeURIComponent(quoteId)}` : ''}`, {
        method: saved ? 'DELETE' : 'POST',
        headers: saved ? undefined : { 'content-type': 'application/json' },
        body: saved ? undefined : JSON.stringify({ quoteId }),
      });
      if (response.status === 401) {
        setError(copy.expired);
        return;
      }
      if (!response.ok) throw new Error(`Favorite request failed (${response.status})`);
      setStatus(saved ? copy.removed : copy.saved);
      setSaved(!saved);
    } catch {
      setError(copy.failed);
    } finally {
      setBusy(false);
    }
  }

  const label = saved ? copy.remove : copy.save;
  // El nombre accesible empieza por el texto visible (WCAG 2.5.3) y añade el id para
  // distinguir los botones de la biblioteca. Como la etiqueta ya dice la acción, no se
  // usa aria-pressed: un conmutador con etiqueta cambiante se anunciaría dos veces.
  // aria-disabled en vez de disabled: mientras guarda, el foco no se pierde.
  return (
    <span>
      <button type="button" aria-label={`${label} (${quoteId})`} aria-disabled={busy} onClick={toggleFavorite}>
        {label}
      </button>
      {/* Las regiones existen desde el principio para que el lector de pantalla las anuncie. */}
      <span role="status">{status}</span>
      <span role="alert">{error}</span>
    </span>
  );
}
