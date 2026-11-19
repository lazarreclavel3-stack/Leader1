// List job cards on Built In search pages: node links.js URL...
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for (const u of process.argv.slice(2)){await p.goto(u,{waitUntil:'domcontentloaded',timeout:45000});await p.waitForTimeout(3000);
const r=await p.$$eval('[data-id="job-card"], div.job-bounded-responsive, div[id^="job-card"]',els=>els.map(e=>{const a=e.querySelector('a[href*="/job/"]');return e.innerText.replace(/\s*\n\s*/g,' | ').slice(0,220)+' -> '+(a?a.href:'')}));
console.log('=== '+u);console.log(r.join('\n'));}
await b.close();})();
