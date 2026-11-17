import fs from "node:fs";import path from "node:path";
const root=process.cwd();
function walk(d,o=[]){for(const f of fs.readdirSync(d,{withFileTypes:true})){const p=path.join(d,f.name);if(f.isDirectory())walk(p,o);else if(p.endsWith(".ts"))o.push(p)}return o}
const files=walk("src");const set=new Set(files);const g={};
for(const f of files){const t=fs.readFileSync(f,"utf8");g[f]=new Set();
for(const m of t.matchAll(/(?:import|export)\s(?!type\s)[^;]*?from\s+"(\.[^"]*)"/g)){let r=path.join(path.dirname(f),m[1]).replace(/\.js$/,"");for(const c of [r+".ts",path.join(r,"index.ts")])if(set.has(c)){g[f].add(c);break}}}
const fin={};for(const f in g)for(const t of g[f])fin[t]=(fin[t]||0)+1;
const top=(o,n)=>Object.entries(o).sort((a,b)=>b[1]-a[1]).slice(0,n);
console.log("FAN-IN",top(fin,10));console.log("FAN-OUT",top(Object.fromEntries(Object.entries(g).map(([k,v])=>[k,v.size])),10));
// SCC tarjan
let idx=0,st=[],on=new Set(),ix={},low={},sccs=[];
function sc(v){ix[v]=low[v]=idx++;st.push(v);on.add(v);for(const w of g[v]){if(ix[w]===undefined){sc(w);low[v]=Math.min(low[v],low[w])}else if(on.has(w))low[v]=Math.min(low[v],ix[w])}
if(low[v]===ix[v]){const c=[];let w;do{w=st.pop();on.delete(w);c.push(w)}while(w!==v);if(c.length>1)sccs.push(c)}}
for(const v of files)if(ix[v]===undefined)sc(v);
console.log("SCCs",JSON.stringify(sccs,null,1));
