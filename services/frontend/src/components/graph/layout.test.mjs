import assert from 'node:assert/strict';
import test from 'node:test';
import { filterGraph, joinTags, radialLayout, sectionColor, sectionColorKey, sectionLabel, selectedTag } from './layout.ts';

const nodes = [{ id: 'a-001', section: 'a', origin: 'blackbox', status: 'active', text: 'A', lang: 'en' }, { id: 'b-001', section: 'b', origin: 'human', status: 'active', text: 'B', lang: 'en' }];
const wisdom = [{ ...nodes[0], level: 'beginner', teaches: '', tags: ['focus'], related: [], rights: { license: 'CC-BY-NC-SA-4.0' } }];
const edges = [{ source: 'a-001', target: 'b-001', rel: 'related' }];

test('joins tags and filters the induced edge set', () => {
  const joined = joinTags(nodes, wisdom);
  const filtered = filterGraph(joined, edges, 'focus');
  assert.deepEqual(filtered.nodes.map((node) => node.id), ['a-001']);
  assert.equal(filtered.edges.length, 0);
});

test('matches any tag without duplicating nodes and preserves tagless nodes', () => {
  const multiTagNodes = [
    { id: 'a-001', section: 'a', origin: 'human', status: 'active', text: 'A', lang: 'en' },
    { id: 'b-001', section: 'b', origin: 'human', status: 'active', text: 'B', lang: 'en' }
  ];
  const multiTagWisdom = [
    { ...multiTagNodes[0], level: 'beginner', teaches: '', tags: ['focus', 'shared'], related: [], rights: { license: 'CC-BY-NC-SA-4.0' } },
    { ...multiTagNodes[1], level: 'beginner', teaches: '', tags: [], related: [], rights: { license: 'CC-BY-NC-SA-4.0' } }
  ];
  const joined = joinTags(multiTagNodes, multiTagWisdom);
  assert.deepEqual(joined.map((node) => node.tags), [['focus', 'shared'], []]);
  assert.deepEqual(filterGraph(joined, [], 'shared').nodes.map((node) => node.id), ['a-001']);
  assert.deepEqual(filterGraph(joined, [], '').nodes.map((node) => node.id), ['a-001', 'b-001']);
});

test('uses governed section colors and a visible fallback for unknown sections', () => {
  assert.equal(sectionColorKey('architecture'), 'architecture');
  assert.equal(sectionColor('architecture'), '#0d9488');
  assert.equal(sectionLabel('architecture'), 'Architecture & Modularization');
  assert.equal(sectionColorKey('future-section'), 'fallback');
  assert.equal(sectionColor('future-section'), '#777');
  assert.equal(sectionLabel('future-section'), 'future-section');
});

test('layout is deterministic and URL state reads only tag', () => {
  const joined = joinTags(nodes, wisdom);
  assert.deepEqual(radialLayout(joined), radialLayout(joined));
  assert.equal(selectedTag('?tag=focus&ignored=yes'), 'focus');
});

test('layout preserves every node when a section contains many nodes', () => {
  const largeNodes = Array.from({ length: 2000 }, (_, index) => ({
    id: `a-${String(index).padStart(4, '0')}`,
    section: 'a',
    origin: 'human',
    status: 'active',
    text: `Node ${index}`,
    lang: 'en',
    tags: []
  }));
  const positioned = radialLayout(largeNodes);
  assert.equal(positioned.length, largeNodes.length);
  assert.deepEqual(positioned.map((node) => node.id).sort(), largeNodes.map((node) => node.id).sort());
});
