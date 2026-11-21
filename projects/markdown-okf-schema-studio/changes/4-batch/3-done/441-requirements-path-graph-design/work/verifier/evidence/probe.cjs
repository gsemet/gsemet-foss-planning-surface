const path=require("node:path"),fs=require("node:fs"),url=require("node:url");
const root=path.resolve(__dirname,"../..");
const {chromium}=require(path.join(root,"node_modules/playwright-core"));
const site=path.join(root,"out/graphlab/site");
const model=JSON.parse(fs.readFileSync(path.join(root,"out/reports/requirements/requirements-report.json"),"utf8"));
const ids=["BLOCK-003","FMSCHEMA-014","BLOCK-014","MYST-006","REVIEW-012","MYST-009"];
const files={};const walk=d=>{for(const f of fs.readdirSync(d,{withFileTypes:true})){const p=path.join(d,f.name);if(f.isDirectory())walk(p);else if(f.name==="index.html"&&p.includes("StRS-MDOKFSTUDIO-"))for(const i of ids)if(p.includes("StRS-MDOKFSTUDIO-"+i+path.sep)||p.endsWith("StRS-MDOKFSTUDIO-"+i+path.sep+"index.html"))files[i]=p;}};
walk(path.join(site,"requirements"));
(async()=>{const b=await chromium.launch();
for(const w of [1280,800]){const pg=await b.newPage({viewport:{width:w,height:900}});
for(const i of ids){await pg.goto(url.pathToFileURL(files[i]).href);
const r=await pg.evaluate(()=>{const svg=document.querySelector("svg.metro");const names={};svg.querySelectorAll("circle").forEach(c=>{});
const st=[...svg.querySelectorAll(".st")];const labels=st.map(s=>(s.querySelector("text")||{}).textContent);const dup=labels.filter((l,i)=>labels.indexOf(l)!==i);
return{docW:document.documentElement.scrollWidth,winW:innerWidth,states:st.length,join:svg.querySelectorAll(".st.join, .join").length,dupLabels:dup.length,svgW:svg.getBoundingClientRect().width,attrW:svg.getAttribute("width"),mapScroll:document.querySelector(".map").scrollWidth+">"+document.querySelector(".map").clientWidth}});
console.log(w,i,JSON.stringify(r));}
await pg.close();}
await b.close();})();
