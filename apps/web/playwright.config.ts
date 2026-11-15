import { defineConfig, devices } from '@playwright/test';
export default defineConfig({ testDir: '../../tests/e2e', fullyParallel: false, workers: 1, retries: 0,
  reporter: [['list'], ['json', { outputFile: '../../evaluations/results/browser-results.json' }]], outputDir: 'test-results',
  use: { baseURL: process.env.E2E_BASE_URL || 'http://127.0.0.1:3100', channel: 'chrome', screenshot: 'only-on-failure' },
  projects: [{ name: 'desktop', use: { ...devices['Desktop Chrome'] } }] });
