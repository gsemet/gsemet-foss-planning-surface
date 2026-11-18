// Ad-hoc check of the router's first load (round 4): a link with &b= keeps b.
// Run: node router-check.mjs file:///<worktree>/skills/chantier/scripts/cli/src/chantier/board/web/js
const store = new Map();
globalThis.localStorage = { getItem: (k) => store.get(k) ?? null, setItem: (k, v) => store.set(k, String(v)), removeItem: (k) => store.delete(k) };
let url = '?p=chantier&v=costs&b=batch-22';
globalThis.location = { get search() { return url; }, get href() { return `http://x/${url}`; } };
globalThis.history = { replaceState: (_s, _t, u) => { url = u; }, pushState: (_s, _t, u) => { url = u; } };
globalThis.window = { addEventListener() {} };
const base = process.argv[2];
const r = await import(`${base}/core/router.js`);
const s = await import(`${base}/core/store.js`);
r.configure(['home', 'kanban', 'costs', 'batch'], ['home']);
const projects = [{ id: 'chantier' }, { id: 'other' }];
s.update({ board: { projects } });
r.go(r.resolve(projects), { replace: true });
const out = [];
out.push(['fresh load', s.snapshot().batchId, url]);
r.go({ view: 'batch' });
out.push(['to batch', s.snapshot().batchId, url]);
r.go({ view: 'kanban' });
out.push(['to kanban', s.snapshot().batchId, url]);
r.go({ view: 'costs', batch: 'batch-21' });
out.push(['costs b=21', s.snapshot().batchId, url]);
r.go({ project: 'other' });
out.push(['other project', s.snapshot().batchId, url]);
for (const line of out) console.log(JSON.stringify(line));
const ok = out[0][1] === 'batch-22' && out[0][2].includes('b=batch-22') && out[1][1] === 'batch-22' && out[2][1] === null && out[3][1] === 'batch-21' && out[4][1] === null;
console.log(ok ? 'PASS' : 'FAIL');
process.exit(ok ? 0 : 1);
