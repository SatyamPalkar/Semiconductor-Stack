// Production-export workflows with real local financial API and isolated Chrome.
import { test, expect } from '../../apps/web/node_modules/@playwright/test';

const shots = '../../data/interim/web-review';

test('visual conclusions change the reading without mixing measures', async ({ page }) => {
  const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Who turns growth into cash?' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'TSMC generates more per revenue unit.' })).toBeVisible();
  const nvidia = page.locator('.conclusion-node[data-company="NVDA"]');
  const tsmc = page.locator('.conclusion-node[data-company="TSM"]');
  await expect(nvidia).toContainText('49.11%'); await expect(tsmc).toContainText('63.10%');
  await page.getByRole('button', { name: 'Cash left', exact: true }).click();
  await expect(nvidia).toContainText('46.53%'); await expect(tsmc).toContainText('30.06%');
  await expect(page.getByRole('heading', { name: 'NVIDIA keeps more per revenue unit.' })).toBeVisible();
  await expect(page.locator('.conclusion-context')).toContainText('Capital-outlay scopes differ');
  await page.getByRole('button', { name: 'Capital spending', exact: true }).click();
  await expect(nvidia).toContainText('2.48%'); await expect(tsmc).toContainText('33.03%');
  await expect(page.getByRole('heading', { name: 'Capital takes different paths.' })).toBeVisible();
  await expect(page.locator('.conclusion-context')).toContainText('principal payments are additional');
  await expect(page.locator('.conclusion-map-key')).toContainText('Node size, position and distance are conceptual');
  expect(errors).toEqual([]);
  await page.getByRole('button', { name: 'Cash generated', exact: true }).click();
  await page.screenshot({ path: `${shots}/overview-desktop.png`, fullPage: true, animations: 'disabled' });
});

