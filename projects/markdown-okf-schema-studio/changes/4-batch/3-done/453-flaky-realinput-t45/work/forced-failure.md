# Forced failure of RI-T45 (local, not committed)

Head 8071d21712ab1389f6b8cc244a344497c2b4265e. One expectState expectation temporarily changed ("| :---: | --- |" to "| :---: | FORCED |"), then reverted (git status clean). Command: STUDIO_REAL_INPUT_SCENARIO=stress STUDIO_STRESS_REPEAT=1 STUDIO_STRESS_SCENARIOS=table-insert-slash npm run test:integration -- --trusted-only (real VS Code 1.147.0 window, Windows). Home paths rewritten to ~ below. Raw log: verifier/forced-run.log.

```text
Real-input integration failed: Error: stress round 1/1, scenario table-insert-slash: Error: Timed out waiting for only the delimiter cell of the first column centred. Editor state: {"value":"Second paragraph.\n\n| Column 1 | Column 2 |\n| :---: | --- |\n|  |  |\n|  |  |","start":30,"end":30} Scenario: {"steps":[{"at":0,"step":"open preview"},{"at":768,"step":"paragraph click"},{"at":969,"step":"paragraph editor open"},{"at":1012,"step":"press End"},{"at":1185,"step":"type /tab"},{"at":1201,"step":"slash menu open"},{"at":1249,"step":"size grid"},{"at":1337,"step":"table inserted"},{"at":1386,"step":"caret after Column 1"},{"at":1624,"step":"type /align"},{"at":1736,"step":"align choices"},{"at":1759,"step":"query removed"},{"at":1981,"step":"Center pressed"}],"pageTraceStart":333,"host":{"requestId":2,"documentVersion":1,"phase":"ready"},"source":{"version":2,"dirty":true,"text":"# Smoke document\n\nFirst paragraph line one\ncontinues on line two.\n\nSecond paragraph.\n\n| Column 1 | Column 2 |\n| :---: | --- |\n|  |  |\n|  |  |\n\n| Name | Value |\n|------|-------|\n| alpha | one |\n| beta | two |\n\n- item one\n- item two\n"}} landing workbench [none] host [none] {"vscode":"1.147.0 (~\\Projets\\markdown-okf-schema-studio.worktrees\\batch-07-CR-453\\.vscode-test\\vscode-win32-x64-archive-1.147.0\\8a14f0cc1b\\resources\\app)","windowState":{"focused":true,"active":true},"activeTextEditor":null,"activeTab":"Studio · smoke.md","page":{"hasFocus":true,"visibility":"visible","activeElement":"iframe.webview.ready","activeEditorUri":null,"textFocusedEditors":[],"messages":[]},"frames":[{"url":"vscode-file://vscode-app/~/Projets/markdown-okf-schema-studio.worktrees/batch-07-CR-453/.vscode-test/vscode-win32-x64-archive-1.147.0/8a14f0cc1b/resources/app/out/vs/code/electron-browser/workbench/workbench.html","state":{"content":false,"documentId":null,"version":null,"requestId":null,"visibility":"visible"}},{"url":"vscode-webview://1agte1t6jj4ke9ljg38ms8ghm3od22k6tu5ar1aan8d0j8blguua/index.html?id=9bb83626-513a-411c-9e9a-b42e805ab022&parentId=1&origin=3c16dd64-067c-4b55-a531-452752ae5f88&swVersion=6&extensionId=GaetanSemet.markdown-okf-schema-studio&platform=electron&vscode-resource-base-authority=vscode-resource.vscode-cdn.net&parentOrigin=vscode-file%3A%2F%2Fvscode-app&mountId=18a062d4-c5bc-4874-ac45-6044f623b27a","state":{"content":false,"documentId":null,"version":null,"requestId":null,"visibility":"visible"}},{"url":"vscode-webview://1agte1t6jj4ke9ljg38ms8ghm3od22k6tu5ar1aan8d0j8blguua/fake.html?id=9bb83626-513a-411c-9e9a-b42e805ab022","state":{"content":true,"documentId":"file:///~/Projets/markdown-okf-schema-studio.worktrees/batch-07-CR-453/test/integration/fixtures/realinput-t45-wz1cT3/smoke.md","version":"1","requestId":"2","visibility":"visible","editorTrace":[{"at":0,"event":"page","detail":"request 2 version 1"},{"at":343,"event":"mousedown","detail":"svg prevented=false active=body pageFocus=false"},{"at":343,"event":"page focus","detail":"active=body pageFocus=true"},{"at":528,"event":"mousedown","detail":"p prevented=false active=button pageFocus=true"},{"at":532,"event":"block editor opened","detail":"line=6 active=p pageFocus=true"},{"at":581,"event":"block editor focused","detail":"line=6 active=textarea pageFocus=true"},{"at":1642,"event":"mousedown","detail":"option=center prevented=true active=textarea pageFocus=true"}]}}]}
Workbench focus (main window, read over CDP):
  focused part: webview
  active element: iframe.webview.ready
  ancestors (nearest first): div#9bb83626-513a-411c-9e9a-b42e805ab022.webview-overlay-content.webview-overlay-outer-right.webview-overlay-outer-bottom[context=22] < div < div.modern-ui.modern-ui-tabs.modern-ui-connected-editor-tabs.modern-ui-notifications-dialogs.monaco-workbench.windows[role=application] < body
  document: hasFocus=true visibility=visible
  focus context keys: not reachable from the page (internal service); see the focused part
  visible parts: title bar, activity bar, editor, status bar; hidden: banner, sidebar, panel, auxiliary bar
  active editor tab: smoke.md, preview
  chat widgets: 0 visible of 0
  quick input: hidden
  notification toasts: none
  notification center: hidden
  dialogs: none
  context menu or hover: none
  recent focus moves (oldest first):
    -12139 ms window-focus active body
    -12138 ms focusin div.native-edit-context[aria-label="The editor is not accessible at this time. To enable screen "] in editor
    -12098 ms focusout div.native-edit-context[aria-label="The editor is not accessible at this time. To enable screen "] in editor -> null
    -12072 ms focusin div.native-edit-context[aria-label="The editor is not accessible at this time. To enable screen "] in editor
    -12013 ms focusout div.native-edit-context[aria-label="The editor is not accessible at this time. To enable screen "] in editor -> null
```
