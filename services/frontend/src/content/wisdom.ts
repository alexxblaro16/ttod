import type { WisdomEntry } from '../types/domain';

export type Locale = 'en' | 'es';

export const isLocale = (value: string | undefined): value is Locale => value === 'en' || value === 'es';

export async function fetchWisdom(locale: Locale): Promise<WisdomEntry[]> {
  const backend = import.meta.env.BACKEND_URL ?? 'http://localhost:8000';
  const response = await fetch(`${backend}/api/v1/wisdom/sample`, { headers: { accept: 'application/json' } });
  if (!response.ok) throw new Error(`Backend wisdom request failed (${response.status})`);
  const payload: unknown = await response.json();
  if (!Array.isArray(payload)) throw new Error('Backend wisdom response is not an array');
  return (payload as WisdomEntry[]).filter((entry) => entry.lang === locale);
}

export const quoteSlug = (entry: WisdomEntry) => entry.id;

export const labels = {
  en: {
    wisdom: 'Wisdom', docs: 'Documentation', empty: 'No accepted English wisdom is available yet.',
    sections: 'Sections', levels: 'Levels', tags: 'Tags', all: 'All wisdom', teaches: 'Teaches',
    back: 'Back to wisdom', entries: 'entries', notFound: 'Wisdom entry not found',
  },
  es: {
    wisdom: 'Sabiduría', docs: 'Documentación', empty: 'Todavía no hay sabiduría aceptada en español.',
    sections: 'Secciones', levels: 'Niveles', tags: 'Etiquetas', all: 'Toda la sabiduría', teaches: 'Enseña',
    back: 'Volver a sabiduría', entries: 'entradas', notFound: 'Entrada de sabiduría no encontrada',
  },
} as const;

export function frequencies(entries: WisdomEntry[], field: 'section' | 'level' | 'tags') {
  const counts = new Map<string, number>();
  for (const entry of entries) {
    const values = field === 'tags' ? entry.tags : [entry[field]];
    for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  }
  return [...counts].sort(([left], [right]) => left.localeCompare(right));
}

