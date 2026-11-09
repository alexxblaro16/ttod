import { expect, test, type Page } from '@playwright/test';
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
	tags: node.section === 'architecture' ? ['architecture'] : ['wisdom'],
	related: [],
	rights: { license: 'CC-BY-NC-SA-4.0' }
}));

const graphEdges: GraphLink[] = [
	{ source: 'arch-001', target: 'arch-002', rel: 'related' },
	{ source: 'arch-002', target: 'wis-001', rel: 'related' }
];

async function mockGraphApi(page: Page) {
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
}

test('tabs from the labelled filter to visible nodes and activates a node with Enter', async ({ page }) => {
	await mockGraphApi(page);
	await page.goto('/en/graph');

	const filter = page.getByLabel('Filter by tag');
	const visibleNodes = page.locator('[data-node-id]');
	await filter.focus();
	await page.keyboard.press('Tab');
	for (let index = 0; index < await visibleNodes.count(); index += 1) {
		const node = visibleNodes.nth(index);
		await expect(node).toBeFocused();
		await expect(node).toHaveAttribute('role', 'button');
		await expect(node).toHaveAttribute('tabindex', '0');
		await expect(node).toHaveAttribute('aria-label');
		await expect(node).toHaveCSS('stroke-width', '3px');
		if (index < (await visibleNodes.count()) - 1) await page.keyboard.press('Tab');
	}

	await page.locator('[data-node-id="arch-001"]').press('Enter');
	await expect(page.getByRole('complementary', { name: 'Selected node' })).toContainText('Keep boundaries clear.');

	const secondNode = page.locator('[data-node-id="arch-002"]');
	await secondNode.press('Space');
	await expect(page.getByRole('complementary', { name: 'Selected node' })).toContainText('Share pure functions.');
});

test('uses the filter with arrow keys and returns focus when history removes a focused node', async ({ page }) => {
	await mockGraphApi(page);
	await page.goto('/en/graph');

	const filter = page.getByLabel('Filter by tag');
	await expect(page.locator('[data-node-id]')).toHaveCount(3);
	await filter.focus();
	await page.keyboard.press('ArrowDown');
	await expect(filter).toHaveValue('architecture');
	await expect(page).toHaveURL(/tag=architecture/);
	await expect(page.locator('[data-node-id]')).toHaveCount(2);

	const focusedNode = page.locator('[data-node-id="arch-001"]');
	await focusedNode.focus();
	await page.evaluate(() => {
		const url = new URL(window.location.href);
		url.searchParams.set('tag', 'wisdom');
		window.history.pushState({}, '', url);
		window.dispatchEvent(new PopStateEvent('popstate'));
	});

	await expect(page.locator('[data-node-id]')).toHaveCount(1);
	await expect(filter).toBeFocused();
	await expect(page.locator('[data-node-id="arch-001"]')).toHaveCount(0);
});