test('company nodes expose exact source rows and financial evidence is optional', async ({ page }) => {
  await page.goto('/companies/');
  await page.getByRole('button', { name: 'Cash left', exact: true }).click();
  const tsmc = page.locator('.conclusion-node[data-company="TSM"]');
  await expect(tsmc).toContainText('30.06%');
  await page.getByRole('button', { name: 'FY2024 / CY2023', exact: true }).click();
  await expect(tsmc).toContainText('13.51%');
  await expect(page.locator('.conclusion-node[data-company="NVDA"]')).toContainText('44.23%');
  await page.getByRole('button', { name: 'FY2025 / CY2024', exact: true }).click();
  await tsmc.click();
  const evidence = page.getByRole('complementary', { name: 'Selected company evidence' });
  await evidence.locator('summary').click();
  await expect(evidence).toContainText('30.0649 %');
  await expect(evidence).toContainText('1,826,177,068 TWD thousand');
  await expect(evidence).toContainText('956,006,536 TWD thousand');
  await expect(evidence.getByRole('link').first()).toHaveAttribute('href', /investor.tsmc.com.*#page=65$/);
  await expect(page.locator('.investigation-table')).toBeHidden();
  await page.locator('.evidence-drawer>summary').click();
  const cashRow = page.locator('.investigation-table tbody tr').last().locator('td').last();
  await cashRow.locator('summary').click();
  await expect(cashRow).toContainText('870170532.0000 TWD thousand');
  expect(await page.locator('.investigation-table table').evaluate(el => el.scrollWidth <= el.parentElement!.clientWidth)).toBe(true);
  await page.locator('.comparability-note>summary').click();
  await expect(page.locator('.comparability-note')).toContainText('Operating cash-flow classifications are not harmonized');
  await page.locator('.evidence-drawer>summary').click();
  await evidence.locator('summary').click();
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({ path: `${shots}/comparison-desktop.png`, fullPage: true, animations: 'disabled' });
});

test('earlier research dates withhold values and visual conclusions in every story chapter', async ({ page }) => {
  await page.goto('/companies/');
  await page.getByLabel('Research as-of date').fill('2025-03-11');
  await expect(page.getByRole('status')).toContainText('does not contain enough evidence for this pair');
  const tsmc = page.locator('.conclusion-node[data-company="TSM"]');
  for (const chapter of ['Cash generated', 'Capital spending', 'Cash left']) {
    await page.getByRole('button', { name: chapter, exact: true }).click();
    await expect(tsmc).toContainText('Unavailable');
    await expect(tsmc.locator('.node-arc')).toHaveCount(0);
    await expect(page.getByRole('heading', { name: 'The evidence stops here.' })).toBeVisible();
  }
  await page.getByRole('button', { name: 'Provenance', exact: true }).click();
  const modal = page.getByRole('dialog', { name: 'Source provenance' });
  await expect(modal).not.toContainText('TSMC 2024 annual report');
  await expect(modal).toContainText('TSMC 2023 annual report');
});

test('financial charts preserve values, units and source-date filtering', async ({ page }) => {
  const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
  await page.goto('/industry-economics/');
  const revenue = page.getByRole('figure', { name: 'Annual NVIDIA revenue by fiscal year in USD billions', exact: true });
  await expect(revenue.locator('.chart-data-key')).toContainText('$60.92B');
  await expect(revenue.locator('.chart-data-key')).toContainText('$130.50B');
  await revenue.getByRole('button', { name: 'Slope', exact: true }).click();
  await expect(revenue.locator('.scatterlayer .trace').first()).toBeVisible();
  await expect(revenue).toContainText('no interim values are supplied');
  await page.getByLabel('Financial chart company').selectOption('TSM');
  const tsmc = page.getByRole('figure', { name: 'Annual TSMC revenue by fiscal year in TWD billions', exact: true });
  await expect(tsmc.locator('.chart-data-key')).toContainText('NT$2894.31B');
  await expect(tsmc.locator('.chart-data-key')).toContainText('NT$2161.74B');
  await expect(tsmc.locator('.chart-data-key')).not.toContainText('$130.50B');
  await tsmc.getByRole('button', { name: 'Columns', exact: true }).click();
  await expect(tsmc.locator('.barlayer .trace').first()).toBeVisible();
  await page.getByLabel('Research as-of date').fill('2025-03-11');
  await expect(tsmc.locator('.chart-data-key')).toContainText('No observations available');
  expect(errors).toEqual([]);
});

test('industry atlas filters companies, profiles and verified coverage', async ({ page }) => {
  await page.goto('/value-chain/');
  await expect(page.getByRole('heading', { name: 'The company directory.' })).toBeVisible();
  await expect(page.locator('.directory-status')).toContainText('139');
  await page.getByRole('button', { name: 'Explore Equipment' }).click();
  await expect(page.getByLabel('Filter companies by role')).toHaveValue('equipment');
  await page.getByLabel('Search semiconductor companies').fill('ASML');
  const profile = page.getByRole('complementary', { name: 'Company profile' });
  await expect(profile.getByRole('heading')).toHaveText('ASML');
  await expect(profile).toContainText('Historical financial dataset loaded');
  await expect(profile.getByRole('link', { name: 'Inspect the financial dataset' })).toHaveAttribute('href', '/industry-economics/?company=ASML');
  await page.getByRole('button', { name: 'Clear filters', exact: true }).click();
  await page.getByLabel('Financial datasets loaded (6)').check();
  await expect(page.getByRole('status')).toContainText('of 6 matching entries');
  await page.getByLabel('Search semiconductor companies').fill('does-not-exist');
  await expect(page.getByRole('heading', { name: 'No match for these filters.' })).toBeVisible();
  await page.getByRole('button', { name: 'Show all companies', exact: true }).last().click();
  await page.getByRole('button', { name: 'Next company page' }).click();
  await expect(page.locator('.directory-pagination')).toContainText('Page 2 of 12');
  await page.getByRole('button', { name: 'Previous company page' }).click();
  await page.locator('.directory-company-card').filter({ hasText: 'AMD' }).click();
  await expect(profile.getByRole('heading')).toHaveText('AMD');
  await expect(profile).toBeFocused();
  await profile.getByRole('link', { name: 'Browse company entries ↓' }).click();
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({ path: `${shots}/industry-atlas-desktop.png`, fullPage: true, animations: 'disabled' });
});

test('provenance resolves to primary sources, print dates and checksums', async ({ page }) => {
  await page.goto('/sources/');
  await page.getByRole('button', { name: /Ingested evidence/ }).click();
  const nvidia = page.locator('.source-card').filter({ hasText: 'NVIDIA fourth-quarter' });
  await expect(nvidia).toContainText('published 2025-02-26');
  await expect(nvidia.getByRole('link', { name: /Open original source/ })).toHaveAttribute('href', /nvidianews.nvidia.com/);
  const asml = page.locator('.source-card').filter({ hasText: 'ASML 2024 annual report' });
  await expect(asml).toContainText('published 2025-03-05');
  await expect(asml).not.toContainText('report printed 2025-03-05');
  const tsmc = page.locator('.source-card').filter({ hasText: 'TSMC 2024 annual report' });
  await expect(tsmc).toContainText('report printed 2025-03-12');
  await tsmc.getByText('Checksum & record details').click();
  await expect(tsmc.locator('code')).toHaveText(/^[a-f0-9]{64}$/);
  await expect(tsmc).toContainText('independent historical availability is unverified');
  await page.getByLabel('Definition company').selectOption('TSM');
  const cashDefinition = page.locator('.methodology details').filter({ has: page.getByText('Cash after disclosed capital outlays', { exact: true }) });
  await cashDefinition.locator('summary').click();
  await expect(cashDefinition).toContainText('Not a harmonized FCF measure');
  await page.getByLabel('Search sources').fill('no matching source');
  await expect(page.getByText('No source matches this search and as-of date.')).toBeVisible();
});

test('an early date removes financial figures and comparative prose from the overview', async ({ page }) => {
  await page.goto('/'); await page.getByLabel('Research as-of date').fill('2024-03-11');
  await expect(page.getByRole('status').first()).toContainText('No financial source was available');
  await expect(page.locator('.conclusion-node[data-company="NVDA"]')).toContainText('Unavailable');
  await expect(page.getByRole('heading', { name: 'The evidence stops here.' })).toBeVisible();
  await page.getByRole('link', { name: 'Research briefs', exact: true }).click();
  await expect(page.getByLabel('Research as-of date')).toHaveValue('2024-03-11');
  await expect(page.getByRole('status').filter({ hasText: 'comparative findings are withheld' })).toBeVisible();
});

test('NVIDIA questions use the real financial API and exact cited inputs', async ({ page }) => {
  await page.goto('/assistant/'); await expect(page.getByText('API connected', { exact: true })).toBeVisible();
  await page.getByRole('button', { name: 'What was NVIDIA free cash flow in FY2025?', exact: true }).click();
  const answer = page.locator('.answer-panel'); await expect(answer).toContainText('60724.0000 USD million');
  await expect(answer).toContainText('0 model calls'); await expect(answer.locator('.evidence')).toHaveCount(3);
  await answer.locator('.evidence').first().locator('summary').click();
  await expect(answer.getByRole('link', { name: 'Original source' }).first()).toHaveAttribute('href', /nvidianews.nvidia.com/);
});

test('TSMC questions retain the original currency, calendar and analytical residual definition', async ({ page }) => {
  await page.goto('/assistant/'); await expect(page.getByText('API connected', { exact: true })).toBeVisible();
  await page.getByLabel('Evidence desk company').selectOption('TSM');
  await page.getByRole('button', { name: 'What was TSMC free cash flow in CY2024?', exact: true }).click();
  const answer = page.locator('.answer-panel');
  await expect(answer).toContainText('870170532.0000 TWD thousand');
  await expect(answer).toContainText('Not a harmonized FCF measure');
  await expect(answer.locator('.evidence')).toHaveCount(2);
  await page.getByLabel('Research question', { exact: true }).fill('What was NVIDIA free cash flow in FY2025?');
  await page.getByRole('button', { name: 'Ask question', exact: true }).click();
  await expect(page.locator('.answer-panel')).toContainText('There is not enough evidence');
});

test('current prices and forecasts remain outside the evidence desk', async ({ page }) => {
  await page.goto('/assistant/'); await expect(page.getByText('API connected', { exact: true })).toBeVisible();
  await page.getByLabel('Research question', { exact: true }).fill('What is NVIDIA stock price today?');
  await page.getByRole('button', { name: 'Ask question', exact: true }).click();
  await expect(page.locator('.answer-panel')).toContainText('There is not enough evidence');
  await page.getByLabel('Research question', { exact: true }).fill('What was Intel revenue in 2024?');
  await page.getByRole('button', { name: 'Ask question', exact: true }).click();
  await expect(page.locator('.answer-panel')).toContainText('There is not enough evidence');
});

test('offline examples are labelled and the static investigation stays useful', async ({ page }) => {
  await page.route('http://127.0.0.1:8100/**', route => route.abort()); await page.goto('/assistant/');
  await expect(page.getByRole('heading', { name: 'Backend offline' })).toBeVisible();
  await page.getByLabel('Evidence desk company').selectOption('TSM');
  await page.getByRole('button', { name: 'What was TSMC free cash flow in CY2024?', exact: true }).click();
  await expect(page.locator('.answer-panel')).toContainText('Recorded calculation · no live AI');
  await expect(page.locator('.answer-panel')).toContainText('870170532.0000 TWD thousand');
  await page.getByLabel('Research question', { exact: true }).fill('A new question without a recorded example');
  await page.getByRole('button', { name: 'Ask question', exact: true }).click();
  await expect(page.getByRole('alert').filter({ hasText: 'The API is offline' })).toBeVisible();
  await page.goto('/companies/');
  await expect(page.locator('.conclusion-node[data-company="TSM"]')).toContainText('63.10%');
});

test('the research note includes counterevidence and withholds unsupported historical findings', async ({ page }) => {
  await page.goto('/briefs/');
  await expect(page.getByRole('heading', { name: 'Counterevidence and alternative explanations' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'What would change this conclusion?' })).toBeVisible();
  await expect(page.locator('.investigation-brief')).toContainText('The order changes depending on the measure');
  await page.getByLabel('Research as-of date').fill('2025-03-11');
  await expect(page.getByRole('status')).toContainText('comparative findings are withheld');
  await expect(page.locator('.investigation-brief')).not.toContainText('63.10%');
});

test('mobile navigation and the comparison fit the viewport', async ({ page }) => {
  const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
  await page.setViewportSize({ width: 393, height: 852 }); await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Who turns growth into cash?' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await page.getByRole('button', { name: 'Toggle navigation' }).click();
  await page.getByRole('link', { name: 'Company comparison', exact: true }).click();
  await expect(page.locator('.conclusion-node[data-company="TSM"]')).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await page.locator('.conclusion-node[data-company="NVDA"]').click();
  await expect(page.getByRole('complementary', { name: 'Selected company evidence' })).toContainText('NVIDIA');
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({ path: `${shots}/comparison-mobile.png`, fullPage: true, animations: 'disabled' });
  expect(errors).toEqual([]);
});


test('all research routes render without page overflow or browser errors at desktop, tablet and phone widths', async ({ page }) => {
  const errors: string[] = []; page.on('pageerror', e => errors.push(e.message));
  for (const width of [1440, 768, 393]) {
    await page.setViewportSize({ width, height: 900 });
    for (const route of ['/', '/companies/', '/industry-economics/', '/briefs/', '/assistant/', '/sources/', '/value-chain/']) {
      await page.goto(route);
      await page.locator('.snapshot-freshness').waitFor({ state: 'attached' });
      if (route === '/industry-economics/') await expect(page.locator('.plot .main-svg').first()).toBeVisible();
      if (route === '/' || route === '/companies/') {
        const diagram = await page.locator('.conclusion-orbit').boundingBox();
        for (const ticker of ['NVDA', 'TSM']) {
          const node = await page.locator(`.conclusion-node[data-company="${ticker}"]`).boundingBox();
          expect(node!.width).toBeGreaterThanOrEqual(44);
          expect(node!.x).toBeGreaterThanOrEqual(diagram!.x);
          expect(node!.x + node!.width).toBeLessThanOrEqual(diagram!.x + diagram!.width);
          expect(node!.y).toBeGreaterThanOrEqual(diagram!.y);
          expect(node!.y + node!.height).toBeLessThanOrEqual(diagram!.y + diagram!.height);
        }
      }
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), `${route} at ${width}px`).toBe(true);
    }
  }
  expect(errors).toEqual([]);
});


