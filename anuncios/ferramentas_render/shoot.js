const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2]));
  const browser = await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const page = await browser.newPage({viewport:{width:2400,height:2400}});
  page.on('console', m => { if (m.type()==='error') console.log('console:', m.text()); });
  page.on('pageerror', e => console.log('pageerror:', e.message));
  await page.goto('http://127.0.0.1:8765/index.html');
  await page.waitForFunction(() => window.ready === true, null, {timeout: 60000});
  for (const j of jobs) {
    const t = Date.now();
    const url = await page.evaluate(o => window.shot(o), j);
    fs.writeFileSync(j.out, Buffer.from(url.split(',')[1], 'base64'));
    console.log('ok', j.out, (Date.now()-t)+'ms');
  }
  await browser.close();
})();
