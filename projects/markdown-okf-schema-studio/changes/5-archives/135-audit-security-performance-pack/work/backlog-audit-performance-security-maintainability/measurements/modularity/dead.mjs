import fs from "node:fs";import path from "node:path";
function walk(d,o=[]){for(const f of fs.readdirSync(d,{withFileTypes:true})){const p=path.join(d,f.name);if(f.isDirectory()){if(f.name!=="node_modules")walk(p,o)}else if(/\.(ts|mjs|cjs|js)$/.test(p))o.push(p)}return o}
const src=walk("src").filter(f=>f.endsWith(".ts"));const all=[...src,...walk("test"),...walk("scripts")];
const txt=Object.fromEntries(all.map(f=>[f,fs.readFileSync(f,"utf8")]));
const out=[];
for(const f of src){const t=txt[f];for(const m of t.matchAll(/^export (?:async )?(?:function|const|class|interface|type|enum) (\w+)/gm)){const n=m[1];if(/ForTests?$/.test(n)||/markers/i.test(f))continue;
const re=new RegExp("\\b"+n+"\\b");let ext=false,local=0;for(const g of all){if(g===f){local=(t.match(new RegExp("\\b"+n+"\\b","g"))||[]).length;continue}if(re.test(txt[g])){ext=true;break}}
if(!ext)out.push(`${f}:${t.slice(0,m.index).split("\n").length} ${n} (uses in file: ${local})`)}}
console.log(out.length);console.log(out.join("\n"));
