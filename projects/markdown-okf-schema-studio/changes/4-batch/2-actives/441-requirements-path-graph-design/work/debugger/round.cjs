const path=require("path");const R=process.cwd();
const {chromium}=require(path.join(R,"node_modules/playwright-core"));
const {pinSiteFonts}=require(path.join(R,"out/test/page/pinnedFont"));
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.setContent("<p style='font:italic 13.5px \"Studio Test Serif\"'>x</p>");await pinSiteFonts(p);
const r=await p.evaluate(async()=>{await document.fonts.load('italic 13.5px "Studio Test Serif"');const c=document.createElement("canvas").getContext("2d");c.font='italic 13.5px "Studio Test Serif"';
const t="a long word, URL or Japanese, Chinese or Korean paragraph wraps in";let ex=0,ro=0,ce=0;for(const ch of t){const w=c.measureText(ch).width;ex+=w;ro+=Math.round(w);ce+=Math.ceil(w);}
return {whole:c.measureText(t).width,ex,ro,ce,n:t.length,est:t.length*6.4};});console.log(r);await b.close();})();
