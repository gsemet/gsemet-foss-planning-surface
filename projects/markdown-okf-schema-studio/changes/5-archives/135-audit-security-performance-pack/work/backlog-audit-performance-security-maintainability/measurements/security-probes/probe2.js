const R='/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/out/src/';
const {renderMyst}=require(R+'core/render/mystRenderer.js');
const ws=__dirname+'/ws';
const ps=['<script src="x.js"></script>\n','<div>\n<script src="x.js"></script>\n</div>\n','<b onclick=1>x</b> <a href="https://e">p</a> <span style="color:red">r</span>\n','<details>\n<summary>s</summary>\n\n<img src="x.js" onerror=1>\n</details>\n','<kbd>a</kbd> <img src="x.png">\n'];
(async()=>{for(const p of ps){const r=await renderMyst(p,{documentPath:ws+'/doc.md',workspaceRoot:ws});console.log(JSON.stringify(p),'=>',r.html.slice(0,300));}})();
