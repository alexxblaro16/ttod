import { expect, test } from '@playwright/test';
import { joinTags, radialLayout } from '../src/components/graph/layout';
import type { GraphLink, GraphNode, WisdomEntry } from '../src/types/domain';

test.use({ serviceWorkers: 'block' });

const graphNodes: GraphNode[] = [
	{ id: 'arch-001', section: 'architecture', origin: 'human', status: 'active', text: 'Keep boundaries clear.', lang: 'en' },
	{ id: 'arch-002', section: 'architecture', origin: 'studio', status: 'active', text: 'Share pure functions.', lang: 'en' },
	{ id: 'wis-001', section: 'wisdom', origin: 'blackbox', status: 'active', text: 'Question the obvious.', lang: 'en' }
];

const wisdom: WisdomEntry[] = graphNodes.map((node) => ({
	...node,
	level: 'beginner',
	teaches: '',
	tags: [`tag-${node.id}`, 'shared'],
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
	await expect(page.getByText('Architecture & Modularization', { exact: true })).toBeVisible();
	await expect(page.getByLabel('Section legend').getByText('Wisdom', { exact: true })).toBeVisible();
	expect(requestedPaths.sort()).toEqual(['/api/v1/graph', '/api/v1/wisdom/sample']);

	const expectedNodes = radialLayout(joinTags(graphNodes, wisdom));
	const nodeButtons = svg.getByRole('button');
	await expect(nodeButtons).toHaveCount(expectedNodes.length);
	for (const node of expectedNodes) {
			const renderedNode = page.getByRole('button', { name: `${node.id}: ${node.text}, section: ${node.section}, origin: ${node.origin}, tags: ${node.tags.join(', ')}` });
			await expect(renderedNode).toHaveAttribute('tabindex', '0');
			await expect(renderedNode).toHaveAttribute('cx', String(node.x));
			await expect(renderedNode).toHaveAttribute('cy', String(node.y));
		}

		const details = page.getByRole('complementary', { name: 'Selected node' });
		await expect(details).toHaveAttribute('aria-live', 'polite');
		const firstNode = page.getByRole('button', { name: 'arch-001: Keep boundaries clear., section: architecture, origin: human, tags: tag-arch-001, shared' });
		await firstNode.click();
		await expect(details).toContainText('Keep boundaries clear.');
		await expect(details).toBeVisible();
		await details.scrollIntoViewIfNeeded();
		await expect(details).toBeInViewport();
		await firstNode.focus();
		await firstNode.press('ArrowLeft');
		await expect(page.getByRole('button', { name: 'arch-002: Share pure functions., section: architecture, origin: studio, tags: tag-arch-002, shared' })).toBeFocused();
		await page.getByRole('button', { name: 'arch-002: Share pure functions., section: architecture, origin: studio, tags: tag-arch-002, shared' }).press('Enter');
		await expect(details).toContainText('Share pure functions.');
		await details.scrollIntoViewIfNeeded();
		await expect(details).toBeInViewport();
		await page.getByLabel('Filter by tag').focus();
		await expect(details).toContainText('Share pure functions.');
		await page.getByRole('button', { name: 'wis-001: Question the obvious., section: wisdom, origin: blackbox, tags: tag-wis-001, shared' }).press('Space');
		await expect(details).toContainText('Question the obvious.');
		await expect(details).toBeVisible();

		const firstNodeById = page.locator('[data-node-id="arch-001"]');
		await firstNodeById.focus();
		await firstNodeById.press('ArrowRight');
		await expect(page.locator('[data-node-id="arch-002"]')).toBeFocused();
		await expect(details).toContainText('Question the obvious.');
		await page.locator('[data-node-id="arch-002"]').press('Space');
		await expect(details).toContainText('Share pure functions.');
	});

	test('filters by tag, moves focus to the filter when the focused node disappears, and follows browser history', async ({ page }) => {
		await page.route('**/api/v1/graph', (route) => route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({ nodes: graphNodes, edges: graphEdges })
		}));
		await page.route('**/api/v1/wisdom/sample', (route) => route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify(wisdom)
		}));

		await page.goto('/en/graph');
		const filter = page.getByLabel('Filter by tag');
		await expect(filter).toHaveValue('');
		const node = page.locator('[data-node-id="arch-001"]');
		await node.focus();
		await node.press('Space');
		const details = page.getByRole('complementary', { name: 'Selected node' });
		await expect(details).toContainText('Keep boundaries clear.');

		await page.evaluate(() => {
			const url = new URL(window.location.href);
			url.searchParams.set('tag', 'tag-arch-002');
			window.history.pushState({}, '', url);
			window.dispatchEvent(new PopStateEvent('popstate'));
		});

		await expect(filter).toHaveValue('tag-arch-002');
		await expect(page.getByRole('group', { name: 'Knowledge graph with 1 nodes and 0 edges' })).toBeVisible();
		await expect(filter).toBeFocused();
		await expect(details).toContainText('Select a node to view its details.');
		await expect(page).toHaveURL(/tag=tag-arch-002/);

		await page.goBack();
		await expect(filter).toHaveValue('');
		await expect(page.getByRole('group', { name: 'Knowledge graph with 3 nodes and 2 edges' })).toBeVisible();
	});

	test('filters from the tag control, preserves matching selection, clears selection, and restores the graph', async ({ page }) => {
		await page.route('**/api/v1/graph', (route) => route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({ nodes: graphNodes, edges: graphEdges })
		}));
		await page.route('**/api/v1/wisdom/sample', (route) => route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify(wisdom.map((entry) => ({
				...entry,
				tags: entry.id.startsWith('arch-') ? ['architecture'] : ['wisdom']
			})))
		}));

		await page.goto('/en/graph');
		const filter = page.getByLabel('Filter by tag');
		const details = page.getByRole('complementary', { name: 'Selected node' });
		await expect(page.getByRole('group', { name: 'Knowledge graph with 3 nodes and 2 edges' })).toBeVisible();

		await page.locator('[data-node-id="arch-001"]').click();
		await expect(details).toContainText('Keep boundaries clear.');
		await filter.selectOption('architecture');
		await expect(page).toHaveURL(/tag=architecture/);
		await expect(page.getByRole('group', { name: 'Knowledge graph with 2 nodes and 1 edges' })).toBeVisible();
		await expect(page.locator('[data-node-id="arch-001"]')).toBeVisible();
		await expect(page.locator('[data-node-id="arch-002"]')).toBeVisible();
		await expect(page.locator('[data-node-id="wis-001"]')).toHaveCount(0);
		await expect(page.locator('svg line')).toHaveCount(1);
		await expect(details).toContainText('Keep boundaries clear.');
		await expect(page.getByText('Filtered to tag: architecture')).toBeAttached();

		await filter.selectOption('wisdom');
		await expect(page).toHaveURL(/tag=wisdom/);
		await expect(page.getByRole('group', { name: 'Knowledge graph with 1 nodes and 0 edges' })).toBeVisible();
		await expect(page.locator('[data-node-id="wis-001"]')).toBeVisible();
		await expect(page.locator('[data-node-id="arch-001"]')).toHaveCount(0);
		await expect(details).toContainText('Select a node to view its details.');

		await filter.selectOption('');
		await expect(page).toHaveURL((url) => !url.searchParams.has('tag'));
		await expect(page.getByRole('group', { name: 'Knowledge graph with 3 nodes and 2 edges' })).toBeVisible();
		await expect(page.locator('svg line')).toHaveCount(2);
		await expect(page.getByText('Showing all tags')).toBeAttached();

		await page.goBack();
		await expect(filter).toHaveValue('wisdom');
		await expect(page.getByRole('group', { name: 'Knowledge graph with 1 nodes and 0 edges' })).toBeVisible();
		await page.goBack();
		await expect(filter).toHaveValue('architecture');
		await expect(page.getByRole('group', { name: 'Knowledge graph with 2 nodes and 1 edges' })).toBeVisible();
	});

	test('initializes the tag filter from the URL', async ({ page }) => {
		await page.route('**/api/v1/graph', (route) => route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify({ nodes: graphNodes, edges: graphEdges })
		}));
		await page.route('**/api/v1/wisdom/sample', (route) => route.fulfill({
			status: 200,
			contentType: 'application/json',
			body: JSON.stringify(wisdom.map((entry) => ({
				...entry,
				tags: entry.id.startsWith('arch-') ? ['architecture'] : ['wisdom']
			})))
		}));

		await page.goto('/en/graph?tag=architecture');
		await expect(page.getByLabel('Filter by tag')).toHaveValue('architecture');
		await expect(page.getByRole('group', { name: 'Knowledge graph with 2 nodes and 1 edges' })).toBeVisible();
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