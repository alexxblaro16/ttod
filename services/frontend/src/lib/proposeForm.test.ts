import { describe, expect, it } from 'vitest';

import { buildPayload, parseTags, validateProposal } from './proposeForm';
import type { ProposeFormFields } from './proposeForm';

const EMPTY: ProposeFormFields = { text: '', section: '', source: '', level: 'intermediate', tags: '', teaches: '' };
const VALID: ProposeFormFields = {
  text: 'Simplicity is the final sophistication.', section: 'wisdom', source: 'student observation',
  level: 'advanced', tags: 'simplicity, design , simplicity', teaches: 'Prefer the smallest useful change.',
};

describe('validateProposal', () => {
  it('requires text and section', () => {
    const errors = validateProposal(EMPTY, 'en');
    expect(errors.text).toBeTruthy();
    expect(errors.section).toBeTruthy();
  });

  it('passes with no errors when text and section are present', () => {
    expect(validateProposal(VALID, 'en')).toEqual({});
  });

  it('rejects text over the 2000-character contract limit', () => {
    const errors = validateProposal({ ...VALID, text: 'a'.repeat(2001) }, 'en');
    expect(errors.text).toBeTruthy();
  });

  it('rejects a section over the 100-character contract limit', () => {
    const errors = validateProposal({ ...VALID, section: 'a'.repeat(101) }, 'en');
    expect(errors.section).toBeTruthy();
  });

  it('treats whitespace-only text as empty', () => {
    expect(validateProposal({ ...VALID, text: '   ' }, 'en').text).toBeTruthy();
  });

  it('translates messages to es', () => {
    const errors = validateProposal(EMPTY, 'es');
    expect(errors.text).toMatch(/cita/);
  });
});

describe('parseTags', () => {
  it('trims, dedupes and drops empty entries', () => {
    expect(parseTags('simplicity, design , simplicity,, ')).toEqual(['simplicity', 'design']);
  });

  it('caps at the contract\'s 20-tag limit', () => {
    const many = Array.from({ length: 25 }, (_, i) => `tag${i}`).join(',');
    expect(parseTags(many)).toHaveLength(20);
  });
});

describe('buildPayload', () => {
  it('matches the real contract exactly: only the fields PR #57 accepts, nothing extra', () => {
    const payload = buildPayload(VALID, 'en');
    expect(Object.keys(payload).sort()).toEqual(['lang', 'level', 'section', 'source', 'tags', 'teaches', 'text']);
    expect(payload).toEqual({
      text: VALID.text, section: 'wisdom', source: 'student observation',
      level: 'advanced', tags: ['simplicity', 'design'], teaches: VALID.teaches, lang: 'en',
    });
  });

  it('omits optional empty fields rather than sending them blank', () => {
    const payload = buildPayload({ ...EMPTY, text: 'x', section: 'y' }, 'en');
    expect(payload).toEqual({ text: 'x', section: 'y', lang: 'en' });
  });

  it('never includes a field outside the contract (would 422 once the real endpoint is live)', () => {
    const payload = buildPayload(VALID, 'en') as unknown as Record<string, unknown>;
    const allowed = new Set(['text', 'section', 'source', 'level', 'tags', 'teaches', 'lang']);
    for (const key of Object.keys(payload)) expect(allowed.has(key)).toBe(true);
  });
});
