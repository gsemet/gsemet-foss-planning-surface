# VS Code Sphinx/MyST Live View: Implementation Status

## Overall Status

**Tasks 01-07 implementation accepted; release remains blocked by missing manual evidence.**
Tasks 01-03 are mandatory feasibility gates. A `NO-GO` on any gate blocks dependent
implementation work.

## Task Status

| Task | Status | Depends on | Gate/Outcome |
| ---- | ------ | ---------- | ------------ |
| [01 Active-file HTML and Security Gate](05-tasks-01-authentic-html-security-gate.md) | Complete | None | `GO`; [feasibility evidence](../../../../docs/feasibility-authentic-html.md) |
| [02 Active Dirty Snapshot Gate](05-tasks-02-dirty-snapshot-build-gate.md) | Complete | Task 01 | `GO` after inspector verification; [feasibility evidence](../../../../docs/feasibility-dirty-snapshots.md) |
| [03 Active-file Mapping and Scroll Gate](05-tasks-03-source-mapping-scroll-gate.md) | Complete | Task 01 | `GO` after independent inspector repair; [feasibility evidence](../../../../docs/feasibility-source-mapping.md) |
| [04 MyST Rendering Fixture](05-tasks-04-sphinx-feature-contract.md) | Complete | Tasks 02, 03 | `GO`; [feature evidence](../../../../docs/active-file-rendering.md) |
| [05 Active Preview Integration](05-tasks-05-preview-lifecycle-integration.md) | Complete; inspector-verified | Tasks 02, 03, 04 | `GO after REWORK`; [lifecycle evidence](../../../../docs/preview-lifecycle.md) |
| [06 Interaction and Accessibility](05-tasks-06-interaction-parity.md) | Complete; inspector-verified | Task 05 | `GO` for the development gate; native find, clipboard, stock coexistence, trust, and semantic accessibility proxy pass; VoiceOver/assistive-technology speech output remains unexecuted release evidence; [interaction and accessibility evidence](../../../../docs/interaction-parity-evidence.md) |
| [07 Release Evidence and Repository Gates](05-tasks-07-release-evidence.md) | Complete; inspector-verified; release blocked | Task 06 | `NO RELEASE`; [release evidence](../../../../docs/release-evidence.md) |

## Standing Decisions

- Render MyST syntax from the active unsaved Markdown file through Sphinx HTML.
- One side preview follows the active Markdown editor; fixed-file views are deferred.
- Stable two-way block/line mapping is required; pixel precision is not.
- Stock Markdown preview and rendered diff remain unchanged; full parity is out of scope.
- Optional rendered-block editing is deferred to a separate later specification.
- Preview builds must not call source-writing `book-prepare` or change publication output.

## Update Rule

When a task completes, update only its row and add the evidence path or blocker. Do not unblock a
dependent task until every dependency has passed its required gate.
