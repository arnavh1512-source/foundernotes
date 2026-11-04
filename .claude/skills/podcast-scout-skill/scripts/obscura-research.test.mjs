import { test } from 'node:test';
import assert from 'node:assert/strict';
import { researchUrl, browserEnvironment, parsePage, parseArgs } from './obscura-research.mjs';

test('only exact public research HTTPS origins are permitted', () => {
  assert.equal(researchUrl('https://arxiv.org/abs/123#part'), 'https://arxiv.org/abs/123');
  for (const url of ['http://arxiv.org/', 'https://127.0.0.1/', 'https://arxiv.org.attacker.com/', 'https://user:secret@arxiv.org/', 'https://arxiv.org:8080/', 'file:///etc/passwd', 'https://localhost/', 'https://[::1]/']) {
    assert.throws(() => researchUrl(url));
  }
});
test('browser subprocess never inherits credentials or proxy/private-network overrides', () => {
  const env = browserEnvironment({ PATH: 'safe-path', SystemRoot: 'C:\\Windows', OPENAI_API_KEY: 'secret', OBSCURA_ALLOW_PRIVATE_NETWORK: '1', OBSCURA_PROXY: 'http://internal', HOME: 'private-home' });
  assert.equal(env.PATH, 'safe-path');
  assert.equal(env.OPENAI_API_KEY, undefined);
  assert.equal(env.OBSCURA_PROXY, undefined);
  assert.equal(env.HOME, undefined);
  assert.equal(env.OBSCURA_ALLOW_PRIVATE_NETWORK, '0');
});
test('page parser rejects cross-host redirects and caps evidence size', () => {
  const page = { url: 'https://arxiv.org/abs/123', title: 'Research', text: 'Evidence '.repeat(2000) };
  assert.equal(parsePage(JSON.stringify(page), page.url).text.length, 12000);
  assert.equal(parsePage(JSON.stringify(page), page.url).truncated, true);
  assert.equal(parsePage(JSON.stringify(page), page.url).originalTextLength, page.text.trim().length);
  assert.equal(parsePage(JSON.stringify({ ...page, text: 'Evidence '.repeat(30) }), page.url).truncated, false);
  assert.equal(parsePage(JSON.stringify(JSON.stringify(page)), page.url).url, page.url);
  assert.throws(() => parsePage(JSON.stringify({ ...page, url: 'https://www.nih.gov/' }), page.url));
  assert.throws(() => parsePage(JSON.stringify({ ...page, text: 'Access denied' }), page.url));
  assert.throws(() => parsePage('not json', page.url));
});
test('CLI validates configuration and limits workload', () => {
  assert.equal(parseArgs([]).help, true);
  assert.equal(parseArgs(['--check']).check, true);
  assert.throws(() => parseArgs(['--binary']));
  assert.throws(() => parseArgs(['--allow-private-network']));
  assert.throws(() => parseArgs(['--check', 'https://arxiv.org/']));
  assert.throws(() => parseArgs(Array(4).fill('https://arxiv.org/')));
});
