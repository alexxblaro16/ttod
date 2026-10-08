import { createServer, type Server } from 'node:http';
import { readFile } from 'node:fs/promises';
import { test, expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const cachePrefix = 'ttod-pwa-stub-';
const proofAsset = '/visual-system/tokens.css';

async function waitForControl(page: Page) {
	await expect.poll(() => page.evaluate(() => Boolean(navigator.serviceWorker.controller)), {
		message: 'The activated worker must control the page',
	}).toBe(true);
}

async function fetchProof(page: Page) {
	// Execute in the controlled page: APIRequestContext requests bypass its worker.
	// no-store bypasses the HTTP cache, while explicit Cache Storage still works.
	return page.evaluate(async (asset) => {
		const response = await fetch(asset, { cache: 'no-store' });
		return { status: response.status, body: await response.text() };
	}, proofAsset);
}

async function closeServer(server: Server) {
	await new Promise<void>((resolve, reject) => {
		server.close((error) => error ? reject(error) : resolve());
		server.closeAllConnections();
	});
}

for (const locale of ['en', 'es'] as const) {
	test(`/${locale}/ registers the worker and serves proof CSS offline`, async ({ page, context }) => {
		await page.goto(`/${locale}/`);
		await waitForControl(page);
		const boundary = page.locator('#ttod-network-boundary');
		const labels = locale === 'en'
			? { online: 'Online', offline: 'Offline' }
			: { online: 'En línea', offline: 'Sin conexión' };

		await expect(boundary).toHaveAttribute('role', 'status');
		await expect(boundary).toHaveAttribute('aria-live', 'polite');
		await expect(boundary).toHaveAttribute('aria-atomic', 'true');
		await expect(boundary).toHaveAttribute('data-state', 'online');
		await expect(boundary).toHaveText(labels.online);

		const manifestLink = page.locator('link[rel="manifest"]');
		await expect(manifestLink).toHaveCount(1);
		await expect(manifestLink).toHaveAttribute('href', '/site.webmanifest');
		const manifestResponse = await context.request.get('/site.webmanifest');
		expect(manifestResponse.status()).toBe(200);
		expect(await manifestResponse.json()).toMatchObject({
			name: expect.any(String), start_url: expect.any(String), display: 'standalone',
		});

		const onlineProof = await fetchProof(page);
		expect(onlineProof.status).toBe(200);
		expect(onlineProof.body.length).toBeGreaterThan(0);
		await context.setOffline(true);
		try {
			await expect(boundary).toHaveAttribute('data-state', 'offline');
			await expect(boundary).toHaveText(labels.offline);
			// Keep the document open: offline HTML navigation belongs to Task 2.
			expect(await fetchProof(page)).toEqual(onlineProof);
			const accessibility = await new AxeBuilder({ page }).analyze();
			expect(accessibility.violations, JSON.stringify(accessibility.violations, null, 2)).toEqual([]);
		} finally {
			await context.setOffline(false);
		}
		await expect(boundary).toHaveAttribute('data-state', 'online');
		await expect(boundary).toHaveText(labels.online);
	});
}

test('a real worker update removes v1, preserves unrelated caches, and serves v2 offline', async ({ page, context, baseURL }) => {
	expect(baseURL, 'Start the local stack before running PWA E2E').toBeTruthy();
	const workerSource = await readFile(new URL('../public/sw.js', import.meta.url), 'utf8');
	const versionDeclaration = /^const CACHE_NAME = `\$\{CACHE_PREFIX\}v\d+`;$/m;
	expect(workerSource, 'Keep the versioned cache declaration explicit').toMatch(versionDeclaration);
	const proofResponse = await context.request.get(proofAsset);
	expect(proofResponse.status()).toBe(200);
	const expectedProof = { status: 200, body: await proofResponse.text() };
	expect(expectedProof.body.length).toBeGreaterThan(0);

	let version = 'v1';
	// Isolate each test's origin and serve two real versions of the actual worker.
	// Only its version declaration changes; production files and Docker stay intact.
	// A server is needed because updated worker scripts cannot use page.route().
	const server = createServer(async (request, response) => {
		try {
			if (request.url === '/sw.js') {
				response.writeHead(200, { 'Content-Type': 'application/javascript', 'Cache-Control': 'no-store' });
				response.end(workerSource.replace(versionDeclaration, () => 'const CACHE_NAME = `${CACHE_PREFIX}' + version + '`;'));
				return;
			}
			const upstream = await fetch(new URL(request.url ?? '/', baseURL!));
			response.writeHead(upstream.status, {
				'Content-Type': upstream.headers.get('content-type') ?? 'application/octet-stream',
				'Cache-Control': 'no-store',
			});
			response.end(Buffer.from(await upstream.arrayBuffer()));
		} catch (error) {
			response.writeHead(502, { 'Content-Type': 'text/plain' });
			response.end(error instanceof Error ? error.message : String(error));
		}
	});

	try {
		await new Promise<void>((resolve, reject) => {
			server.once('error', reject);
			server.listen(0, '127.0.0.1', resolve);
		});
		const address = server.address();
		if (!address || typeof address === 'string') throw new Error('No test server port allocated');
		await page.goto(`http://127.0.0.1:${address.port}/en/`);
		await waitForControl(page);
		await expect.poll(() => page.evaluate(() => caches.keys())).toEqual([`${cachePrefix}v1`]);
		await context.setOffline(true);
		expect(await fetchProof(page)).toEqual(expectedProof);
		await context.setOffline(false);

		await page.evaluate(async () => {
			const unrelated = await caches.open('unrelated-pwa-test');
			await unrelated.put('/unrelated-marker', new Response('preserve this response'));
		});
		version = 'v2';
		await page.evaluate(async () => {
			const registration = await navigator.serviceWorker.getRegistration('/');
			if (!registration) throw new Error('Worker was not registered');
			const claimed = new Promise<void>((resolve) => {
				navigator.serviceWorker.addEventListener('controllerchange', () => resolve(), { once: true });
			});
			await registration.update();
			await claimed;
		});
		// Activation is asynchronous; poll real state instead of assuming update()
		// or a fixed sleep means cache cleanup has finished.
		await expect.poll(() => page.evaluate(async () => (await caches.keys()).sort()), {
			message: 'v2 activation must retire v1 without deleting unrelated caches',
		}).toEqual([`${cachePrefix}v2`, 'unrelated-pwa-test'].sort());
		await waitForControl(page);
		await context.setOffline(true);
		expect(await fetchProof(page)).toEqual(expectedProof);
		expect(await page.evaluate(async () => {
			const unrelated = await caches.open('unrelated-pwa-test');
			return (await unrelated.match('/unrelated-marker'))?.text();
		})).toBe('preserve this response');
	} finally {
		await context.setOffline(false);
		await closeServer(server);
	}
});
