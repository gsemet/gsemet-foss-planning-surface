# Before and after (CR-304)

Before: cb7690a8c0946d1fd296acd1f6032a8518a4f6c8 (main). After: 7c96789fd0d6791228925f40510c293eae25bc18.
The pictures are in the CR folder's `evidence/` as `before-<size>-<check>.png` and `after-<size>-<check>.png`
(sizes 2560, 2940, 1400, 375; checks c1 panel/view, c2 hover, c3 triage, c4 drag (2940), c5 frontmatter,
c6 wide table). Reproduce: `uv run --script work/verifier/verify_board.py` then `verify_drag.py`.
Not captured: Home's "see the batch" on a phone (Home has no openable row at 375).


Round 2 (after at f11132b, before at faa4719): all before-* and after-* pairs in evidence/ were recaptured by verify_board.py and verify_drag.py at these SHAs (rerun both scripts to reproduce).