test('visual conclusions support keyboard selection and reduced motion', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/companies/');
  const nvidia = page.locator('.conclusion-node[data-company="NVDA"]');
  await nvidia.focus(); await page.keyboard.press('Enter');
  await expect(nvidia).toHaveAttribute('aria-pressed', 'true');
  await expect(page.getByRole('complementary', { name: 'Selected company evidence' })).toContainText('NVIDIA');
  const step = page.getByRole('button', { name: 'Cash left', exact: true });
  await step.focus(); await page.keyboard.press('Enter');
  await expect(step).toHaveAttribute('aria-pressed', 'true');
  await expect(nvidia).toContainText('46.53%');
  expect(await nvidia.locator('.node-arc').evaluate(el => getComputedStyle(el).transitionDuration)).toBe('0s');
});


test('resource discovery stays separate from ingested evidence and filters by access', async ({ page }) => {
  await page.goto('/sources/?role=equipment#research-library');
  await expect(page.getByLabel('Filter resources by industry role')).toHaveValue('equipment');
  await expect(page.locator('.source-card')).toHaveCount(0);
  await page.getByLabel('Search research resources').fill('SEMI');
  await expect(page.locator('.research-resource-card').first()).toContainText('NOT INGESTED EVIDENCE');
  await page.getByRole('button', { name: 'Clear resource filters', exact: true }).click();
  await expect(page.getByRole('status')).toContainText('36 matching resources');
  await page.getByLabel('Filter resources by access').selectOption('mixed');
  const cards = page.locator('.research-resource-card');
  expect(await cards.count()).toBeGreaterThan(0);
  for (const card of await cards.all()) await expect(card).toContainText('SOME ACCESS RESTRICTED');
  await page.getByLabel('Search research resources').fill('impossible-topic-000');
  await expect(page.getByRole('heading', { name: 'No resources match these filters.' })).toBeVisible();
});

