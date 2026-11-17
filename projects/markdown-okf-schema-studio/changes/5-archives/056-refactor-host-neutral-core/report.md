# Report — 056-refactor-host-neutral-core

Status: **done** (2026-10-24, branch `changes-requests/056-refactor-host-neutral-core`,
[PR #51](https://github.com/gsemet/markdown-okf-schema-studio/pull/51), rebase-merged; main at 8513346).

## Delivered (8 commits)

| Step | Commit on main |
| --- | --- |
| Safety net: host/page timing, page message validation, runtime trace | c29198f |
| One typed protocol, typed routers, host-neutral revision | 7bcc15c |
| Host ports (`src/host-api/`), VS Code adapter, in-memory host, pure core edits | c51d416 |
| `PreviewManager`, `PreviewSession`, 13 feature controllers; `extension.ts` 5 830 → 48 lines | 78b8424 |
| Page runtime as a typed esbuild bundle with `HostTransport`; neutral `--studio-*` tokens | 454ac51 |
| Layers enforced by dependency-cruiser; size ratchet 800/1 500 lines | a3f7afd |
| Registries: settings table (generates `package.json` schema), palette actions, MyST directives | aa559cd |
| Page runtime, renderer, front matter and styles split | 8513346 |

## Proof of completion

- Each step: coder + reviewer, APPROVE (S8 took 2 rounds, others 1).
- [checks run 40064684479](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40064684479),
  heavy [run 40065250657](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40065250657)
  (integration + stress pass). Real VS Code proofs ran in CI only (screen locked overnight).
- No visual change (320 scenarios, baselines unchanged; preview.css byte-identical).
- PR body has a "How it works" section (layer diagram, edit sequence, code sketch, size table).

## Open items

- Spec deviations (in the PR): styles stay TS modules, ProcessRunner port not wired to
  PlantUML/Sphinx, core keeps documented Node built-in exceptions, some directives still in the
  renderer, `realInput.test.ts` above the ratchet.
- Proposed backlog: async ports for fs / child_process / crypto to remove the core exceptions.
- Main checkout needs `npm ci` (dependency-cruiser).
