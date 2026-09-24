import { useState } from 'react';

interface FavoriteButtonProps {
  quoteId: string;
  initiallySaved?: boolean;
}

export default function FavoriteButton({ quoteId, initiallySaved = true }: FavoriteButtonProps) {
  const [saved, setSaved] = useState(initiallySaved);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);

  async function toggleFavorite() {
    if (busy) return;
    setBusy(true);
    setError(false);
    try {
      const response = await fetch(`/api/v1/favorites${saved ? `/${encodeURIComponent(quoteId)}` : ''}`, {
        method: saved ? 'DELETE' : 'POST',
        headers: saved ? undefined : { 'content-type': 'application/json' },
        body: saved ? undefined : JSON.stringify({ quoteId }),
      });
      if (!response.ok) throw new Error(`Favorite request failed (${response.status})`);
      setSaved(!saved);
    } catch {
      setError(true);
    } finally {
      setBusy(false);
    }
  }

  return (
    <span>
      <button
        type="button"
        aria-label={`${saved ? 'Remove quote' : 'Save quote'} ${quoteId} ${saved ? 'from' : 'to'} favorites`}
        aria-pressed={saved}
        disabled={busy}
        onClick={toggleFavorite}
      >
        {saved ? 'Saved to favorites' : 'Save to favorites'}
      </button>
      {error && <span role="alert"> Unable to update favorites.</span>}
    </span>
  );
}