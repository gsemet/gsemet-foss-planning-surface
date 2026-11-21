# Verify CR-421

Head: af840b1b151b9d503fdc196e00d8599eaa44e0b6

Move since the last judgment (b4d7117): restack onto CR-420's branch; one conflict in tests/test_startup_manifest.py, resolved by keeping CR-420's limits and dropping CR-421's 45_400 constant. Previous judgment kept in work/verifier/verify-b4d7117.log.

1. Move's touch, judged at af840b1: `git diff <CR-420 branch>..HEAD -- tests/test_startup_manifest.py` shows only the added test `test_the_cards_send_a_downloaded_ci_artifact_to_the_scratch_folder` (driver, debugger, verifier cards); no limit constant is changed against the base, so CR-420's limits stand. OK.
2. Writer artifact exclusion, path-too-long reason, store agreement, lines, card byte budgets and card sentence, judged at af840b1: `pytest tests/test_store_conformance.py tests/test_writer_edges.py tests/test_writer_lines.py tests/test_startup_manifest.py -q` -> `108 passed, 12 skipped in 57.97s` (was 104 passed at b4d7117; the +4 are the base's manifest tests and the 3 card cases, minus none failing). Includes the path-too-long blocked-reason test (real, win32) and the artifact-folder-left-out test. OK.
3. Spec claims A-E (ignore line, `_matches`, path-too-long machinery, cards, docs): the CR's own diff against its base lists the same 16 files as before (`git diff --stat <base>..HEAD`); carried from b4d7117: the move touched only the manifest test file, so the sources and docs proofs hold.
4. PR description, Review box, gate: carried from b4d7117 (description unchanged by the move); no `chantier gate` pass at this head and none run by me (brief: long gate not run; CI's scenario job is the spec's long gate).

VERIFIED
