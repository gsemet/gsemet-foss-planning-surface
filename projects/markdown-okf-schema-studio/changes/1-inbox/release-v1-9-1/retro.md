# Retro: release v1.9.1

| What cost time | Root cause | Process fix (proposed CR) |
| --- | --- | --- |
| The release held about an hour for a fix CR (CR-327) after the version work had started | CR-326 grew the stress list to 17 scenarios; the default 20 rounds took 24 min 41 s against a fixed 26-minute launch deadline, and no default-repeat stress run had completed on the merged head | A CR that changes the stress scenario list proves a default-repeat stress run and reports its duration against the deadline before merge |
| Stress red once on `main` 0941cc09 (round 10/20, real-input palette: Heading 2 prefix timeout) | Intermittent real-window step, already seen in v1.9.0's branch run | Track it with the real-input flake log; harden the palette heading step (proposed CR) |
| Version push integration red once at `myst-blocks`, tag refused until the re-run | The known lost Edit-toggle clicks with an unfocused webview host frame (inbox bug toc-edit-toggle-clicks-lost-after-readme-html), now one step after `toc` | Fix that bug (it gates every version push); widen `toc-loop` to the step after `toc` |
| Open VSX answered 404 for about 3 minutes after a green publish | Registry indexing delay | None: the 10 to 15 minute watch covers it |
