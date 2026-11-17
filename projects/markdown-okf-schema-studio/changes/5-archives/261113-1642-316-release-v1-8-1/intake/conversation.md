# Conversation excerpts (owner and Chief of Staff, 2026-11-13, translated from French)

- Owner: "Let's move to publishing on the VS Code Marketplace, which apparently changed, with a
  trusted publisher too."
- Chief of Staff: the Marketplace offers Trusted Publishing from GitHub Actions; our vsce 4.0.0 has
  no `--oidc`, so the release job must change; keep the token until an OIDC release succeeds.
- Owner, on how to prove it before the next feature release: "We can do a fake 1.8.1 if you want."
- Owner, on the blocked local gate: "Heavy run in CI."
- Owner, before the release: "So there will be a release: check carefully that the version is
  consistent."
- Chief of Staff: every versioned file says 1.8.0, the only tag is v1.8.0, the Marketplace serves
  1.8.0; 1.8.1 is set explicitly.
- Owner: "Yes, confirm."
