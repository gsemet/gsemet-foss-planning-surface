# Open VSX publish fails on the version push

On the v1.9.0 version push the Open VSX step failed: "No trusted publisher matches the presented
token". The release job runs as a reusable workflow called from `ci.yml` (`workflow_call`), so the
OIDC token names `ci.yml`. The only trusted publisher open-vsx.org allows per extension is
registered for `release.yml` with environment `release`. The Release driver recovered with one
`workflow_dispatch` of `release.yml` with the tag, which published.

Every future version push fails the same way until the publish path matches the registration.

Source: retro of CR-323, `.agents/changes/4-archives/261114-0709-323-release-v1-9-0/retro.md`.