test('expanded financial visuals retain euros, negative margins and analytical labels', async ({ page }) => {
  await page.goto('/industry-economics/?company=ASML');
  await expect(page.getByLabel('Financial chart company')).toHaveValue('ASML');
  const euro = page.getByRole('figure', { name: 'Annual ASML revenue by fiscal year in EUR billions', exact: true });
  await expect(euro).toContainText('€28.26B');
  await expect(page.locator('.financial-cash-lens')).toContainText('32.14');
  await page.getByLabel('Financial chart company').selectOption('MU');
  const margin = page.getByRole('figure', { name: 'Micron gross margin by fiscal year', exact: true });
  await expect(margin).toContainText('-9.11%');
  await page.getByRole('button', { name: 'FY2023 Ended 2023-08-31', exact: true }).click();
  await expect(page.locator('.financial-cash-lens')).toContainText('-35.09');
  await expect(page.locator('.financial-cash-lens')).toContainText('Negative cash residual');
  await page.getByRole('button', { name: 'FY2024 Ended 2024-08-29', exact: true }).click();
  await expect(margin.locator('.main-svg').first()).toBeVisible();
  const lowerBound = await margin.locator('.plot').evaluate(el => (el as HTMLElement & {_fullLayout: {xaxis: {range: number[]}}})._fullLayout.xaxis.range[0]);
  expect(lowerBound).toBeLessThan(-9.11);
  await page.getByLabel('Financial chart company').selectOption('AMKR');
  await expect(page.locator('.financial-cash-lens')).toContainText('analytical gross-PPE cash residual');
  await expect(page.locator('.financial-cash-lens')).toContainText('NOT Amkor’s reported free cash flow');
  await page.locator('.financial-cash-lens summary').click();
  await expect(page.locator('.financial-cash-lens')).toContainText('345072.0000 USD thousand');
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({ path: `${shots}/expanded-financials-desktop.png`, fullPage: true, animations: 'disabled' });
  await page.getByLabel('Research as-of date').fill('2024-09-24');
  await page.getByLabel('Financial chart company').selectOption('MU');
  await expect(page.getByRole('status')).toContainText('No annual dataset');
});

