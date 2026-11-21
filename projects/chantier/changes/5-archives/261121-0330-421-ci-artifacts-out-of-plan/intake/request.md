# CI artifacts in work folders: keep them out of the published plan

Priority P2. Seen at the switch to the surface's writer (2026-11-20, after CR-404), reported by the Studio project's Chief of Staff.

The writer's first cycle was blocked by `git add` ("Filename too long") on Windows: raw CI artifacts that Drivers and debuggers download under `work/**/artifacts-<run id>/` reach 358 characters of path (about 360 files in Studio's CR-350 and CR-425, 20 MB in one CR). They also have no place in the published plan.

Keep downloaded CI artifacts out of what the writer publishes: the cards tell the Driver, the debugger and the verifier to download them under `work/scratch/` (already ignored), and the managed `changes/.gitignore` also ignores `**/work/**/artifacts-*/` for agents that miss it. The writer's blocked message for a too-long path names the file and this rule. Workarounds in use until then: Studio's pattern in the surface's `.git/info/exclude`, and one folder moved by hand to `work/scratch/`.
