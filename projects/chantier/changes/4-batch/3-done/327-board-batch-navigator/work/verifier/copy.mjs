import { launch, page } from './cdp.mjs';
const K = process.argv[2]; const EV = process.argv[4];
const b = await launch(process.argv[3]);
await b.send('Browser.grantPermissions', { permissions: ['clipboardReadWrite', 'clipboardSanitizedWrite'] });
const pg = await page(b, `http://127.0.0.1:8791/?k=${K}`, 1280, 1000);
await pg.ev(`localStorage.setItem('chantier.lang','en')`);
await pg.goto(`http://127.0.0.1:8791/?p=chantier&v=costs`);
const click = (sel) => pg.ev(`document.querySelector(${JSON.stringify(sel)}).click()`);
await click('.bn-arrow'); await pg.wait();
console.log('lang', await pg.ev(`document.documentElement.lang`), 'h1', await pg.ev(`document.getElementById('title').textContent`));
console.log('detail', await pg.ev(`[...document.querySelectorAll('*')].filter(e=>e.children.length==0&&/Detail|Détail/.test(e.textContent)).map(e=>e.textContent).join('//')`));
console.log('nav', await pg.ev(`document.getElementById('batch-nav').innerText.replace(/\n/g,' ') + ' | aria: ' + [...document.querySelectorAll('#batch-nav [aria-label]')].map(x=>x.getAttribute('aria-label')).join(',') + ' nav aria ' + document.getElementById('batch-nav').getAttribute('aria-label')`));
console.log('secure', await pg.ev('window.isSecureContext'));
console.log('btn', await pg.ev(`(()=>{const x=document.querySelector('[data-copy-receipt]');return JSON.stringify({text:x.textContent,disabled:x.disabled,inTicket:!!x.closest('.ticket')})})()`));
await pg.shot(EV + '/_costs_en.png');
await click('[data-copy-receipt]'); await pg.wait(3000);
console.log('toast', await pg.ev(`document.querySelector('.toast, #toast, [role=status]')?.innerText`));
console.log('clip', await pg.ev(`navigator.clipboard.read().then(async items=>{const out=[];for(const it of items){for(const ty of it.types){const bl=await it.getType(ty);const bm=await createImageBitmap(bl);out.push({ty,size:bl.size,w:bm.width,h:bm.height})}}return JSON.stringify(out)}).catch(e=>'ERR '+e)`));
// save the clipboard image
const dataUrl = await pg.ev(`navigator.clipboard.read().then(async items=>{const bl=await items[0].getType('image/png');return await new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result);fr.readAsDataURL(bl)})})`);
import('node:fs').then(fs=>fs.writeFileSync(EV+'/_clip.png', Buffer.from(dataUrl.split(',')[1],'base64')));
await pg.wait(500);
// phone
const ph = await page(b, `http://127.0.0.1:8791/?p=chantier&v=costs`, 400, 900);
await ph.ev(`localStorage.setItem('chantier.lang','en')`); await ph.goto(`http://127.0.0.1:8791/?p=chantier&v=costs`);
await ph.shot(EV + '/_phone.png');
// non-secure origin
const lan = await page(b, `http://192.168.5.45:8791/?k=${K}`, 1280, 1000);
await lan.ev(`localStorage.setItem('chantier.lang','en')`); await lan.goto(`http://192.168.5.45:8791/?p=chantier&v=costs`);
await lan.ev(`document.querySelector('.bn-arrow').click()`); await lan.wait();
console.log('LAN secure', await lan.ev('window.isSecureContext'), await lan.ev('location.search'));
console.log('LAN btn', await lan.ev(`(()=>{const x=document.querySelector('[data-copy-receipt]');const w=x.closest('.tipwrap');return JSON.stringify({disabled:x.disabled,wrap:!!w,tabindex:w?.getAttribute('tabindex'),tip:w?.querySelector('.tip')?.innerText,href:w?.querySelector('.tip a')?.href})})()`));
await lan.ev(`document.querySelector('.tipwrap').focus()`); await lan.wait(300);
console.log('tip visible on focus', await lan.ev(`getComputedStyle(document.querySelector('.tipwrap .tip')).visibility+' '+getComputedStyle(document.querySelector('.tipwrap .tip')).opacity+' '+getComputedStyle(document.querySelector('.tipwrap .tip')).display`));
await lan.shot(EV + '/_lan.png');
b.proc.kill(); process.exit(0);
