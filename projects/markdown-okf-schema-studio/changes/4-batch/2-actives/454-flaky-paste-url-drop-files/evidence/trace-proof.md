# Trace proof (Evidence 5)

Throwaway commit d571951e (branch throwaway/cr-454-trace-proof, on 845997bb, deleted after). Forced throw after the first phase of each scenario, stress_repeat=1.

- paste-url: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/44905091608 (stress job)
- drop-files: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/44905104654 (stress job)

```
paste-url failed: Error: forced failure for the trace proof
paste-url failure trace: {"preview":{"phase":"ready","requestId":1,"documentVersion":1,"webviewReady":true,"deferredWorkPending":false,"blockEditOpen":false,"pageEditorOpen":true,"contentPatches":0,"htmlAssignments":4,"panelActive":true},"source":{"version":1,"text":"Read the guide for details.\nLogo:  then text.\nHome:  then text.\n\nSecond paragraph.\n"},"frame":{"found":true,"editMode":"on"},"tabs":[[{"label":"preview.md","inputType":"Hc"},{"label":"paste.md","inputType":"Hc"}],[{"label":"Studio · paste.md","inputType":"Lf"}]],"failures":[],"lastProgress":"paste-url: first paste (link)"}
drop-files failed: Error: forced failure for the trace proof
drop-files failure trace: {"preview":{"phase":"ready","requestId":1,"documentVersion":1,"webviewReady":true,"deferredWorkPending":false,"blockEditOpen":false,"pageEditorOpen":false,"contentPatches":0,"htmlAssignments":4,"panelActive":true},"source":{"version":1,"text":"First paragraph of the page.\n\nSecond paragraph of the page.\n"},"frame":{"found":true,"editMode":"on"},"tabs":[[{"label":"preview.md","inputType":"Hc"},{"label":"page.md","inputType":"Hc"}],[{"label":"Studio · page.md","inputType":"Lf"}]],"failures":[],"lastProgress":"drop-files: first drop (Markdown file)"}
```
