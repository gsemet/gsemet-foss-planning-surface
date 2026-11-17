# Flaky real-window integration steps

During the v1.9.0 release two heavy runs needed a re-run: the toc step in the heavy run on `main`,
and a real-input step in the branch heavy run 43536948441 (rerun once). These intermittent steps
make a version push or a release gate depend on luck.

Source: retro of CR-323, `.agents/changes/4-archives/261114-0709-323-release-v1-9-0/retro.md`.