test('Micron questions reconcile all five cash inputs without model calls', async ({ page }) => {
  await page.goto('/assistant/');
  await expect(page.getByText('API connected', { exact: true })).toBeVisible();
  await page.getByLabel('Evidence desk company').selectOption('MU');
  await page.getByRole('button', { name: 'What was Micron free cash flow in FY2024?', exact: true }).click();
  const answer = page.locator('.answer-panel');
  await expect(answer).toContainText('386.0000 USD million');
  await expect(answer).toContainText('adjusted free cash flow');
  await expect(answer.locator('.evidence')).toHaveCount(5);
  await expect(answer).toContainText('0 model calls');
});

test('atlas and financial explorer are usable on mobile with keyboard selection', async ({ page }) => {
  await page.setViewportSize({ width: 393, height: 852 });
  await page.goto('/value-chain/');
  for (const node of await page.locator('.industry-role-node').all()) {
    const bounds = await node.boundingBox();
    expect(bounds!.width).toBeGreaterThanOrEqual(44);
    expect(bounds!.height).toBeGreaterThanOrEqual(44);
  }
  const memory = page.getByRole('button', { name: 'Explore Memory' });
  await memory.focus(); await page.keyboard.press('Enter');
  await expect(memory).toHaveAttribute('aria-pressed', 'true');
  await expect(page.getByLabel('Filter companies by role')).toHaveValue('memory');
  await page.getByLabel('Research as-of date').fill('2024-03-01');
  await expect(page.locator('.directory-status')).toContainText('139');
  await page.screenshot({ path: `${shots}/industry-atlas-mobile.png`, fullPage: true, animations: 'disabled' });
  await page.goto('/industry-economics/?company=ASML');
  await page.getByLabel('Research as-of date').fill('2025-03-13');
  await expect(page.locator('.financial-cash-lens')).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({ path: `${shots}/expanded-financials-mobile.png`, fullPage: true, animations: 'disabled' });
});


