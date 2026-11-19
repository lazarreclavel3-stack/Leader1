// Full Built In job description + apply links: node full.js URL
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();const u=process.argv[2];
await p.goto(u,{waitUntil:'domcontentloaded',timeout:45000});await p.waitForTimeout(2500);
const btn=await p.$('text=Read Full Description'); if(btn){await btn.click().catch(()=>{});await p.waitForTimeout(1000);}
console.log((await p.innerText('main')).replace(/\n\s*\n/g,'\n'));
const a=await p.$$eval('a',els=>els.map(e=>e.innerText.trim()+' -> '+e.href).filter(s=>/apply/i.test(s)));console.log(a.join('\n'));
await b.close();})();
