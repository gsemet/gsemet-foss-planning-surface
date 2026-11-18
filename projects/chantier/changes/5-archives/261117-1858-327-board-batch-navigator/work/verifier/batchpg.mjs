import { launch, page } from './cdp.mjs';
const K = process.argv[2]; const EV = process.argv[4];
const b = await launch(process.argv[3]);
const pg = await page(b, `http://127.0.0.1:8791/?k=${K}`, 1280, 1000);
const click = (sel) => pg.ev(`document.querySelector(${JSON.stringify(sel)}).click()`);
const idNow = () => pg.ev(`document.querySelector('.bn-id')?.textContent`);
await pg.goto(`http://127.0.0.1:8791/?p=chantier&v=costs`);
async function to(id){ for(let i=0;i<30;i++){ if(await idNow()===id) return; await click('.bn-arrow'); await pg.wait(150);} }
async function dump(id){
  await click('[data-view=costs]'); await pg.wait(200);
  await to(id); await click('[data-view=batch]'); await pg.wait(500);
  console.log('=====', id, await pg.ev('location.search'));
  console.log(await pg.ev(`JSON.stringify({crumb:document.querySelector('#crumbs, .crumbs')?.innerText, notice:[...document.querySelectorAll('*')].filter(e=>e.children.length==0&&/Dépendances|Dependencies/.test(e.textContent)).map(e=>e.textContent), nodes:document.querySelectorAll('[data-cr], .gnode, .node').length, paths:document.querySelectorAll('svg path').length})`));
  console.log((await pg.ev(`document.querySelector('main, #view, .content')?.innerText.slice(0,900)`)));
}
await dump('batch-23'); await pg.shot(EV+'/_b23.png');
await dump('batch-18'); await pg.shot(EV+'/_b18.png');
await dump('batch-01'); await pg.shot(EV+'/_b01.png');
// Latest from batch page
await click('.bn-pill'); await pg.wait(); console.log('Latest on batch:', await pg.ev('location.search'));
b.proc.kill(); process.exit(0);
