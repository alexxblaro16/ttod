import { expect, test } from '@playwright/test';
import type { GraphLink, GraphNode, WisdomEntry } from '../src/types/domain';

test.use({ serviceWorkers: 'block' });

const sectionCount = 8;
const nodesPerSection = 250;
const largeGraphNodes: GraphNode[] = Array.from({ length: sectionCount * nodesPerSection }, (_, index) => {
	const sectionIndex = Math.floor(index / nodesPerSection);
	return {
		id: `section-${String(sectionIndex).padStart(2, '0')}-${String(index).padStart(4, '0')}`,
		section: `section-${String(sectionIndex).padStart(2, '0')}`,
		origin: index % 3 === 0 ? 'human' : index % 3 === 1 ? 'studio' : 'blackbox',
		status: 'active',
		text: `Graph node ${index}`,
		lang: 'en'
	};
});

const largeGraphWisdom: WisdomEntry[] = largeGraphNodes.map((node) => ({
	...node,
	level: 'beginner',
		teaches: 'Keep graph rendering predictable at scale.',
	tags: [node.section, 'large-corpus'],
		related: [],
		rights: { license: 'CC-BY-NC-SA-4.0' }
}));

const largeGraphEdges: GraphLink[] = largeGraphNodes.slice(1).map((node, index) => ({
	source: largeGraphNodes[index].id,
	target: node.id,
	rel: 'related'
}));

test('renders a large graph and keeps filtering within the interaction budget', async ({ page }) => {
	await page.addInitScript(() => {
		(window as Window & { graphPerfStart?: number }).graphPerfStart = performance.now();
	});
	await page.route('**/api/v1/graph', (route) => route.fulfill({
		status: 200,
		contentType: 'application/json',
		body: JSON.stringify({ nodes: largeGraphNodes, edges: largeGraphEdges })
	}));
	await page.route('**/api/v1/wisdom/sample', (route) => route.fulfill({
		status: 200,
		contentType: 'application/json',
		body: JSON.stringify(largeGraphWisdom)
	}));

	await page.goto('/en/graph');
	const graph = page.getByRole('group', {
		name: `Knowledge graph with ${largeGraphNodes.length} nodes and ${largeGraphEdges.length} edges`
	});
	await expect(graph).toBeVisible();

	const renderMs = await page.evaluate(() => {
		const start = (window as Window & { graphPerfStart?: number }).graphPerfStart;
		return start === undefined ? Number.POSITIVE_INFINITY : performance.now() - start;
	});
	expect(renderMs).toBeLessThan(8000);
	await expect(graph.locator('[data-node-id]')).toHaveCount(largeGraphNodes.length);

	const filter = page.getByLabel('Filter by tag');
	const filterStartMs = await page.evaluate(() => performance.now());
	await filter.selectOption('section-04');
	await expect(page.getByRole('group', { name: 'Knowledge graph with 250 nodes and 249 edges' })).toBeVisible();
	const filterMs = await page.evaluate((startMs) => performance.now() - startMs, filterStartMs);
	expect(filterMs).toBeLessThan(2000);
	console.log(`graph-scale nodes=${largeGraphNodes.length} renderMs=${renderMs.toFixed(1)} filterMs=${filterMs.toFixed(1)}`);

	const firstVisibleNode = page.locator('[data-node-id^="section-04-"]').first();
	await firstVisibleNode.focus();
	await firstVisibleNode.press('ArrowRight');
	await expect(page.locator('[data-node-id^="section-04-"]:focus')).toHaveCount(1);
});
