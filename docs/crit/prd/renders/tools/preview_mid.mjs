// Review round 12: the README at a two-column viewport (an iPad held sideways at 1180, a laptop window at 900). The
// viewport is `width`, so the <picture> media queries see it; the README column is GitHub's (checks/column.py
// column_px: vw - 370 from 768 to 1011, vw - 434 from 1012 to 1279), right of a blank sidebar, with GitHub's box.
import { marked } from '/tmp/claude-0/-home-user-BenjaminSRussell/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/tools/node_modules/marked/lib/marked.esm.js';
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
const [,, readmePath, outDir, repoRoot, width = '1180', height = '820'] = process.argv;
const vw = +width;
const col = vw <= 767 ? vw - 82 : vw <= 1011 ? vw - 370 : vw <= 1279 ? vw - 434 : 846;
const md = fs.readFileSync(readmePath, 'utf8')
  .replace(/https:\/\/raw\.githubusercontent\.com\/BenjaminSRussell\/BenjaminSRussell\/chart\//g, 'file://' + path.resolve(repoRoot) + '/');
const body = marked.parse(md, { gfm: true });
const html = `<!doctype html><meta charset=utf-8><style>body{margin:0;background:#fff;color:#1f2328;font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}
.side{position:absolute;left:0;top:0;width:${vw - col - 82}px;height:100%;background:#f6f8fa}
.md{position:absolute;left:${vw - col - 66}px;top:24px;width:${col}px;padding:24px;border:1px solid #d0d7de;border-radius:6px;box-sizing:content-box}
img{max-width:100%}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}sub{bottom:-.25em}
pre{background:#f6f8fa;padding:16px;border-radius:6px;overflow:auto}code{font:85% ui-monospace,SFMono-Regular,Menlo,monospace}pre code{white-space:pre}</style>
<div class=side></div><div class=md>${body}</div>`;
fs.mkdirSync(outDir, { recursive: true });
const file = path.join(outDir, `readme-${vw}.html`);
fs.writeFileSync(file, html);
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: vw, height: +height }, deviceScaleFactor: 1 });
const p = await ctx.newPage();
await p.goto('file://' + path.resolve(file));
await p.waitForTimeout(1500);
const img = await p.evaluate(() => { const i = document.querySelector('img'); const r = i.getBoundingClientRect(); return [i.currentSrc.split('/').pop(), Math.round(r.width), Math.round(r.height), Math.round(r.top)]; });
await p.screenshot({ path: path.join(outDir, `readme-${vw}-screen.png`) });
await b.close();
console.log(JSON.stringify({ vw, col, img }));
