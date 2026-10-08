#!/usr/bin/env node
// render.mjs — Playwright renders for the still-frame gate (MASTERPLAN 7.2) and the silhouette test.
//
//   node scripts/render.mjs frames <svg> <outdir> t1,t2,...  [--still <svg>] [--width 1280] [--strip <png>] [--json <path>]
//       Inline the SVG, `svg.pauseAnimations(); svg.setCurrentTime(t)`, screenshot each instant to
//       <outdir>/frame-<t>.png. With --still, compares each frame to the still edition: ink coverage
//       ink(F)/ink(S) (ink = pixels farther than ~ΔE 3 from paper), changed-pixel fraction, and the
//       blank-ledger test (fraction of 8×8 cells that have text/ink in S but are empty in F).
//       --strip writes a contact strip of all frames (for looking at).
//   node scripts/render.mjs silhouette <svg...> [--out <dir>]
//       128 px thumbnails (frozen state), grey → threshold → 16×8 mass grid, pairwise L1 (≥ 0.25 passes).
//   node scripts/render.mjs phone <svg> <out.png> [--width 360] [--dpr 3]
//   node scripts/render.mjs matrix        placeholder (T10's source matrix; needs the README preview page)
//
// No image library: pixels are read in the page through a <canvas>, so Playwright is the only dependency.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
let pw;
try { pw = require('/opt/node-tools/node_modules/playwright'); } catch { pw = require('playwright'); }
const { chromium } = pw;

const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const argv = process.argv.slice(2);
const cmd = argv.shift();

function flag(name, dflt) {
  const i = argv.indexOf(name);
  if (i < 0) return dflt;
  const v = argv[i + 1];
  argv.splice(i, 2);
  return v === undefined ? true : v;
}
function usage() {
  console.error('usage: render.mjs frames <svg> <outdir> t1,t2,... [--still <svg>] [--width 1280] [--strip <png>] [--json <path>]\n' +
    '       render.mjs silhouette <svg...> [--out <dir>]\n       render.mjs phone <svg> <out.png> [--width 360] [--dpr 3]\n       render.mjs matrix');
  process.exit(2);
}

async function launch(dpr = 1, width = 1400, height = 1000) {
  const o = { args: ['--no-sandbox'] };
  if (fs.existsSync(CHROME)) o.executablePath = CHROME;
  const browser = await chromium.launch(o);
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: dpr });
  const page = await ctx.newPage();
  return { browser, page };
}

function inlineSvg(file) {
  let s = fs.readFileSync(file, 'utf8');
  s = s.replace(/^\s*<\?xml[^>]*\?>\s*/, '').replace(/<!DOCTYPE[^>]*>/i, '');
  return s;
}
function svgSize(svg) {
  const vb = svg.match(/viewBox="\s*([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)\s+([\d.-]+)"/);
  if (vb) return { w: +vb[3], h: +vb[4] };
  const w = svg.match(/<svg[^>]*\swidth="([\d.]+)/), h = svg.match(/<svg[^>]*\sheight="([\d.]+)/);
  return { w: w ? +w[1] : 1280, h: h ? +h[1] : 720 };
}
function pageHtml(svg, width) {
  const { w, h } = svgSize(svg);
  const height = Math.round(width * h / w);
  return `<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#fff}#wrap{width:${width}px;height:${height}px;overflow:hidden}#wrap>svg{width:${width}px;height:${height}px;display:block}</style></head><body><div id="wrap">${svg}</div></body></html>`;
}

// Run inside the page: pixel statistics of the wrapper's screenshot (passed back in as a data URL).
const PIXELS_FN = `async (dataUrl, grid) => {
  const img = new Image(); img.src = dataUrl; await img.decode();
  const c = document.createElement('canvas'); c.width = img.naturalWidth; c.height = img.naturalHeight;
  const g = c.getContext('2d', { willReadFrequently: true }); g.drawImage(img, 0, 0);
  const d = g.getImageData(0, 0, c.width, c.height).data;
  // paper colour: the most common colour among the border pixels
  const hist = new Map();
  const bump = (i) => { const k = (d[i] << 16) | (d[i + 1] << 8) | d[i + 2]; hist.set(k, (hist.get(k) || 0) + 1); };
  for (let x = 0; x < c.width; x += 4) { bump(x * 4 + 8 * c.width * 4); bump(x * 4 + (c.height - 3) * c.width * 4); }
  for (let y = 0; y < c.height; y += 4) { bump(y * c.width * 4 + 8); bump(y * c.width * 4 + (c.width - 3) * 4); }
  let paper = 0, best = -1; for (const [k, v] of hist) if (v > best) { best = v; paper = k; }
  const pr = (paper >> 16) & 255, pg = (paper >> 8) & 255, pb = paper & 255;
  const [gx, gy] = grid; const cells = new Float64Array(gx * gy); const cw = c.width / gx, ch = c.height / gy;
  let ink = 0; const n = c.width * c.height;
  const mask = new Uint8Array(n);
  for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) {
    const i = (y * c.width + x) * 4;
    const dr = d[i] - pr, dg = d[i + 1] - pg, db = d[i + 2] - pb;
    // ~ΔE 3 ≈ 8 RGB units of Euclidean distance on a light paper
    if (dr * dr + dg * dg + db * db > 64) { ink++; mask[y * c.width + x] = 1; cells[Math.floor(y / ch) * gx + Math.floor(x / cw)]++; }
  }
  return { w: c.width, h: c.height, paper: [pr, pg, pb], ink, inkFrac: ink / n, cells: Array.from(cells), mask: Array.from(mask) };
}`;

