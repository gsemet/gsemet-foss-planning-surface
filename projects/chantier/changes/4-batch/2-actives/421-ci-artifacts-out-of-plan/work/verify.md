# Verify CR-421

Head: b4d7117bdd051794ff88deed74f471e4908ee25c

All claims judged at b4d7117 unless noted.

1. Ignore line and `_matches` (spec A, B): `git diff origin/main...HEAD -- src/core/files.py src/store/base.py` shows `**/work/**/artifacts-*/` in IGNORED and `_fits` reading a middle `**` as zero or more folders. Before/after probe of `is_published` (`before-after.md`): the 3 artifact paths go True -> False, the file named `artifacts-1` and `evidence/artifacts-1/a.txt` stay True. OK.
2. Tests 1-7 of the spec, run at b4d7117: `pytest test_store_conformance.py test_writer_edges.py test_writer_lines.py test_startup_manifest.py` -> `104 passed, 12 skipped` (the skips are the surface backends' feature skips and POSIX-only cases). Includes the git `check-ignore` agreement test, writer leaves `artifacts-123/` out (synced, commit holds only 01-intent.md), recognition cases, lines test, cards test. OK.
3. Real refusal (check 5, win32): `pytest test_writer_edges.py -v -k "path_too_long or artifact"` -> `test_a_real_path_too_long_blocks_with_its_reason_then_resumes PASSED`, `test_a_downloaded_artifact_folder_is_left_out_of_the_commit PASSED`, `2 passed`. Path 311 characters, folder 235 (git for Windows only warns on a too-long folder; stated in Known gaps). OK.
4. `path-too-long` machinery (spec C): diff shows `too_long_path` (add only, phrase and path both required, else git-error), `FAILED_STEPS` excluded from `sync-resumed@1` in `_preconditions`, text `<n> characters: <path>` cut at 150 + `...` and `rec.cut`, audience `self._holding([path])`, `WAY_OUT["path-too-long"]` with the spec's exact text; no new git command. OK.
5. Cards and docs (spec D, E): diff shows the added sentences in driver.md, debugger.md, verifier.md, concepts.md (two places), planning-folder.md (both sentences), planning-modes.md; agents/ untouched (`git diff --stat` lists none). OK.
6. Startup limit raised 45_000 -> 45_400 (`test_startup_manifest.py`): disclosed in the PR as an autonomous decision; test green. OK.
7. PR description (https://github.com/gsemet/chantier/pull/389, read with `gh pr view 389`): renders (sections, details fold), Summary/Deliverables/Changes match the diff (including the `late.py` move), Known gaps names the folder-too-long limit, no images. Review box: log note "r1 approved at 4ed0d56" matches the box's `4ed0d56` base round; the later commit b4d7117 is a one-comma docs fix, stated. Evidence/Verified/CI boxes pending (Driver's). Role names are product terms of the cards. OK.
8. Gate: no `chantier gate` pass exists at this head; the spec's long gate is CI's `just scenario (ubuntu-latest)`, not claimed here. Not run by me (brief).

VERIFIED
