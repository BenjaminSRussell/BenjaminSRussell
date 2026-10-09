#!/usr/bin/env node
// social.mjs — the social-preview PNGs: the hero's day and night editions rendered at 1280 px, written to social/.
//   node scripts/social.mjs [--out social] [--width 1280]
// GitHub's social preview is uploaded by hand (MASTERPLAN §5.12); the files ride the chart branch so the
// upload is one click from https://raw.githubusercontent.com/<login>/<login>/chart/social/hero-day.png.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('/opt/node-tools/node_modules/playwright'); } catch { pw = require('playwright'); }
const { chromium } = pw;
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const argv = process.argv.slice(2);
function flag(name, dflt) { const i = argv.indexOf(name); if (i < 0) return dflt; const v = argv[i + 1]; argv.splice(i, 2); return v; }
const out = flag('--out', 'social');
const width = +flag('--width', '1280');
fs.mkdirSync(out, { recursive: true });
const o = { args: ['--no-sandbox'] };
if (fs.existsSync(CHROME)) o.executablePath = CHROME;
const browser = await chromium.launch(o);
for (const [ed, bg] of [['day', '#ffffff'], ['night', '#0d1117']]) {
  // round 6: the hero does not move and ships no still editions; an older build's still is used if it is there
  const still = path.resolve('assets', 'v9', `hero-still-${ed}.svg`);
  const svg = fs.existsSync(still) ? still : path.resolve('assets', 'v9', `hero-${ed}.svg`);
  if (!fs.existsSync(svg)) { console.error(`missing ${svg}`); continue; }
  const html = path.join(out, `hero-${ed}.html`);
  fs.writeFileSync(html, `<!doctype html><body style="margin:0;background:${bg}"><img src="file://${svg}" style="width:${width}px;display:block"></body>`);
  const ctx = await browser.newContext({ viewport: { width, height: 200 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve(html));
  await page.waitForTimeout(300);
  const png = path.join(out, `hero-${ed}.png`);
  await page.screenshot({ path: png, fullPage: true });
  await ctx.close();
  fs.unlinkSync(html);
  console.log(`wrote ${png}`);
}
await browser.close();
