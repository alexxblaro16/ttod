import { expect, test, type Page } from '@playwright/test';
import { buildUrl, parseUrlState, resolveUrlState } from '../src/components/graph/urlState';
import type { GraphLink, GraphNode, WisdomEntry } from '../src/types/domain';

test.use({ serviceWorkers: 'block' });

const graphNodes: GraphNode[] = [
	{ id: 'arch-001', section: 'architecture', origin: 'human', status: 'active', text: 'Keep boundaries clear.', lang: 'en' },
	{ id: 'arch-002', section: 'architecture', origin: 'studio', status: 'active', text: 'Share pure functions.', lang: 'en' },
	{ id: 'wis-001', section: 'wisdom', origin: 'blackbox', status: 'active', text: 'Question the obvious.', lang: 'en' }
];
const wisdom: WisdomEntry[] = graphNodes.map((node) => ({
	id: node.id,
	section: node.section,
	level: 'beginner',
	text: node.text,
	teaches: '',
	tags: [node.section],
	related: [],
	origin: node.origin,
	lang: node.lang,
	rights: { license: 'CC-BY-NC-SA-4.0' }
}));
const graphEdges: GraphLink[] = [
	{ source: 'arch-001', target: 'arch-002', rel: 'related' },
	{ source: 'arch-002', target: 'wis-001', rel: 'related' }
];

async function mockApi(page: Page) {
	await page.route('**/api/v1/graph', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ nodes: graphNodes, edges: graphEdges }) }));
	await page.route('**/api/v1/wisdom/sample', (route) => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(wisdom) }));
}

const details = (page: Page) => page.getByRole('complementary', { name: 'Selected node' });
const graph = (page: Page, nodes: number, edges: number) => page.getByRole('group', { name: `Knowledge graph with ${nodes} nodes and ${edges} edges` });

test('deep link restores tag and selected node', async ({ page }) => {
	await mockApi(page);
	await page.goto('/en/graph?tag=architecture&node=arch-002');
	await expect(graph(page, 2, 1)).toBeVisible();
	await expect(page.getByLabel('Filter by tag')).toHaveValue('architecture');
	await expect(details(page)).toContainText('Share pure functions.');
});

test('selecting a node and a tag writes the URL, and reload restores it', async ({ page }) => {
	await mockApi(page);
	await page.goto('/en/graph');
	await expect(graph(page, 3, 2)).toBeVisible();
	await page.locator('[data-node-id="arch-001"]').click();
	await expect(page).toHaveURL(/node=arch-001/);
	await page.getByLabel('Filter by tag').selectOption('architecture');
	await expect(page).toHaveURL(/tag=architecture/);
	await expect(page).toHaveURL(/node=arch-001/);

	await page.reload();
	await expect(graph(page, 2, 1)).toBeVisible();
	await expect(page.getByLabel('Filter by tag')).toHaveValue('architecture');
	await expect(details(page)).toContainText('Keep boundaries clear.');
});

test('back and forward restore filter and selection', async ({ page }) => {
	await mockApi(page);
	await page.goto('/en/graph');
	await expect(graph(page, 3, 2)).toBeVisible();
	await page.locator('[data-node-id="wis-001"]').click();
	await page.locator('[data-node-id="arch-001"]').click();
	await expect(details(page)).toContainText('Keep boundaries clear.');

	await page.goBack();
	await expect(details(page)).toContainText('Question the obvious.');
	await expect(page).toHaveURL(/node=wis-001/);
	await page.goBack();
	await expect(details(page)).toContainText('Select a node to view its details.');
	await page.goForward();
	await page.goForward();
	await expect(details(page)).toContainText('Keep boundaries clear.');
});

test('clearing the filter removes the tag param and a hidden node is dropped from the URL', async ({ page }) => {
	await mockApi(page);
	await page.goto('/en/graph');
	await page.locator('[data-node-id="wis-001"]').click();
	await page.getByLabel('Filter by tag').selectOption('architecture');
	await expect(page).toHaveURL((url) => url.searchParams.get('tag') === 'architecture' && !url.searchParams.has('node'));
	await expect(details(page)).toContainText('Select a node to view its details.');
	await page.getByLabel('Filter by tag').selectOption('');
	await expect(page).toHaveURL((url) => !url.searchParams.has('tag'));
	await expect(graph(page, 3, 2)).toBeVisible();
});

test('invalid tag or node in the URL resets to a clean default state', async ({ page }) => {
	await mockApi(page);
	await page.goto('/en/graph?tag=nope&node=ghost-999');
	await expect(graph(page, 3, 2)).toBeVisible();
	await expect(page.getByLabel('Filter by tag')).toHaveValue('');
	await expect(details(page)).toContainText('Select a node to view its details.');
	await expect(page).toHaveURL((url) => !url.searchParams.has('tag') && !url.searchParams.has('node'));

	await page.goto('/en/graph?tag=wisdom&node=arch-001');
	await expect(graph(page, 1, 0)).toBeVisible();
	await expect(page.getByLabel('Filter by tag')).toHaveValue('wisdom');
	await expect(page).toHaveURL((url) => url.searchParams.get('tag') === 'wisdom' && !url.searchParams.has('node'));
});

test('parseUrlState reads tag and node, defaulting to empty', () => {
	expect(parseUrlState('?tag=architecture&node=arch-031')).toEqual({ tag: 'architecture', node: 'arch-031' });
	expect(parseUrlState('')).toEqual({ tag: '', node: '' });
});

test('buildUrl sets, removes, and preserves params', () => {
	expect(buildUrl('http://x/en/graph', { tag: 'a', node: 'n-1' })).toBe('/en/graph?tag=a&node=n-1');
	expect(buildUrl('http://x/en/graph?tag=a&node=n-1&q=1#h', { tag: '' })).toBe('/en/graph?node=n-1&q=1#h');
	expect(buildUrl('http://x/en/graph?tag=a', { node: 'n-2' })).toBe('/en/graph?tag=a&node=n-2');
});

test('resolveUrlState resets invalid tag or hidden node', () => {
	const visible = (tag: string) => (tag === 'a' ? ['n-1'] : ['n-1', 'n-2']);
	expect(resolveUrlState({ tag: 'a', node: 'n-1' }, ['a'], visible)).toEqual({ tag: 'a', node: 'n-1' });
	expect(resolveUrlState({ tag: 'zzz', node: 'n-2' }, ['a'], visible)).toEqual({ tag: '', node: 'n-2' });
	expect(resolveUrlState({ tag: 'a', node: 'n-2' }, ['a'], visible)).toEqual({ tag: 'a', node: '' });
	expect(resolveUrlState({ tag: '', node: 'missing' }, ['a'], visible)).toEqual({ tag: '', node: '' });
});