test('guided story connects business illustrations, cash chapters and the next question', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1 })).toContainText('A tiny chip.');
  const rail=page.getByRole('navigation', { name: 'Story chapters' });
  await page.getByRole('link', { name: 'Start the story', exact: true }).click();
  await expect(page.locator('#story-system')).toBeInViewport();
  await expect(rail.getByRole('link', { name: '01 The system' })).toHaveAttribute('aria-current', 'location');
  await page.getByRole('button', { name: 'Next: Fabricate', exact: true }).click();
  await expect(page.getByRole('tab', { name: 'Fabricate', exact: true })).toHaveAttribute('aria-selected','true');
  await expect(page.getByRole('tabpanel')).toContainText('Give the idea a physical form.');
  await expect(page.getByRole('tabpanel').getByRole('img')).toHaveAttribute('aria-label','Illustrated wafer with an array of chip dies');
  await page.getByRole('tab', { name: 'Fabricate', exact: true }).focus();
  await page.keyboard.press('ArrowRight');
  await expect(page.getByRole('tab', { name: 'Equip', exact: true })).toBeFocused();
  await expect(page.getByRole('tabpanel')).toContainText('ASML');
  await page.keyboard.press('End');
  await expect(page.getByRole('tab', { name: 'Connect', exact: true })).toHaveAttribute('aria-selected','true');
  await page.getByRole('link', { name: 'Now follow the cash', exact: true }).click();
  await expect(page.locator('#story-cash')).toBeInViewport();
  await page.getByRole('button', { name: 'Next: Capital spending', exact: true }).click();
  await expect(page.getByRole('button', { name: 'Capital spending', exact: true })).toHaveAttribute('aria-pressed','true');
  await page.getByRole('button', { name: 'Next: Cash left', exact: true }).click();
  await expect(page.locator('.conclusion-node[data-company="NVDA"]')).toContainText('46.53%');
  await page.getByRole('link', { name: 'Next: Change the year', exact: true }).click();
  await expect(page.locator('#story-cycle')).toBeInViewport();
  await expect(rail.getByRole('link', { name: '03 The changing year' })).toHaveAttribute('aria-current','location');
  await rail.getByRole('link', { name: '04 Your next question' }).click();
  await expect(page.locator('#story-next')).toBeInViewport();
  await expect(page.locator('.story-next-paths a')).toHaveCount(4);
  await page.goto('/companies/');
  await page.getByRole('button',{name:'Next: Capital spending',exact:true}).click();
  const cashTop=await page.locator('.conclusion-experience').evaluate(el=>el.getBoundingClientRect().top);
  const headerBottom=await page.locator('.atlas-masthead').evaluate(el=>el.getBoundingClientRect().bottom);
  expect(cashTop).toBeGreaterThanOrEqual(headerBottom);
});

