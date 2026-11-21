const W = process.argv[2];
globalThis.localStorage = { d:{}, getItem(k){return this.d[k]??null}, setItem(k,v){this.d[k]=String(v)}, removeItem(k){delete this.d[k]} };
globalThis.location = { search: '' };
const { kanbanBlock } = await import(`file:///${W}/js/views/batch-kanban.js`);
const rows = [
 {cr:'CR-430',stage:'1-pending',state:'queued',folder:'a'},{cr:'CR-425',stage:'1-pending',state:'queued'},
 {cr:'CR-428',stage:'2-actives',state:'blocked',folder:"1-pending/428-x"},{cr:'CR-410',stage:'2-actives',state:'working'},
 {cr:'CR-401',stage:'3-done',merged_at:'2026-11-20T10:00',state:'merged'},{cr:'CR-402',stage:'3-done',merged_at:'2026-11-21T10:00',state:'merged'},
 {cr:'CR-403',stage:'3-done',state:'merged'},{cr:'CR-499',stage:'0-inbox',state:'cancelled'},{cr:'CR-498',state:'cancelled'}];
const out = String(kanbanBlock({data:{batch:{crs:rows}}}, rows));
for (const k of ['bcol-pending','bcol-actives','bcol-done']) {
  const i = out.indexOf(`data-key="${k}"`); console.log(k, i>=0);
}
console.log([...out.matchAll(/CR-\d+/g)].map(m=>m[0]).filter((v,i,a)=>a.indexOf(v)===i).join(' '));
console.log('bkanban', out.includes('class="kanban bkanban"'));
const r = await import(`file:///${W}/js/core/router.js`);
const projects=[{id:'p'}]; r.configure(['home','batch'],['home']);
console.log('TABS', r.TABS.join());
console.log('resolve no t, nothing kept:', r.resolve(projects,'?p=p&v=batch').tab);
localStorage.setItem('chantier.batchTab','graph');
console.log('resolve no t, kept graph:', r.resolve(projects,'?p=p&v=batch').tab);
console.log('resolve t=kanban:', r.resolve(projects,'?p=p&v=batch&t=kanban').tab);
console.log('href kanban:', r.href({project:'p',view:'batch',tab:'kanban'}));
console.log('href home:', r.href({project:'p',view:'home',tab:'graph'}));
console.log('tabOf from home, kept graph:', r.tabOf({}, {view:'home',project:'p',batchTab:'kanban'}, 'p','batch'));
console.log('tabOf batch navigator:', r.tabOf({}, {view:'batch',project:'p',batchTab:'gantt'}, 'p','batch'));
