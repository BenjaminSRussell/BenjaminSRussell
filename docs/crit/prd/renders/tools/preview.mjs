// Render README.md the way GitHub roughly does (dark + light). Review round 6: at a 1280 px viewport, since the README serves the phone sheet up to 1199 px
import { marked } from '/tmp/claude-0/-home-user-BenjaminSRussell/707a62e9-865e-57a2-81be-b65fd4820b14/scratchpad/tools/node_modules/marked/lib/marked.esm.js';
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import path from 'node:path';

const [,, readmePath, outDir, repoRoot] = process.argv;
const md = fs.readFileSync(readmePath, 'utf8');
// Rewrite raw.githubusercontent URLs for this repo (main branch) to local files so unpushed assets render.
const local = md.replace(/https:\/\/raw\.githubusercontent\.com\/BenjaminSRussell\/BenjaminSRussell\/main\//g, 'file://' + path.resolve(repoRoot) + '/');
const local9 = local.replace(/https:\/\/raw\.githubusercontent\.com\/BenjaminSRussell\/BenjaminSRussell\/chart\//g, 'file://' + path.resolve(repoRoot) + '/');
const body = marked.parse(local9, { gfm: true });
const css = (dark) => `
  :root{color-scheme:${dark?'dark':'light'}}
  body{margin:0;background:${dark?'#0d1117':'#ffffff'};color:${dark?'#e6edf3':'#1f2328'};font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif}
  .wrap{max-width:1012px;margin:0 auto;padding:32px}
  .md{border:1px solid ${dark?'#30363d':'#d0d7de'};border-radius:6px;padding:32px}
  h1{font-size:2em;border-bottom:1px solid ${dark?'#21262d':'#d8dee4'};padding-bottom:.3em;margin:.67em 0}
  h2{font-size:1.5em;border-bottom:1px solid ${dark?'#21262d':'#d8dee4'};padding-bottom:.3em;margin-top:24px}
  h3{font-size:1.25em} a{color:${dark?'#4493f8':'#0969da'};text-decoration:none} a:hover{text-decoration:underline}
  img{max-width:100%;box-sizing:border-box;background:${dark?'#0d1117':'#fff'}}
  code{background:${dark?'rgba(110,118,129,.4)':'rgba(175,184,193,.2)'};padding:.2em .4em;border-radius:6px;font:85% ui-monospace,SFMono-Regular,Menlo,monospace}
  pre{background:${dark?'#161b22':'#f6f8fa'};padding:16px;border-radius:6px;overflow:auto} pre code{background:none;padding:0}
  table{border-collapse:collapse} td,th{border:1px solid ${dark?'#30363d':'#d0d7de'};padding:6px 13px}
  details{margin:8px 0} summary{cursor:pointer} blockquote{border-left:.25em solid ${dark?'#3d444d':'#d0d7de'};color:${dark?'#8b949e':'#59636e'};margin:0;padding:0 1em}
  hr{border:0;border-top:1px solid ${dark?'#30363d':'#d0d7de'};height:0;margin:24px 0} sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}sub{bottom:-.25em}sup{top:-.5em}
  kbd{font:11px ui-monospace,monospace;background:${dark?'#161b22':'#f6f8fa'};border:1px solid ${dark?'#3d444d':'#d1d9e0'};border-bottom-color:${dark?'#3d444d':'#d1d9e0'};box-shadow:inset 0 -1px 0 ${dark?'#3d444d':'#d1d9e0'};border-radius:6px;padding:3px 5px}
`;
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch();
for (const dark of [true, false]) {
  const html = `<!doctype html><meta charset=utf-8><style>${css(dark)}</style><div class=wrap><div class=md>${body}</div></div>`;
  const file = path.join(outDir, `readme-${dark?'dark':'light'}.html`);
  fs.writeFileSync(file, html);
  const ctx = await browser.newContext({ colorScheme: dark ? 'dark' : 'light', viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve(file));
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(outDir, `readme-${dark?'dark':'light'}.png`), fullPage: true });
  await ctx.close();
}
await browser.close();
console.log('done');