test('the memory story preserves signed figures and withholds unavailable evidence', async ({ page }) => {
  await page.goto('/');
  const chapter=page.locator('#story-cycle');
  await expect(chapter.locator('.year-observation-key')).toContainText('-9.11%');
  await expect(chapter.locator('.year-observation-key')).toContainText('22.35%');
  await chapter.getByRole('button', { name: 'Adjusted cash margin', exact: true }).click();
  await expect(chapter.locator('.year-observation-key')).toContainText('-35.09%');
  await expect(chapter.locator('.year-observation-key')).toContainText('1.54%');
  await chapter.locator('.year-story-sources>summary').click();
  const latest=chapter.locator('.year-story-sources section').last();
  await latest.locator('.metric-trace>summary').click();
  await expect(latest).toContainText('capital investment');
  await expect(latest.locator('.metric-trace li')).toHaveCount(6);
  await expect(latest.getByRole('link').first()).toHaveAttribute('href',/investors.micron.com/);
  await page.getByLabel('Research as-of date').fill('2024-09-24');
  await expect(chapter.getByRole('status')).toContainText('graphic and its interpretation are withheld');
  await expect(chapter.getByRole('figure')).toHaveCount(0);
  await expect(chapter).not.toContainText('The sign changes.');
  await expect(chapter.locator('.year-story-sources')).toHaveCount(0);
});

test('continuation links carry the reader from interpretation to the stored evidence', async ({ page }) => {
  await page.goto('/companies/');
  const onward=page.getByRole('complementary',{name:'Continue the research story'});
  await onward.getByRole('link',{name:'Read the research note'}).click();
  await expect(page).toHaveURL(/\/briefs\/$/);
  await page.getByRole('complementary',{name:'Continue the research story'}).getByRole('link',{name:'Inspect the sources'}).click();
  await expect(page).toHaveURL(/\/sources\/#evidence-records$/);
  await expect(page.getByRole('button',{name:/Ingested evidence/})).toHaveAttribute('aria-pressed','true');
  await expect(page.locator('.source-card')).toHaveCount(7);
});

test('the illustrated narrative fits small screens and honors reduced motion', async ({ page }) => {
  await page.emulateMedia({ reducedMotion:'reduce' });
  await page.setViewportSize({width:393,height:852});
  await page.goto('/');
  await expect(page.getByRole('heading',{name:/A tiny chip/})).toBeVisible();
  expect(await page.locator('.scene-cover .silicon-stack').evaluate(el=>getComputedStyle(el).animationName)).toBe('none');
  expect(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior)).toBe('auto');
  for(const act of ['story-system','story-cash','story-cycle','story-next']) {
    await page.getByRole('navigation',{name:'Story chapters'}).getByRole('link',{name:new RegExp(act==='story-system'?'The system':act==='story-cash'?'The cash':act==='story-cycle'?'The changing year':'Your next question')}).click();
    await expect(page.locator(`#${act}`)).toBeInViewport();
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
  }
  for(const tab of await page.getByRole('tablist',{name:'Explore the business story'}).getByRole('tab').all()) {
    const box=await tab.boundingBox(); expect(box!.width).toBeGreaterThanOrEqual(44);expect(box!.height).toBeGreaterThanOrEqual(44);
  }
  await page.evaluate(()=>window.scrollTo(0,0));
  await page.screenshot({path:`${shots}/guided-story-mobile.png`,fullPage:true,animations:'disabled'});
  await page.setViewportSize({width:1440,height:1000});
  await page.goto('/');
  await expect(page.locator('.story-cover')).toHaveCount(1);
  await expect(page.getByRole('heading',{level:1})).toBeVisible();
  await page.screenshot({path:`${shots}/guided-story-desktop.png`,fullPage:true,animations:'disabled'});
  await page.screenshot({path:`${shots}/guided-cover-desktop.png`,animations:'disabled'});
  await page.getByRole('link',{name:'Start the story',exact:true}).click();
  await page.screenshot({path:`${shots}/guided-system-desktop.png`,animations:'disabled'});
  await page.getByRole('navigation',{name:'Story chapters'}).getByRole('link',{name:'03 The changing year'}).click();
  await expect(page.getByRole('navigation',{name:'Story chapters'}).getByRole('link',{name:'03 The changing year'})).toHaveAttribute('aria-current','location');
  await page.screenshot({path:`${shots}/guided-year-desktop.png`,animations:'disabled'});
});
