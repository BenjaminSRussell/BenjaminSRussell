#!/usr/bin/env node
// perf_check.js — 12's SVG-in-<img> rendering-cost harness with a warm-up and the MASTERPLAN 7.3 budget.
//
// Usage: node scripts/perf_check.js <svg>... [--warm=S] [--seconds=S] [--width=PX] [--dpr=N]
//                                   [--json[=path]] [--class=NAME] [--static] [--offscreen] [--no-fail]
//   --warm     seconds to wait after load before tracing (opening_end+2: hero 30, approaches 44, log 50, footer 66)
//   --seconds  trace length (default 6)
//   --width    <img width> in CSS px (870 = README column, 360 = phone)
//   --dpr      deviceScaleFactor (3 for the phone run)
//   --json     print machine-readable rows (or write them to a file)
//   --class    override the budget class inferred from the filename
//              (frozen | hero | approaches | log | footer | hero-phone | none)
//   --static   strip every <animate*>/<set> first (12's baseline)
//   --no-fail  report budget failures without a non-zero exit
//
// Repaints = ProxyMain::BeginMainFrame count in the trace window (12's "repaints"); ms/frame = raster + paint
// per repaint. Budget (7.3, binding): frozen 0 repaints after warm; hero ≤ 1/s; approaches ≤ 2/s; log ≤ 2/s;
// footer raster+paint ≤ 4 ms/frame; nothing over 8 ms/frame while moving after its opening; hero-phone at
// 360 px DPR 3 ≤ 0.25/s after 6 s. Chromium only until `playwright install` is permitted.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'); const path = require('path'); const os = require('os');

const args = process.argv.slice(2);
const opt = { width: 870, seconds: 6, warm: 0, dpr: 1, static: false, offscreen: false, json: false, jsonPath: null, cls: null, fail: true };
const files = [];
for (const a of args) {
  const kv = (k) => a.startsWith(k + '=') ? a.slice(k.length + 1) : null;
  let v;
  if ((v = kv('--width')) !== null) opt.width = +v;
  else if ((v = kv('--seconds')) !== null) opt.seconds = +v;
  else if ((v = kv('--warm')) !== null) opt.warm = +v;
  else if ((v = kv('--dpr')) !== null) opt.dpr = +v;
  else if ((v = kv('--class')) !== null) opt.cls = v;
  else if ((v = kv('--json')) !== null) { opt.json = true; opt.jsonPath = v; }
  else if (a === '--json') opt.json = true;
  else if (a === '--static') opt.static = true;
  else if (a === '--offscreen') opt.offscreen = true;
  else if (a === '--no-fail') opt.fail = false;
  else if (a.startsWith('--')) { console.error(`unknown flag ${a}`); process.exit(2); }
  else files.push(a);
}
if (!files.length) { console.error('usage: node scripts/perf_check.js <svg>... [--warm=S] [--seconds=S] [--width=PX] [--dpr=N] [--json] [--class=NAME]'); process.exit(2); }

const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

function stripAnim(svg) { return svg.replace(/<(animate|animateTransform|animateMotion|set)\b[^>]*?(\/>|>[\s\S]*?<\/\1>)/g, ''); }

// Budget class from the filename: {sheet}-{day|night}[-still][-phone].svg or legacy names.
function classify(file, o) {
  if (o.cls) return o.cls;
  const b = path.basename(file).toLowerCase();
  const sheet = b.split(/[-.]/)[0];
  if (b.includes('-still') || o.static) return 'frozen';
  if (b.includes('phone')) return sheet === 'hero' ? 'hero-phone' : 'frozen';
  if (['soundings', 'instruments', 'legend'].includes(sheet)) return 'frozen';
  if (['hero', 'approaches', 'log', 'footer'].includes(sheet)) return sheet;
  return 'none';
}

// MASTERPLAN 7.3 budget evaluator. row has repaintsPerS, msPerFrame (raster+paint), maxFrameMs.
function evaluate(cls, row) {
  const reasons = [];
  const rate = row.repaintsPerS, ms = row.msPerFrame;
  switch (cls) {
    case 'frozen': if (row.frames > 0) reasons.push(`frozen sheet repainted ${row.frames}× after warm`); break;
    case 'hero': if (rate > 1.0) reasons.push(`hero ${rate.toFixed(2)} repaints/s > 1`); break;
    case 'approaches': if (rate > 2.0) reasons.push(`approaches ${rate.toFixed(2)} repaints/s > 2`); break;
    case 'log': if (rate > 2.0) reasons.push(`log ${rate.toFixed(2)} repaints/s > 2`); break;
    case 'footer': if (ms !== null && ms > 4.0) reasons.push(`footer ${ms.toFixed(2)} ms/frame > 4`); break;
    case 'hero-phone': if (rate > 0.25) reasons.push(`hero-phone ${rate.toFixed(2)} repaints/s > 0.25`); break;
    default: break;
  }
  if (cls !== 'footer' && cls !== 'none' && ms !== null && ms > 8.0 && row.frames > 2) {
    reasons.push(`${ms.toFixed(1)} ms/frame while moving after the opening (cap 8)`);
  }
  return { pass: reasons.length === 0, reasons };
}