async function statsOf(page, pngBuffer, grid = [8, 8]) {
  const url = 'data:image/png;base64,' + pngBuffer.toString('base64');
  return page.evaluate(`(${PIXELS_FN})(${JSON.stringify(url)}, ${JSON.stringify(grid)})`);
}

async function frames() {
  const still = flag('--still', null);
  const width = +flag('--width', 1280);
  const strip = flag('--strip', null);
  const jsonOut = flag('--json', null);
  const [file, outdir, tlist] = argv;
  if (!file || !outdir || !tlist) usage();
  const times = tlist.split(',').map(Number);
  fs.mkdirSync(outdir, { recursive: true });
  const svg = inlineSvg(file);
  const { w, h } = svgSize(svg);
  const { browser, page } = await launch(1, width + 40, Math.round(width * h / w) + 40);
  const results = [];
  let stillStats = null, stillPng = null;
  if (still) {
    await page.setContent(pageHtml(inlineSvg(still), width), { waitUntil: 'load' });
    await page.evaluate(() => { const s = document.querySelector('#wrap>svg'); if (s && s.pauseAnimations) s.pauseAnimations(); });
    stillPng = await page.locator('#wrap').screenshot();
    fs.writeFileSync(path.join(outdir, 'still.png'), stillPng);
    stillStats = await statsOf(page, stillPng);
  }
  await page.setContent(pageHtml(svg, width), { waitUntil: 'load' });
  // pause as early as possible so no wall-clock advance leaks into the frames
  await page.evaluate(() => { const s = document.querySelector('#wrap>svg'); s.pauseAnimations(); s.setCurrentTime(0); });
  const pngs = [];
  for (const t of times) {
    await page.evaluate((tt) => { const s = document.querySelector('#wrap>svg'); s.pauseAnimations(); s.setCurrentTime(tt); }, t);
    await page.waitForTimeout(60);
    const png = await page.locator('#wrap').screenshot();
    const name = `frame-${String(t).replace('.', 'p')}.png`;
    fs.writeFileSync(path.join(outdir, name), png);
    pngs.push({ t, name, png });
    const st = await statsOf(page, png);
    const row = { t, file: name, inkFrac: +st.inkFrac.toFixed(4), paper: st.paper };
    if (stillStats) {
      row.coverage = +(st.ink / Math.max(stillStats.ink, 1)).toFixed(3);
      let changed = 0; const n = st.mask.length;
      for (let i = 0; i < n; i++) if (st.mask[i] !== stillStats.mask[i]) changed++;
      row.changedFrac = +(changed / n).toFixed(4);
      // blank-ledger: cells where the still has ink (> 0.5 % of the cell) but the frame has < 10 % of it
      let emptied = 0, inked = 0; const cellPx = (st.w * st.h) / st.cells.length;
      for (let i = 0; i < st.cells.length; i++) {
        if (stillStats.cells[i] > 0.005 * cellPx) { inked++; if (st.cells[i] < 0.1 * stillStats.cells[i]) emptied++; }
      }
      row.emptiedCellFrac = inked ? +(emptied / st.cells.length).toFixed(3) : 0;
      row.blankLedger = row.emptiedCellFrac > 0.25;
    }
    delete st.mask;
    results.push(row);
    console.error(`t=${t}s ink ${(st.inkFrac * 100).toFixed(2)}%` + (stillStats ? ` coverage ${row.coverage} changed ${(row.changedFrac * 100).toFixed(2)}% emptied ${row.emptiedCellFrac}` : ''));
  }
  if (strip) {
    const cells = pngs.map(p => `<figure style="margin:0 6px 0 0;text-align:center;font:12px monospace"><img src="data:image/png;base64,${p.png.toString('base64')}" style="width:${Math.floor(Math.min(420, 1800 / pngs.length))}px;display:block;border:1px solid #999"><figcaption>t=${p.t}s</figcaption></figure>`).join('');
    const extra = stillPng ? `<figure style="margin:0;text-align:center;font:12px monospace"><img src="data:image/png;base64,${stillPng.toString('base64')}" style="width:${Math.floor(Math.min(420, 1800 / pngs.length))}px;display:block;border:1px solid #c33"><figcaption>still</figcaption></figure>` : '';
    await page.setViewportSize({ width: 1900, height: 700 });
    await page.setContent(`<!doctype html><body style="margin:8px;background:#ddd;display:flex;align-items:flex-start">${cells}${extra}</body>`);
    const shot = await page.locator('body').screenshot();
    fs.writeFileSync(strip, shot);
    console.error(`wrote ${strip}`);
  }
  await browser.close();
  const out = { file, still, width, frames: results };
  if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(out, null, 1));
  console.log(JSON.stringify(out, null, 1));
}

