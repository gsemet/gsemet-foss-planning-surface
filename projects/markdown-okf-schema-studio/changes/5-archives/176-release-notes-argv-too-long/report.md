# 176 — Release notes prompt exceeds the argv limit (HOTFIX) — report

Landed 2026-10-28. PR https://github.com/gsemet/markdown-okf-schema-studio/pull/190 merged as
1a2fe6ef. v1.0.0 then RELEASED by the Chief of Staff: release run 40782519223 (workflow_dispatch from
main, tag=v1.0.0, notes=placeholder) published GaetanSemet.markdown-okf-schema-studio v1.0.0 to the
Marketplace and attached the VSIX; the body was replaced with hand-written notes.

- release_notes.py: Git context written to a file; short argv prompt; size-bound unit test.
- release.yml: on dispatch, the notes tooling comes from the workflow ref; package/verify/publish
  keep the tag checkout; new input notes=generated|placeholder.
(Driver hand-back pending at landing time; details in the PR.)
