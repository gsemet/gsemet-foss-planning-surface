fix(security): read-only previews no longer expose the home folder or dot-directories

## Summary

A read-only preview (no workspace folder, or Restricted Mode) used the document's folder as the
root for includes and for the webview's local resources. A document placed directly in the user's
home folder therefore made the whole home tree readable by the preview. There is no network path
out of the webview, so the exposure was local, but it is avoidable.

This change closes two classes of input in read-only previews:

- a document folder that is the user's home folder, one of its ancestors, or a file-system or
  drive root: includes and resources are refused with a visible warning, and the webview gets no
  local resource root other than the extension bundle;
- include and resource paths that contain a dot-directory segment (any segment starting with `.`),
  in any folder, including when reached through a symlink.

Trusted workspaces keep their current behaviour.

## Deliverables

No visible UI change: refusals appear through the existing preview diagnostics warnings, so there
are no screenshots. New tests:

- `test/security/readOnlyRoot.requirements.test.ts`: root detection (home, ancestor, file-system
  root, case folding, platform home variable) and the dot-segment rule through the render pipeline.
- `test/session/readOnlyLocalRoots.test.ts`: the webview local resource roots for a temporary
  "home" folder, a file-system root, a subfolder and a writable workspace.

A new software requirement (trust and security) records the behaviour; the changelog is updated.

## Changes

Read-only root resolution and resource policy in the core layer, session local resource roots, one requirement, changelog.

## Impacts

Read-only previews of documents in the home folder, a file-system root or a dot-directory no longer load includes or local resources.

Blast radius: 2.

## Autonomous decisions

- The home folder is read from `HOME` (`USERPROFILE` on Windows) rather than `os.homedir()`,
  because the core layer may not import `node:os`; paths are compared after realpath, case
  insensitively on Windows and macOS.
- In a broad root, includes and resources are refused outright, not allowed one by one (images
  next to the document are not shown there).
- Navigation links are unchanged.
- The dot-segment rule applies to read-only previews only.

## Test plan

`just check`: unit 2802/2802, security 57/57, contracts 2/2, pytest 31, requirements validate with
0 errors. No real-window suite was run (no host or webview UI change). Locally,
`okfreq update-coverage --check` differs only by file-list ordering of the local okfreq build; to be
confirmed on CI.

## Internal references

CR 133; backlog item security-read-only-root-home; audit finding S-02.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
