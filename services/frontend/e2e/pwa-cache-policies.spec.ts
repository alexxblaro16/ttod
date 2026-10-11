import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { test as base, expect, type Page } from '@playwright/test';

type PolicyServer = {
	origin: string;
	hits: Map<string, number>;
	apiValue: string;
	apiStatus: number;
};

const staticPaths = ['/visual-system/policy-test.css', '/assets/policy-test.css', '/_astro/policy-test.css'];

// A real HTTP origin is required: page.route() cannot intercept worker fetches.
// Serve the actual worker unchanged, with deterministic endpoints for freshness
// and network-hit assertions. Forward the real app and its precache dependencies.
const test = base.extend<{ policyServer: PolicyServer }>({
	policyServer: async ({ baseURL, request }, use) => {
		if (!baseURL) throw new Error('Start the local stack before running PWA tests');
		const worker = await readFile(new URL('../public/sw.js', import.meta.url), 'utf8');
		const served = await request.get('/sw.js');
		expect(served.status()).toBe(200);
		expect(await served.text(), 'Rebuild frontend before testing the local worker').toBe(worker);
		const state: PolicyServer = { origin: '', hits: new Map(), apiValue: 'first', apiStatus: 200 };
		const server = createServer(async (incoming, outgoing) => {
			const path = new URL(incoming.url ?? '/', 'http://localhost').pathname;
			state.hits.set(path, (state.hits.get(path) ?? 0) + 1);
			try {
				if (path === '/sw.js') {
					outgoing.writeHead(200, { 'Content-Type': 'application/javascript', 'Cache-Control': 'no-store' });
					outgoing.end(worker);
				} else if (staticPaths.includes(path)) {
					outgoing.writeHead(200, { 'Content-Type': 'text/css', 'Cache-Control': 'no-store' });
					outgoing.end('body { --policy-test: cached; }');
				} else if (path.startsWith('/api/policy-test/')) {
					// Deliberately cacheable by HTTP: Network-First must still attempt
					// the server rather than reuse an old browser HTTP-cache entry.
					outgoing.writeHead(state.apiStatus, { 'Content-Type': 'application/json', 'Cache-Control': 'max-age=3600' });
					outgoing.end(JSON.stringify({ value: state.apiValue, method: incoming.method }));
				} else {
					const upstream = await fetch(new URL(incoming.url ?? '/', baseURL));
					outgoing.writeHead(upstream.status, { 'Content-Type': upstream.headers.get('content-type') ?? 'application/octet-stream', 'Cache-Control': 'no-store' });
					outgoing.end(Buffer.from(await upstream.arrayBuffer()));
				}
			} catch (error) {
				outgoing.writeHead(502);
				outgoing.end(String(error));
			}
		});
		try {
			await new Promise<void>((resolve, reject) => {
				server.once('error', reject);
				server.listen(0, '127.0.0.1', resolve);
			});
			const address = server.address();
			if (!address || typeof address === 'string') throw new Error('Missing server port');
			state.origin = `http://127.0.0.1:${address.port}`;
			await use(state);
		} finally {
			await new Promise<void>((resolve, reject) => {
				server.close((error) => error ? reject(error) : resolve());
				server.closeAllConnections();
			});
		}
	},
});

async function install(page: Page, origin: string) {
	await page.goto(`${origin}/en/`);
	await expect.poll(() => page.evaluate(() => Boolean(navigator.serviceWorker.controller))).toBe(true);
}

async function cachedText(page: Page, path: string) {
	return page.evaluate(async (target) => {
		const name = (await caches.keys()).find((key) => key.startsWith('ttod-pwa-stub-'));
		if (!name) throw new Error('Missing active PWA cache');
		return (await (await caches.open(name)).match(target))?.text() ?? null;
	}, path);
}

async function fetchText(page: Page, path: string, method = 'GET') {
	return page.evaluate(async ({ target, verb }) => {
		try {
			const response = await fetch(target, { method: verb });
			return { status: response.status, body: await response.text() };
		} catch {
			return { status: 0, body: 'network failure' };
		}
	}, { target: path, verb: method });
}

for (const path of staticPaths) {
	test(`Cache-First stores ${path} and reuses it online and offline`, async ({ page, context, policyServer }) => {
		await install(page, policyServer.origin);
		expect(await cachedText(page, path)).toBeNull();
		const first = await fetchText(page, path);
		expect(first.status).toBe(200);
		expect(await cachedText(page, path)).toBe(first.body);
		expect(policyServer.hits.get(path)).toBe(1);
		expect(await fetchText(page, path)).toEqual(first);
		expect(policyServer.hits.get(path)).toBe(1);
		await context.setOffline(true);
		try {
			expect(await fetchText(page, path)).toEqual(first);
			expect(policyServer.hits.get(path)).toBe(1);
		} finally {
			await context.setOffline(false);
		}
	});
}

test('Network-First refreshes API data, falls back offline, and preserves HTTP errors', async ({ page, context, policyServer }) => {
	await install(page, policyServer.origin);
	const path = '/api/policy-test/data';
	const first = await fetchText(page, path);
	expect(JSON.parse(first.body).value).toBe('first');
	expect(await cachedText(page, path)).toBe(first.body);
	policyServer.apiValue = 'fresh';
	const fresh = await fetchText(page, path);
	expect(JSON.parse(fresh.body).value).toBe('fresh');
	expect(policyServer.hits.get(path)).toBe(2);
	expect(await cachedText(page, path)).toBe(fresh.body);
	policyServer.apiStatus = 503;
	expect((await fetchText(page, path)).status).toBe(503);
	expect(await cachedText(page, path)).toBe(fresh.body);
	await context.setOffline(true);
	try {
		expect(await fetchText(page, path)).toEqual(fresh);
		expect((await fetchText(page, '/api/policy-test/cold')).status).toBe(0);
		expect(policyServer.hits.get(path)).toBe(3);
	} finally {
		await context.setOffline(false);
	}
	policyServer.apiStatus = 200;
	policyServer.apiValue = 'reconnected';
	expect(JSON.parse((await fetchText(page, path)).body).value).toBe('reconnected');
	expect(policyServer.hits.get(path)).toBe(4);
});

test('POST requests bypass GET caching and do not replay cached API data', async ({ page, context, policyServer }) => {
	await install(page, policyServer.origin);
	const path = '/api/policy-test/post';
	const get = await fetchText(page, path);
	policyServer.apiValue = 'posted';
	const post = await fetchText(page, path, 'POST');
	expect(JSON.parse(post.body)).toEqual({ value: 'posted', method: 'POST' });
	expect(await cachedText(page, path)).toBe(get.body);
	await context.setOffline(true);
	try {
		expect((await fetchText(page, path, 'POST')).status).toBe(0);
	} finally {
		await context.setOffline(false);
	}
	expect(policyServer.hits.get(path)).toBe(2);
});
