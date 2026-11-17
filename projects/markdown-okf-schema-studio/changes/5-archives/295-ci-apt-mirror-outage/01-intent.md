# CI: visual job must not depend on the Ubuntu mirrors

During an Ubuntu mirror outage (2026-11-11), every visual job timed out: `apt-get update` ran twice
(dev-ci, then Playwright `--with-deps`) at ~2.5 min each, although all 47 archives were cached.
Owner: "Oui fait la ce". Fix: install from the cached archives with `--no-download`, no update,
Chromium without `--with-deps`; fall back to the old path on failure (ci.guidelines rule 4).
