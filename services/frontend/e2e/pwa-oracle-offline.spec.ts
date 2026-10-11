import { readFile } from 'node:fs/promises';
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

for (const locale of ['en', 'es'] as const) {
	test(`/${locale}/oracle loads and remains interactive after offline navigation and reload`, async ({ page, context }) => {
		const labels = locale === 'en'
			? { title: 'Ask the Tao', offline: 'Offline', close: 'Close oracle', open: 'Open oracle' }
			: { title: 'Pregunta al Tao', offline: 'Sin conexión', close: 'Cerrar oráculo', open: 'Abrir oráculo' };
		const target = `/${locale}/oracle`;
		const errors: string[] = [];
		const failedAssets: string[] = [];
		page.on('pageerror', (error) => errors.push(error.message));
		page.on('requestfailed', (request) => {
			const path = new URL(request.url()).pathname;
			if (path.startsWith('/_astro/') || path.startsWith('/visual-system/')) {
				failedAssets.push(path);
			}
		});

		// Reject stale Docker builds rather than testing a different worker from source.
		const servedWorker = await context.request.get('/sw.js');
		expect(servedWorker.status()).toBe(200);
		expect(await servedWorker.text()).toBe(await readFile(new URL('../public/sw.js', import.meta.url), 'utf8'));

		// Install on the home page without first visiting the Oracle document.
		// Offline navigation therefore proves install precaching, not a warm page.
		await page.goto(`/${locale}/`);
		await expect.poll(() => page.evaluate(() => Boolean(navigator.serviceWorker.controller))).toBe(true);
		await expect.poll(() => page.evaluate(async (path) => {
			const names = (await caches.keys()).filter((name) => name.startsWith('ttod-pwa-stub-'));
			return (await Promise.all(names.map(async (name) => Boolean(await (await caches.open(name)).match(path)))))
				.some(Boolean);
		}, target), { message: 'Installation must precache the selected Oracle document' }).toBe(true);

		await context.setOffline(true);
		try {
			const navigation = await page.goto(target);
			expect(navigation?.status()).toBe(200);
			expect(navigation?.fromServiceWorker()).toBe(true);
			await expect(page.getByRole('heading', { name: labels.title, exact: true })).toBeVisible();

			// A real offline reload discards the previous document and React state.
			const reload = await page.reload();
			expect(reload?.status()).toBe(200);
			expect(reload?.fromServiceWorker()).toBe(true);
			await expect(page.getByRole('heading', { name: labels.title, exact: true })).toBeVisible();
			await expect(page.locator('#ttod-network-boundary')).toHaveAttribute('data-state', 'offline');
			await expect(page.locator('#ttod-network-boundary')).toHaveText(labels.offline);

			const input = page.getByRole('textbox');
			await expect(input).toHaveAccessibleName(/\S/);
			await input.fill('A question entered while offline');
			const close = page.getByRole('button', { name: labels.close, exact: true });
			await close.focus();
			await close.press('Enter');
			const open = page.getByRole('button', { name: labels.open, exact: true });
			await expect(open).toHaveAttribute('aria-expanded', 'false');
			await open.press('Enter');
			await expect(input).toHaveValue('A question entered while offline');
			// Responding controls prove React hydrated; SSR text alone would pass otherwise.
			const accessibility = await new AxeBuilder({ page }).analyze();
			expect(accessibility.violations, JSON.stringify(accessibility.violations, null, 2)).toEqual([]);
			expect(failedAssets, 'All required scripts, styles and images must be available offline').toEqual([]);
			expect(errors, 'Offline hydration must not raise JavaScript errors').toEqual([]);
		} finally {
			await context.setOffline(false);
		}
	});
}
