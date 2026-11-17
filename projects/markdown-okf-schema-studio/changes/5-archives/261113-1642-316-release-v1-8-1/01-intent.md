# Release v1.8.1

Type: release. Filed 2026-11-13 by the Chief of Staff.

## Owner's words

> on peut faire un 1.8.1 fake si tu veux

then, on the batch plan: « Oui, lance ».

## Why

A maintenance release whose only change is how the extension is published: the release job
publishes to the VS Code Marketplace with Trusted Publishing (GitHub OIDC) instead of `VSCE_PAT`
(CR `marketplace-trusted-publishing`, same batch). It is the only real proof of the OIDC publish.

## Scope

- The project's own procedure: `.agents/guidelines/release-process.guidelines.md` (on
  `origin/main`) and "How to Release" in `CONTRIBUTING.md`.
- Version 1.8.1 (patch: no user-facing change).
- Check of record: the Marketplace serves 1.8.1 and the release job's publish step ran with
  `--oidc`; the Marketplace policy "Release workflow" shows a "Last used" date.
