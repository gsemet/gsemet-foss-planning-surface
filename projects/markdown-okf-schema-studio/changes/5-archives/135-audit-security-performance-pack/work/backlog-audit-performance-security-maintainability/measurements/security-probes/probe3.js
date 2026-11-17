const R='/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/out/src/';
const {renderMyst}=require(R+'core/render/mystRenderer.js');
const {buildPreviewWebviewHtml}=require(R+'session/webview.js');
const ws=__dirname+'/ws';
const assets={cspSource:'vscode-res:',resourceUri:p=>'https://res/'+p,bundleUri:()=>undefined};
const ps=['[calc](https%3A/../../System/Applications/Calculator.app)','<table><tr><td><a href="javascript:alert(1)" onclick="x">a</a><img src=x onerror=1><script src="x.js"></script></td></tr></table>','<span style="color:red;background:url(https://e)">s</span> <kbd onclick=1>k</kbd>','<img src="x.js" onerror="alert(1)" width=1>'];
(async()=>{for(const p of ps){const r=await renderMyst(p+'\n',{sourcePath:ws+'/doc.md'});
const w=buildPreviewWebviewHtml(r.html,ws,assets,undefined,ws,undefined,undefined,true,true);
const m=w.html.match(/<main[\s\S]*?<\/main>/);console.log('IN :',p,'\nMYST:',r.html.slice(0,300),'\nOUT:',m[0].replace(/<main[^>]*>/,'').slice(0,400),'\n');}})().catch(e=>console.error(e));
