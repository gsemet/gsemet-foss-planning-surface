# A read-only preview must not expose the home folder or dot-directories

Type: fix · Priority: P1 · Filed 2026-10-27 from the performance and security audit (finding S-02)

## Problem

For a read-only preview (no workspace folder, or Restricted Mode) the resource and include root
is the document's folder (`src/session/previewManager.ts:252-254`), used as `localResourceRoots`
(`src/session/rendering.ts:410`) and as the include policy root
(`src/core/render/renderPipeline.ts:182-185`). Opening `~/notes.md` makes the whole home folder
readable: `{include} .ssh/id_rsa` renders the private key, and the webview can load any file under
it. There is no network exfiltration (`connect-src 'none'`), so the exposure is local.

## Expected

- Read-only preview whose document folder is the user's home folder, a file-system root or a
  drive root: includes are refused with a visible message in the preview, and the webview's
  local resource roots are narrowed (images next to the document are still shown when they can
  be allowed individually; otherwise a clear placeholder).
- Read-only previews in any folder: include and resource paths with a dot-directory segment
  (`.ssh`, `.aws`, `.gnupg`, `.config`, any segment starting with `.`) are refused.
- Trusted workspaces keep their current behaviour (repositories include from `.agents/` etc.).
- Proof: unit tests of the policy roots and the dot-segment rule; an integration test with a
  document in a temporary "home" folder.

Source: [audit report, S-02](../../P3/audit-performance-security-maintainability/report.md).