(async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'svgperf-'));
  const launch = { args: ['--no-sandbox', '--disable-gpu-vsync'] };
  if (fs.existsSync(CHROME)) launch.executablePath = CHROME;
  const b = await chromium.launch(launch);
  const ctx = await b.newContext({ viewport: { width: Math.max(1000, opt.width + 40), height: 900 }, deviceScaleFactor: opt.dpr });
  const page = await ctx.newPage();
  const rows = [];
  let failed = 0;
  for (const f of files) {
    let svg = fs.readFileSync(f, 'utf8');
    if (opt.static) svg = stripAnim(svg);
    const svgPath = path.join(tmp, path.basename(f));
    fs.writeFileSync(svgPath, svg);
    const spacer = opt.offscreen ? '<div style="height:3000px"></div>' : '';
    const html = `<!doctype html><html><body style="margin:0;background:#fff">${spacer}<img id="i" src="file://${svgPath}" width="${opt.width}"></body></html>`;
    const htmlPath = path.join(tmp, 'h.html'); fs.writeFileSync(htmlPath, html);
    await page.goto('about:blank');
    const t0 = Date.now();
    await page.goto('file://' + htmlPath, { waitUntil: 'load' });
    const decodeMs = await page.evaluate(async () => { const i = document.getElementById('i'); const s = performance.now(); try { await i.decode(); } catch (e) {} return performance.now() - s; });
    const loadMs = Date.now() - t0;
    await page.waitForTimeout(400 + opt.warm * 1000);
    await b.startTracing(page, { categories: ['devtools.timeline', 'disabled-by-default-devtools.timeline', 'disabled-by-default-devtools.timeline.frame', 'blink', 'cc'] });
    await page.waitForTimeout(opt.seconds * 1000);
    const buf = await b.stopTracing();
    const ev = JSON.parse(buf.toString()).traceEvents;
    const sum = {}; const cnt = {}; const frameCosts = [];
    for (const e of ev) {
      if (e.ph !== 'X' || !e.dur) continue;
      sum[e.name] = (sum[e.name] || 0) + e.dur / 1000; cnt[e.name] = (cnt[e.name] || 0) + 1;
      if (e.name === 'RasterTask' || e.name === 'Paint') frameCosts.push(e.dur / 1000);
    }
    const g = n => (sum[n] || 0);
    const paint = g('Paint') + g('PaintImage') + g('Paint::ImagePaint');
    const raster = g('RasterTask') + g('Decode Image') + g('ImageDecodeTask');
    const mainMisc = g('UpdateLayerTree') + g('PrePaint') + g('Layerize') + g('Layout') + g('CompositeLayers') + g('Animation') + g('HitTest');
    const frames = cnt['ProxyMain::BeginMainFrame'] || 0; const rasterTasks = cnt['RasterTask'] || 0;
    const msPerFrame = frames ? (paint + raster) / frames : null;
    const cls = classify(f, opt);
    const row = {
      file: path.basename(f), class: cls, kb: +(fs.statSync(f).size / 1024).toFixed(0), width: opt.width, dpr: opt.dpr,
      static: opt.static, offscreen: opt.offscreen, warmS: opt.warm, sec: opt.seconds, loadMs, decodeMs: +decodeMs.toFixed(0),
      frames, repaintsPerS: +(frames / opt.seconds).toFixed(3), rasterTasks,
      paintMs: +paint.toFixed(1), rasterMs: +raster.toFixed(1), mainOtherMs: +mainMisc.toFixed(1),
      paintPerFrame: frames ? +(paint / frames).toFixed(2) : null, rasterPerFrame: frames ? +(raster / frames).toFixed(2) : null,
      msPerFrame: msPerFrame === null ? null : +msPerFrame.toFixed(2),
      maxFrameMs: frameCosts.length ? +Math.max(...frameCosts).toFixed(2) : 0,
      cpuPct: +(((paint + raster + mainMisc) / (opt.seconds * 1000)) * 100).toFixed(1),
    };
    const verdict = evaluate(cls, row);
    row.pass = verdict.pass; row.reasons = verdict.reasons;
    if (!verdict.pass) failed++;
    rows.push(row);
    const top = Object.entries(sum).sort((a, b2) => b2[1] - a[1]).slice(0, 6).map(([k, v]) => `${k}=${v.toFixed(0)}ms×${cnt[k]}`).join(' ');
    console.error(`${row.file} [${cls}] warm ${opt.warm}s trace ${opt.seconds}s @${opt.width}px dpr${opt.dpr}: ` +
      `${frames} repaints (${row.repaintsPerS}/s), ${row.msPerFrame === null ? '-' : row.msPerFrame + ' ms/frame'}, cpu ${row.cpuPct}% → ${verdict.pass ? 'PASS' : 'FAIL ' + verdict.reasons.join('; ')}`);
    console.error(`  top: ${top}`);
  }
  await b.close();
  const out = JSON.stringify(rows, null, 1);
  if (opt.jsonPath) { fs.writeFileSync(opt.jsonPath, out); console.error(`wrote ${opt.jsonPath}`); }
  if (opt.json || !opt.jsonPath) console.log(out);
  process.exit(failed && opt.fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
