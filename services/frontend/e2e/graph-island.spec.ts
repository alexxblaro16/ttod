import { expect, test } from '@playwright/test';
import { joinTags, radialLayout } from '../src/components/graph/layout';
import type { GraphLink, GraphNode, WisdomEntry } from '../src/types/domain';

const graphNodes: GraphNode[] = [
	{ id: 'arch-001', section: 'architecture', origin: 'human', status: 'active', text: 'Keep boundaries clear.', lang: 'en' },
	{ id: 'arch-002', section: 'architecture', origin: 'studio', status: 'active', text: 'Share pure functions.', lang: 'en' },
	{ id: 'wis-001', section: 'wisdom', origin: 'blackbox', status: 'active', text: 'Question the obvious.', lang: 'en' }
];

const wisdom: WisdomEntry[] = graphNodes.map((node) => ({
	...node,
	level: 'beginner',
	teaches: '',
	tags: [`tag-${node.id}`],
	related: [],
	rights: { license: 'CC-BY-NC-SA-4.0' }
}));

const graphEdges: GraphLink[] = [
	{ source: 'arch-001', target: 'arch-002', rel: 'related' },
	{ source: 'arch-002', target: 'wis-001', rel: 'related' }
];

test('fetches, lays out, renders, and selects graph nodes accessibly', async ({ page }) => {
	const requestedPaths: string[] = [];
	await page.route('**/api/v1/graph', async (route) => {
		requestedPaths.push(new URL(route.request().url()).pathname);
		await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ nodes: graphNodes, edges: graphEdges }) });
	});
	await page.route('**/api/v1/wisdom/sample', async (route) => {
		requestedPaths.push(new URL(route.request().url()).pathname);
		await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(wisdom) });
	});

	await page.goto('/en/graph');
	const svg = page.getByRole('group', { name: 'Knowledge graph with 3 nodes and 2 edges' });
	await expect(svg).toBeVisible();
	await expect(page.locator('svg line')).toHaveCount(graphEdges.length);
	await expect(page.getByText('Human', { exact: true })).toBeVisible();
	await expect(page.getByText('Studio', { exact: true })).toBeVisible();
	await expect(page.getByText('AI proposal', { exact: true })).toBeVisible();
	expect(requestedPaths.sort()).toEqual(['/api/v1/graph', '/api/v1/wisdom/sample']);

	const expectedNodes = radialLayout(joinTags(graphNodes, wisdom));
	const nodeButtons = svg.getByRole('button');
	await expect(nodeButtons).toHaveCount(expectedNodes.length);
	for (const node of expectedNodes) {
		const renderedNode = page.getByRole('button', { name: `${node.id}: ${node.text}` });
		await expect(renderedNode).toHaveAttribute('tabindex', '0');
		await expect(renderedNode).toHaveAttribute('cx', String(node.x));
		await expect(renderedNode).toHaveAttribute('cy', String(node.y));
	}

	const details = page.getByRole('complementary', { name: 'Selected node' });
	await expect(details).toHaveAttribute('aria-live', 'polite');
	await page.getByRole('button', { name: 'arch-001: Keep boundaries clear.' }).click();
	await expect(details).toContainText('Keep boundaries clear.');
	await expect(details).toBeInViewport();
	await page.getByRole('button', { name: 'arch-002: Share pure functions.' }).press('Enter');
	await expect(details).toContainText('Share pure functions.');
	await expect(details).toBeInViewport();
	await page.getByRole('button', { name: 'wis-001: Question the obvious.' }).press('Space');
	await expect(details).toContainText('Question the obvious.');
	await expect(details).toBeInViewport();
});

test('shows loading and empty states while a successful graph response is pending', async ({ page }) => {
	let releaseGraphResponse!: () => void;
	const graphResponsePending = new Promise<void>((resolve) => {
		releaseGraphResponse = resolve;
	});
	await page.route('**/api/v1/graph', async (route) => {
		await graphResponsePending;
		await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ nodes: [], edges: [] }) });
	});
	await page.route('**/api/v1/wisdom/sample', (route) => route.fulfill({
		status: 200,
		contentType: 'application/json',
		body: JSON.stringify([])
	}));

	await page.goto('/en/graph');
	await expect(page.getByText('Loading live graph…')).toBeVisible();
	releaseGraphResponse();
	await expect(page.getByText('No graph nodes are available.')).toBeVisible();
	await expect(page.getByRole('group', { name: /Knowledge graph/ })).toHaveCount(0);
});

test('announces graph fetch failures', async ({ page }) => {
	await page.route('**/api/v1/graph', (route) => route.fulfill({
		status: 503,
		contentType: 'application/json',
		body: JSON.stringify({ detail: 'unavailable' })
	}));
	await page.route('**/api/v1/wisdom/sample', (route) => route.fulfill({
		status: 200,
		contentType: 'application/json',
		body: JSON.stringify([])
	}));

	await page.goto('/en/graph');
	await expect(page.getByRole('alert')).toHaveText('The live graph is unavailable.');
});