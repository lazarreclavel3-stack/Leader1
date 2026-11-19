// Dump page text: node pg.js URL...
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for (const u of process.argv.slice(2)){try{await p.goto(u,{waitUntil:'domcontentloaded',timeout:45000});await p.waitForTimeout(3000);
console.log('=== '+u);console.log((await p.innerText('body')).replace(/\n\s*\n/g,'\n').slice(0,12000));}catch(e){console.log('ERR '+u+' '+e.message)}}
await b.close();})();
