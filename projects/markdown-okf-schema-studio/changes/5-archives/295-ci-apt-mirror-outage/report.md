# Report: CI visual job without the Ubuntu mirrors

PR #361 merged as 967eecba on 2026-11-11. The `dev-ci visual` recipe installs the cached apt
archives with `--no-download` and no `apt-get update`, then Chromium without `--with-deps`, and
falls back to the old path on failure. Visual setup: 30 s (6.5 min before, jobs cancelled at 15 min
during the mirror outage). Log: "no mirror contacted".
