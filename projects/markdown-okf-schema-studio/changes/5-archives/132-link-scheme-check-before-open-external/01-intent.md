# A percent-encoded link scheme must never open a local file

Type: fix · Priority: P1 · Filed 2026-10-27 from the performance and security audit (finding S-01)

## Problem

A Markdown link such as `[x](https%3A/../../System/Applications/Calculator.app)` is classified as
an external link: the scheme allowlist is checked on the decoded path, but the raw string is what
is opened (`src/core/navigation/previewNavigation.ts:134-141`, same pattern in
`src/core/security/resource-policy.ts:238-241`). `src/session/features/links.ts:258-259` passes
it to `src/host-vscode/vscodeHost.ts:226`, `vscode.env.openExternal(vscode.Uri.parse(url))`.
`Uri.parse` finds no scheme and defaults to `file:`, so one click on a link in an untrusted
document can open a local file or application with the OS handler, Restricted Mode included.

## Expected

- Only `http`, `https` and `mailto` links reach `openExternal`; the host re-checks the scheme on
  the parsed URI (`vscode.Uri.parse(value, true)`) immediately before the call.
- The classifier checks the scheme on the raw string and treats a `%` before the first `:` as
  not external (shown as a broken/unsupported link, never opened).
- Proof: a unit test on `classifyPreviewReference` with the percent-encoded case, and an
  integration test asserting `openExternal` is never called with a non-allowlisted scheme.
  Confirm the launch in a real VS Code window before the fix (before-shot or log), if it can be
  shown safely (open a harmless file, never run an application).

Source: [audit report, S-01](../../P3/audit-performance-security-maintainability/report.md).
