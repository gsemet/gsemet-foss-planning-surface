const R='/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/out/src/';
const {renderMyst}=require(R+'core/render/mystRenderer.js');
const {buildPreviewWebviewHtml}=require(R+'session/webview.js');
const ws=__dirname+'/ws';
const assets={cspSource:'vscode-res:',resourceUri:p=>'https://res/'+p,bundleUri:()=>undefined};
const payloads=[
 '<script src="x.js"></script>',
 '<a href="javascript:alert(1)">j</a> <a href="command:workbench.action.terminal.new">c</a>',
 '<img src=x onerror=alert(1)> <svg><a xlink:href="javascript:alert(1)"><text>t</text></a></svg>',
 '<math><mtext><table><mglyph><style><img src=x onerror=alert(2)></style></mglyph></table></mtext></math>',
 '<svg></p><title><a id="</title><img src=x onerror=alert(3)>"></a></title></svg>',
 '<form><button formaction="javascript:1">b</button></form><input name="acquireVsCodeApi" id="__proto__">',
 '<meta http-equiv="refresh " content="0;url=https://evil"><meta http-equiv="Content-Security-Policy" content="x">',
 '<svg><use href="data:image/svg+xml,<svg id=x xmlns=http://www.w3.org/2000/svg><a><image href=1 onerror=alert(4) /></a></svg>#x"/></svg>',
 '<noscript><p title="</noscript><img src=x onerror=alert(5)>"></noscript> <textarea></textarea><img src=x onerror=alert(6)></textarea>',
 '<details open ontoggle=alert(7)><summary>s</summary></details><a href="https://e" target="_blank" ping="https://e">p</a>',
];
(async()=>{for(const p of payloads){const r=await renderMyst(p+'\n',{documentPath:ws+'/doc.md',workspaceRoot:ws});
const w=buildPreviewWebviewHtml(r.html,ws,assets,undefined,ws,undefined,undefined,true,true);
const m=w.html.match(/<main[\s\S]*?<\/main>/);console.log('IN :',p,'\nOUT:',m?m[0].replace(/<main[^>]*>/,'').slice(0,500):w.html.slice(-400),'\n');}})().catch(e=>console.error(e));
