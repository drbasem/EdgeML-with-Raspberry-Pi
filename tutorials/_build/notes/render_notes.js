// usage: node render_notes.js input.html outPrefix   -> outPrefix.pdf and outPrefix_p{N}.png (A4 @ 300 dpi)
const { chromium } = require("/opt/node22/lib/node_modules/playwright");
const path = require("path"), fs = require("fs");
(async () => {
  const [input, prefix] = process.argv.slice(2);
  const exe = fs.readdirSync("/opt/pw-browsers").filter(d => d.startsWith("chromium-"))[0];
  const browser = await chromium.launch({ executablePath: `/opt/pw-browsers/${exe}/chrome-linux/chrome`, args: ["--no-sandbox", "--allow-file-access-from-files"] });
  const ctx = await browser.newContext({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 300 / 96 });
  const page = await ctx.newPage();
  await page.goto("file://" + path.resolve(input));
  await page.waitForFunction(() => document.body.dataset.ready === "1", null, { timeout: 30000 });
  await page.waitForTimeout(500);
  await page.pdf({ path: prefix + ".pdf", format: "A4", printBackground: true, preferCSSPageSize: true });
  const pages = await page.$$(".pg");
  for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: `${prefix}_p${i + 1}.png` });
  console.log("pages:", pages.length);
  await browser.close();
})();
