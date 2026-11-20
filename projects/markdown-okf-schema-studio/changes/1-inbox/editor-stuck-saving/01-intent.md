Bug, found by the owner on 1.10.0 (2026-11-20). After several cycles of opening a block's editor and
leaving it, mostly on lists, the editor stays open with "Saving Markdown..." under the source, and
the status never clears. The owner asked for aggressive testing to reproduce it.

Done when: the sequence that leaves the editor stuck is known and covered by a test that fails
before the fix; after the fix, every way of leaving the editor (Done, Cancel, Escape, click
outside, click another block, a re-render during the save) ends with the editor closed or showing
an error, never stuck.

Reproduction is running (Chief of Staff, 2026-11-20); its report goes into this folder's `work/`.

Owner, 2026-11-20, later: "attention, ca arrive aussi sur une liste, un texte, sauf que je n'arrive
pas reproduire". It happens on lists and on plain text, and it is intermittent: the owner cannot
reproduce it on demand. Look for a timing race, not a list-only path.
