// Pure functions, no DOM/network: easy to unit-test, and the one place that knows the exact shape
// of the real backend contract (PR #57's ProposalRequest, extra="forbid" — a field outside this
// shape gets a 422 once the real endpoint is live, so buildPayload() must never add one).

export type ProposalLevel = 'beginner' | 'intermediate' | 'advanced' | 'master';
export type ProposalLang = 'en' | 'es';

export interface ProposeFormFields {
  text: string;
  section: string;
  source: string;
  level: ProposalLevel;
  tags: string; // comma-separated, as typed in the field
  teaches: string;
}

export interface ProposalPayload {
  text: string;
  section: string;
  source?: string;
  level?: ProposalLevel;
  tags?: string[];
  teaches?: string;
  lang: ProposalLang;
}

export type ProposeFormErrors = Partial<Record<keyof ProposeFormFields, string>>;

const LIMITS = { text: 2000, section: 100, source: 2000, teaches: 2000, maxTags: 20 } as const;

export function parseTags(raw: string): string[] {
  return [...new Set(raw.split(',').map((tag) => tag.trim()).filter(Boolean))].slice(0, LIMITS.maxTags);
}

export function validateProposal(fields: ProposeFormFields, lang: ProposalLang): ProposeFormErrors {
  const errors: ProposeFormErrors = {};
  const copy = lang === 'es'
    ? {
        textRequired: 'Escribe el texto de la cita.', textTooLong: `Máximo ${LIMITS.text} caracteres.`,
        sectionRequired: 'Indica una sección.', sectionTooLong: `Máximo ${LIMITS.section} caracteres.`,
        sourceTooLong: `Máximo ${LIMITS.source} caracteres.`, teachesTooLong: `Máximo ${LIMITS.teaches} caracteres.`,
      }
    : {
        textRequired: 'Write the text of the quote.', textTooLong: `Maximum ${LIMITS.text} characters.`,
        sectionRequired: 'Enter a section.', sectionTooLong: `Maximum ${LIMITS.section} characters.`,
        sourceTooLong: `Maximum ${LIMITS.source} characters.`, teachesTooLong: `Maximum ${LIMITS.teaches} characters.`,
      };

  const text = fields.text.trim();
  if (!text) errors.text = copy.textRequired;
  else if (text.length > LIMITS.text) errors.text = copy.textTooLong;

  const section = fields.section.trim();
  if (!section) errors.section = copy.sectionRequired;
  else if (section.length > LIMITS.section) errors.section = copy.sectionTooLong;

  if (fields.source.trim().length > LIMITS.source) errors.source = copy.sourceTooLong;
  if (fields.teaches.trim().length > LIMITS.teaches) errors.teaches = copy.teachesTooLong;

  return errors;
}

export function buildPayload(fields: ProposeFormFields, lang: ProposalLang): ProposalPayload {
  const payload: ProposalPayload = { text: fields.text.trim(), section: fields.section.trim(), lang };
  const source = fields.source.trim();
  if (source) payload.source = source;
  if (fields.level !== 'intermediate') payload.level = fields.level;
  const tags = parseTags(fields.tags);
  if (tags.length) payload.tags = tags;
  const teaches = fields.teaches.trim();
  if (teaches) payload.teaches = teaches;
  return payload;
}
