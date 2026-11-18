import { launch, page } from './cdp.mjs';
const K = process.argv[2];
const EV = process.argv[4];
const b = await launch(process.argv[3]);
const pg = await page(b, `http://127.0.0.1:8791/?k=${K}`);
const nav = () => pg.ev(`(()=>{const n=document.getElementById('batch-nav');const bs=[...n.querySelectorAll('button')].map(x=>x.textContent.trim()+(x.disabled?'(disabled)':''));return JSON.stringify({hidden:n.hidden,id:n.querySelector('.bn-id')?.textContent,bs,url:location.search})})()`);
const click = (sel) => pg.ev(`document.querySelector(${JSON.stringify(sel)}).click()`);
const log = async (l) => console.log(l.padEnd(28), await nav(), '| h1:', await pg.ev('document.getElementById("title").textContent'));
await pg.goto(`http://127.0.0.1:8791/?p=chantier&v=home`); await log('home');
await click('[data-view=costs]'); await pg.wait(); await log('costs (click sidebar)');
await pg.shot(EV + '/_t1.png');
await click('[data-batch-go]:first-of-type'); await pg.wait(); await log('prev x1');
await pg.ev(`document.querySelector('.bn-arrow').click()`); await pg.wait(); await log('prev x2');
console.log('ticket head:', await pg.ev(`document.querySelector('.ticket')?.innerText.slice(0,300)`));
await pg.goto(await pg.ev('location.href')); await log('reload same url');
await click('[data-view=batch]'); await pg.wait(); await log('-> batch view');
await click('[data-view=costs]'); await pg.wait(); await log('-> costs again');
await click('[data-view=kanban]'); await pg.wait(); await log('-> kanban'); 
await click('[data-view=costs]'); await pg.wait(); await log('-> costs back');
await pg.goto(`http://127.0.0.1:8791/?p=chantier&v=costs&b=batch-99`); await log('unknown b=batch-99');
await pg.goto(`http://127.0.0.1:8791/?p=chantier&v=costs&b=batch-01`); await log('b=batch-01');
console.log('ticket batch01:', await pg.ev(`document.querySelector('.ticket')?.innerText.slice(0,500)`));
console.log('detail heading:', await pg.ev(`[...document.querySelectorAll('*')].filter(e=>e.children.length==0&&/Détail|Detail/.test(e.textContent)).map(e=>e.textContent).join(' // ')`));
// go next to the end by clicking
for (let i=0;i<30;i++){ const d=await pg.ev(`(()=>{const x=[...document.querySelectorAll('.bn-arrow')][1];if(!x||x.disabled)return false;x.click();return true})()`); if(!d)break; await pg.wait(150);} await log('after > to the end');
// Latest pill then back
await pg.goto(`http://127.0.0.1:8791/?p=chantier&v=costs&b=batch-19`); await log('b=batch-19');
await click('.bn-pill'); await pg.wait(); await log('Latest clicked');
await pg.ev('history.back()'); await pg.wait(); await log('browser back');
// english
await pg.ev(`localStorage.setItem('lang','en')`);
console.log('lang keys:', await pg.ev(`JSON.stringify(Object.keys(localStorage))`));
b.proc.kill(); process.exit(0);