async function silhouette() {
  const outdir = flag('--out', null);
  const files = argv;
  if (!files.length) usage();
  const { browser, page } = await launch(1, 400, 400);
  const grids = [];
  const thumbs = [];
  for (const f of files) {
    const svg = inlineSvg(f);
    const { w, h } = svgSize(svg);
    const W = 128, H = Math.max(1, Math.round(128 * h / w));
    await page.setContent(pageHtml(svg, W), { waitUntil: 'load' });
    await page.evaluate(() => { const s = document.querySelector('#wrap>svg'); if (s.pauseAnimations) { s.pauseAnimations(); s.setCurrentTime(600); } });
    const png = await page.locator('#wrap').screenshot();
    if (outdir) { fs.mkdirSync(outdir, { recursive: true }); fs.writeFileSync(path.join(outdir, path.basename(f, '.svg') + '-128.png'), png); }
    const st = await statsOf(page, png, [16, 8]);
    const total = st.cells.reduce((a, b) => a + b, 0) || 1;
    grids.push(st.cells.map(c => c / total));
    thumbs.push({ file: path.basename(f), w: W, h: H, inkFrac: +st.inkFrac.toFixed(4), heaviestTopLeft: st.cells.indexOf(Math.max(...st.cells)) === 0 });
  }
  const pairs = [];
  let minL1 = Infinity;
  for (let i = 0; i < files.length; i++) for (let j = i + 1; j < files.length; j++) {
    let l1 = 0; for (let k = 0; k < 128; k++) l1 += Math.abs(grids[i][k] - grids[j][k]);
    pairs.push({ a: path.basename(files[i]), b: path.basename(files[j]), l1: +l1.toFixed(3), pass: l1 >= 0.25 });
    minL1 = Math.min(minL1, l1);
  }
  await browser.close();
  const out = { thumbs, pairs, minL1: pairs.length ? +minL1.toFixed(3) : null, pass: pairs.every(p => p.pass) };
  console.log(JSON.stringify(out, null, 1));
  process.exitCode = out.pass ? 0 : 1;
}

async function phone() {
  const width = +flag('--width', 360);
  const dpr = +flag('--dpr', 3);
  const [file, out] = argv;
  if (!file || !out) usage();
  const svg = inlineSvg(file);
  const { w, h } = svgSize(svg);
  const { browser, page } = await launch(dpr, width, Math.round(width * h / w));
  await page.setContent(pageHtml(svg, width), { waitUntil: 'load' });
  await page.evaluate(() => { const s = document.querySelector('#wrap>svg'); if (s.pauseAnimations) { s.pauseAnimations(); s.setCurrentTime(600); } });
  const png = await page.locator('#wrap').screenshot();
  fs.mkdirSync(path.dirname(out) || '.', { recursive: true });
  fs.writeFileSync(out, png);
  await browser.close();
  console.log(JSON.stringify({ file, out, width, dpr }));
}

async function matrix() {
  console.log(JSON.stringify({ status: 'not implemented', note: 'source matrix (T10 check 21) needs the README preview page from render_readme.py; contexts 360/390/412/600/767/768/1024/1280 × DPR 1,3 × scheme × reduced-motion' }, null, 1));
}

const cmds = { frames, silhouette, phone, matrix };
if (!cmds[cmd]) usage();
cmds[cmd]().catch(e => { console.error(e); process.exit(1); });
