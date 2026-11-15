// Resolve the web app's installed runner from this repository-level test directory.
import { test, expect } from '../../apps/web/node_modules/@playwright/test';

test('overview shows real metrics and honest coverage', async ({ page }) => {
  const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
  await page.goto('/'); await expect(page.getByRole('heading', { name: 'The industry behind everything.' })).toBeVisible();
  await expect(page.getByRole('button', { name: /Annual revenue \$130.50B/ })).toBeVisible();
  await expect(page.getByText('Source access pending', { exact: false }).first()).toBeVisible();
  await expect(page.locator('.plot .main-svg').first()).toBeVisible(); expect(errors).toEqual([]); if (process.env.SAVE_SCREENSHOTS === '1') await page.screenshot({ path: '../../../.local-artifacts/semiconductor-milestone1/overview.png', fullPage: true });
});
test('provenance resolves to official source and checksum', async ({ page }) => {
  await page.goto('/'); await page.getByRole('button', { name: 'Provenance', exact: true }).click();
  const modal = page.getByRole('dialog', { name: 'Source provenance' }); await expect(modal).toBeVisible();
  await expect(modal.getByText(/published 2025-02-26/)).toBeVisible();
  await expect(modal.getByRole('link', { name: /Open original source/ })).toHaveAttribute('href', /nvidianews.nvidia.com/);
  await modal.getByText('Checksum & record details').click(); await expect(modal.locator('code')).toHaveText(/^[a-f0-9]{64}$/);
  await page.getByRole('button', { name: 'Close source details' }).click(); await expect(modal).toBeHidden();
});
test('as-of date excludes future publications', async ({ page }) => {
  await page.goto('/'); await page.getByLabel('Research as-of date').fill('2025-02-25');
  await expect(page.getByRole('status')).toContainText('No financial source was available');
  await expect(page.getByRole('button', { name: /Annual revenue/ })).toContainText('—');
});
test('assistant calls the real financial API with cited inputs', async ({ page }) => {
  await page.goto('/assistant/'); await expect(page.getByText('API connected', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'What was NVIDIA free cash flow in FY2025?', exact: true }).click();
  const answer = page.locator('.answer-panel'); await expect(answer).toContainText('60724.0000 USD million');
  await expect(answer).toContainText('0 model calls'); await expect(answer.locator('.evidence')).toHaveCount(3);
  await answer.locator('.evidence').first().locator('summary').click();
  await expect(answer.getByRole('link', { name: 'Original source' }).first()).toHaveAttribute('href', /nvidianews.nvidia.com/);
});
test('current-price question gets an explicit limitation', async ({ page }) => {
  await page.goto('/assistant/'); await expect(page.getByText('API connected', { exact: true })).toBeVisible();
  await page.getByLabel('Research question', { exact: true }).fill('What is NVIDIA stock price today?');
  await page.getByRole('button', { name: 'Ask question', exact: true }).click();
  await expect(page.locator('.answer-panel')).toContainText('There is not enough evidence');
});
test('offline examples are labelled and new questions do not get fake answers', async ({ page }) => {
  await page.route('http://127.0.0.1:8100/**', route => route.abort()); await page.goto('/assistant/');
  await expect(page.getByRole('heading', { name: 'Backend offline' })).toBeVisible();
  await page.getByRole('button', { name: 'What was NVIDIA gross margin in FY2025?', exact: true }).click();
  await expect(page.locator('.answer-panel')).toContainText('Recorded calculation · no live AI');
  await expect(page.locator('.answer-panel')).toContainText('74.9887 %');
  await page.getByLabel('Research question', { exact: true }).fill('A new question without a recorded example');
  await page.getByRole('button', { name: 'Ask question', exact: true }).click();
  await expect(page.getByRole('alert').filter({ hasText: 'The API is offline' })).toContainText('The API is offline');
});
test('coverage filters and source search have honest empty states', async ({ page }) => {
  await page.goto('/companies/'); await page.getByLabel('Company coverage filter').selectOption('source_access_pending');
  await expect(page.locator('tbody').first().getByRole('row')).toHaveCount(1); await expect(page.locator('tbody').first()).toContainText('TSMC');
  await page.getByRole('link', { name: 'Sources & methodology', exact: true }).click();
  await page.getByLabel('Search sources').fill('no matching source'); await expect(page.getByText('No source matches this search and as-of date.')).toBeVisible();
});
test('mobile navigation fits without horizontal overflow', async ({ page }) => {
  await page.setViewportSize({ width: 393, height: 852 }); await page.goto('/');
  await page.getByRole('button', { name: 'Toggle navigation' }).click(); await page.getByRole('link', { name: 'Value chain', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Follow the silicon.' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
});
