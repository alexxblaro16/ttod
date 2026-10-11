import React, { useRef, useState } from 'react';

import { buildPayload, validateProposal } from '../lib/proposeForm';
import type { ProposalLevel, ProposeFormErrors, ProposeFormFields } from '../lib/proposeForm';
import { submitProposal } from '../lib/proposals';

interface Props { lang: 'en' | 'es' }

type SubmitState = 'idle' | 'submitting' | 'success' | 'error';

const EMPTY_FIELDS: ProposeFormFields = { text: '', section: '', source: '', level: 'intermediate', tags: '', teaches: '' };
const LEVELS: ProposalLevel[] = ['beginner', 'intermediate', 'advanced', 'master'];

const copyFor = (lang: 'en' | 'es') => lang === 'es'
  ? {
      text: 'Texto de la cita', section: 'Sección', source: 'Fuente (opcional)',
      level: 'Nivel', tags: 'Etiquetas (separadas por comas, opcional)', teaches: 'Qué enseña (opcional)',
      levels: { beginner: 'Principiante', intermediate: 'Intermedio', advanced: 'Avanzado', master: 'Maestro' },
      submit: 'Proponer', submitting: 'Enviando…',
      success: 'Propuesta enviada. Pendiente de revisión.',
      errors: {
        unauthenticated: 'Tu sesión ha caducado. Inicia sesión de nuevo.',
        validation: 'El servidor ha rechazado la propuesta. Revisa los campos.',
        network: 'No se ha podido conectar con el servidor. Comprueba tu conexión.',
        'not-found': 'El endpoint de propuestas todavía no está disponible.',
        server: 'Algo ha fallado al guardar la propuesta. Inténtalo de nuevo más tarde.',
      },
    }
  : {
      text: 'Quote text', section: 'Section', source: 'Source (optional)',
      level: 'Level', tags: 'Tags (comma-separated, optional)', teaches: 'What it teaches (optional)',
      levels: { beginner: 'Beginner', intermediate: 'Intermediate', advanced: 'Advanced', master: 'Master' },
      submit: 'Propose', submitting: 'Submitting…',
      success: 'Proposal submitted. Pending review.',
      errors: {
        unauthenticated: 'Your session has expired. Please log in again.',
        validation: 'The server rejected the proposal. Check the fields.',
        network: 'Could not reach the server. Check your connection.',
        'not-found': 'The proposals endpoint is not available yet.',
        server: 'Something went wrong saving the proposal. Please try again later.',
      },
    };

export default function ProposeForm({ lang }: Props) {
  const copy = copyFor(lang);
  const [fields, setFields] = useState<ProposeFormFields>(EMPTY_FIELDS);
  const [errors, setErrors] = useState<ProposeFormErrors>({});
  const [state, setState] = useState<SubmitState>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const textRef = useRef<HTMLTextAreaElement>(null);
  const sectionRef = useRef<HTMLInputElement>(null);
  const sourceRef = useRef<HTMLInputElement>(null);
  const teachesRef = useRef<HTMLTextAreaElement>(null);

  const field = (key: keyof ProposeFormFields) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) => setFields((prev) => ({ ...prev, [key]: e.target.value }));

  const onSubmit = async (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();
    const found = validateProposal(fields, lang);
    setErrors(found);
    if (Object.keys(found).length > 0) {
      // Focus the first field with an error, in the same order the fields appear in the DOM.
      const firstInvalid = found.text ? textRef : found.section ? sectionRef : found.source ? sourceRef : teachesRef;
      firstInvalid.current?.focus();
      return; // no network call when validation fails
    }

    setState('submitting');
    const result = await submitProposal(buildPayload(fields, lang));
    if (result.ok) {
      setState('success');
    } else {
      setState('error');
      setErrorMessage(copy.errors[result.reason]);
    }
  };

  if (state === 'success') {
    return <p role="status" aria-live="polite">{copy.success}</p>;
  }

  return (
    <form onSubmit={onSubmit} noValidate>
      <p>
        <label htmlFor="propose-text">{copy.text}</label><br />
        <textarea
          id="propose-text" ref={textRef} value={fields.text} onChange={field('text')}
          aria-describedby={errors.text ? 'propose-text-error' : undefined}
          aria-invalid={errors.text ? true : undefined}
        />
        {errors.text && <span id="propose-text-error" role="alert">{errors.text}</span>}
      </p>
      <p>
        <label htmlFor="propose-section">{copy.section}</label><br />
        <input
          id="propose-section" ref={sectionRef} type="text" value={fields.section} onChange={field('section')}
          aria-describedby={errors.section ? 'propose-section-error' : undefined}
          aria-invalid={errors.section ? true : undefined}
        />
        {errors.section && <span id="propose-section-error" role="alert">{errors.section}</span>}
      </p>
      <p>
        <label htmlFor="propose-source">{copy.source}</label><br />
        <input
          id="propose-source" ref={sourceRef} type="text" value={fields.source} onChange={field('source')}
          aria-describedby={errors.source ? 'propose-source-error' : undefined}
        />
        {errors.source && <span id="propose-source-error" role="alert">{errors.source}</span>}
      </p>
      <p>
        <label htmlFor="propose-level">{copy.level}</label><br />
        <select id="propose-level" value={fields.level} onChange={field('level')}>
          {LEVELS.map((level) => <option key={level} value={level}>{copy.levels[level]}</option>)}
        </select>
      </p>
      <p>
        <label htmlFor="propose-tags">{copy.tags}</label><br />
        <input id="propose-tags" type="text" value={fields.tags} onChange={field('tags')} />
      </p>
      <p>
        <label htmlFor="propose-teaches">{copy.teaches}</label><br />
        <textarea
          id="propose-teaches" ref={teachesRef} value={fields.teaches} onChange={field('teaches')}
          aria-describedby={errors.teaches ? 'propose-teaches-error' : undefined}
        />
        {errors.teaches && <span id="propose-teaches-error" role="alert">{errors.teaches}</span>}
      </p>
      <button type="submit" disabled={state === 'submitting'}>
        {state === 'submitting' ? copy.submitting : copy.submit}
      </button>
      {state === 'error' && <p role="alert" aria-live="polite">{errorMessage}</p>}
    </form>
  );
}
