# Publish the extension on Open VSX

Type: ci · Priority: P1 (owner, 2026-11-03). Filed earlier by the owner but misplaced inside the CR 249
archive; moved here on 2026-11-03.

## Owner's words

> Publish this extension to <https://open-vsx.org/search?q=Markdown>
>
> Then check what would be necessary to be compatible with Cursor

## Scope

- The release job (`.github/workflows/release.yml`, called by CI after tagging) also publishes the
  same VSIX to Open VSX with `ovsx publish`, after the Marketplace step; a version already on Open VSX
  is skipped, like the Marketplace, so a re-run is safe.
- Setup the owner does: an Open VSX account, the `GaetanSemet` namespace (`ovsx create-namespace`)
  and its ownership claim, an `OVSX_PAT` secret in the `release` environment.
- CONTRIBUTING "How to Release" and "GitHub Configuration" name the new secret and step.
- Cursor (and VSCodium, Windsurf) install from Open VSX: check what else Cursor needs (engine version
  range, proposed APIs, webview behaviour) and report the gaps; do not fix them in this CR.
- Optionally publish 1.3.0 by hand once the step exists (`ovsx publish` on the released VSIX).
