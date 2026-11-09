// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { mount, unmount, type Component } from 'svelte';
import GraphIsland from './GraphIsland.svelte';
import type { GraphNode, WisdomEntry } from '../../types/domain';

const graphNodes: GraphNode[] = [
	{ id: 'arch-001', section: 'architecture', origin: 'human', status: 'active', text: 'Keep boundaries clear.', lang: 'en' },
	{ id: 'wis-001', section: 'wisdom', origin: 'studio', status: 'active', text: 'Question the obvious.', lang: 'en' },
	{ id: 'unknown-001', section: 'new-section', origin: 'legacy-unknown', status: 'active', text: 'Leave room for change.', lang: 'en' }
];

const wisdomEntries: WisdomEntry[] = [
	{ ...graphNodes[0], level: 'beginner', teaches: '', tags: ['boundaries', 'shared'], related: [], rights: { license: 'CC-BY-NC-SA-4.0' } },
	{ ...graphNodes[1], level: 'beginner', teaches: '', tags: [], related: [], rights: { license: 'CC-BY-NC-SA-4.0' } },
	{ ...graphNodes[2], level: 'beginner', teaches: '', tags: ['change'], related: [], rights: { license: 'CC-BY-NC-SA-4.0' } }
];

afterEach(() => {
	vi.unstubAllGlobals();
	document.body.replaceChildren();
});

describe('GraphIsland', () => {
	it('renders nodes and updates the accessible details panel when a node is selected', async () => {
		vi.stubGlobal('fetch', vi.fn()
			.mockResolvedValueOnce(new Response(JSON.stringify({ nodes: graphNodes, edges: [] }), { status: 200 }))
			.mockResolvedValueOnce(new Response(JSON.stringify(wisdomEntries), { status: 200 })));

		const target = document.createElement('div');
		document.body.append(target);
		const island = mount(GraphIsland as unknown as Component, { target });

		await vi.waitFor(() => {
			expect(target.querySelectorAll('[data-node-id]')).toHaveLength(graphNodes.length);
		});

		const firstNode = target.querySelector<SVGCircleElement>('[data-node-id="arch-001"]');
		expect(firstNode).not.toBeNull();
		expect(firstNode).toHaveAttribute('role', 'button');
		expect(firstNode).toHaveAttribute('tabindex', '0');
		expect(firstNode).toHaveAttribute(
			'aria-label',
			'arch-001: Keep boundaries clear., section: architecture, origin: human, tags: boundaries, shared'
		);
		expect(target.querySelector('[data-node-id="wis-001"]')).toHaveAttribute(
			'aria-label',
			'wis-001: Question the obvious., section: wisdom, origin: studio'
		);
		expect(target.querySelector('[data-node-id="unknown-001"]')).toHaveAttribute('data-section-color', 'fallback');
		expect(target.querySelector('.legend')).toHaveAccessibleName('Section legend');
		expect(target.querySelector('.legend')).toHaveTextContent('Architecture & Modularization');
		expect(target.querySelector('.legend')).toHaveTextContent('new-section');

		firstNode?.dispatchEvent(new MouseEvent('click', { bubbles: true }));

		await vi.waitFor(() => {
			const details = target.querySelector('aside[aria-label], aside[aria-labelledby]');
			expect(details).toHaveTextContent('Keep boundaries clear.');
		});

		await unmount(island);
	});
});
