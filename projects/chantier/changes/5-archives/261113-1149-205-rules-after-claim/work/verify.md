# CR-205 verify (delta after restack)

Head: 1fbe16f

- Move: restack, 1989d60 (on origin/main d178c7e) to 1fbe16f (on a246894). `git range-diff` shows `1989d60 = 1fbe16f`: the patch is identical.
- Re-judged: diff vs the new base is still only skills/chantier/references/chief-of-staff.md (+5/-1); the sentence sits at line 554, in place. `just check` at 1fbe16f: 58 passed, release-notes ok, exit 0.
- Carried from 1989d60: sentence matches the spec, foreman.md/agents/CLI/audit unchanged, no BOM, no role names in the body (same patch, byte-identical).
- Not run: `just scenario` (the stack's top gets it once); the earlier pass at 1989d60 is not re-claimed for 1fbe16f.

Verdict: VERIFIED

---
Previous verify (head 1989d60):
# CR-205 verify (head 1989d60)

- Diff vs origin/main: only skills/chantier/references/chief-of-staff.md (+5/-1), inside the "Your epoch." bullet, right after the claim sentence. Test and worker-card commits are already on the base.
- Sentence matches the spec: command after each claim, every batch, resumed/taken-over too; reading before this batch's open does not count; skip only re-read since open and last compaction; command runs every time. `--epoch` list untouched, `rules` not added to it.
- foreman.md, agents, CLI, audit unchanged, as the spec says.
- `just check`: 50 passed, release-notes ok, exit 0.
- No UTF-8 BOM in any tracked file (scan of git ls-files).
- Minor: the line ending "...Carry `--epoch <n>` on exactly these commands..." is long (not wrapped), no check fails on it.
- Not checked by me: `just scenario` (reported passed by the Driver); the J14 pass is the user's next real-direct eval.

Verdict: VERIFIED

- Description pass on the posted body at 1989d60: quoted sentence matches the diff, claims match the spec, boxes true (CI green on check x3, scenario, eval-dry-run), UTF-8 no BOM, no coder/inspector/verifier/investigator/debugger names; it names Chief of Staff and Foreman only as the card's own subjects. Verdict: VERIFIED

