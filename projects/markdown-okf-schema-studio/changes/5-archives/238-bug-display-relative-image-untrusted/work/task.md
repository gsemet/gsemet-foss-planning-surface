# Task: relative images in Restricted Mode

## Files (start here)

- `src/core/security/resource-policy.ts`: `createPreviewResourcePolicy` (line ~159),
  `isBroadReadOnlyRoot` (line ~141), the `readOnly` branches (lines ~274, ~311).
- `src/session/features/rendering.ts` line ~78: read-only roots.
- Image URL rewriting in `src/core/render` (relative path to webview URI), and
  `localResourceRoots` in `src/host-vscode`.

## Change

1. Reproduce first: a Restricted Mode preview of a document with relative images, one with spaces
   in its name, one in a subfolder, one in a document under the home folder. Name the cause
   (encoding, policy, localResourceRoots, CSP).
2. Fix the cause. If it is the policy, apply the owner's limits from `00-request.md`: images only,
   document folder and workspace root, includes and dot-segments still refused, broad roots refused
   except the document's own folder.

## Tests first

- Unit tests on the policy or the URL rewrite that fail today for the reproduced case(s).
- Security tests stay: includes refused, `.ssh` refused, home-root refused for other folders.
- e2e scenario in group `trust-security` (simulated).

## Requirements

Update `SwRS-MDOKFSTUDIO-TRUST-002` (proposed, owner agreement recorded in `00-request.md`) and any
other touched TRUST/MYST requirement; markers per `rules.md`.

## Gates (foreground)

- `just check` (includes the security checks)
- The e2e group touched, simulated (no real VS Code window).
- `just requirements-update`
