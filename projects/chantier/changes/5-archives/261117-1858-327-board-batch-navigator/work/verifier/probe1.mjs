import { launch, page } from './cdp.mjs';
const K = process.argv[2];
const b = await launch(process.argv[3]);
const pg = await page(b, `http://127.0.0.1:8791/?k=${K}`);
console.log(await pg.ev('location.href'));
console.log(await pg.ev('document.title + " | " + document.getElementById("title").textContent'));
console.log(await pg.ev('JSON.stringify(document.getElementById("sidebar")?.innerText||document.body.innerText.slice(0,500))'));
console.log(await pg.ev('fetch("/api/board").then(r=>r.json()).then(j=>JSON.stringify(j).slice(0,500))'));
b.proc.kill(); process.exit(0);
