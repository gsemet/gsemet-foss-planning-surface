## Summary

The Chief of Staff keeps chantier's rules through a compaction, and offers only options the user can take.

- What the steering session may do while its batch runs, as the user said it: backlog work and the spec-writer yes; grill and touching the batch no (cards, init, docs).
- The reload: "chantier reload" by hand (router skill, `session-start.md` section 5), and on Claude Code the mod's `session.compact` hook adds the reload line after every manual or automatic compaction of a session that loaded a chantier role (Chief of Staff, router, Griller). No CLI change.
- Options by environment: a general "Offering options" rule and checklist, and Claude Code's "Surfaces and options" table. Copilot gets "Not done yet" sections.
- Two pre-existing bugs fixed in `hooks/register.tsx` so the mod parses and its tests run: a block comment that closed early, and a duplicate Markdown key on the planning-surface board.

Open questions answered: "no demo" kept while a direct batch runs; the reload covers a Griller.

## Test plan

- [x] `just check`: 37 passed
- [x] `claude plugin test .`: 29 pass, 0 fail (4 new tests)
- [x] `claude plugin validate .`: the two known warnings only
- [ ] `just scenario`: see the PR comment / evidence
- [ ] `tsc -p`: 7 errors, none in the new hook (the 6 on `bases`/`views` come from the planning-surface commit, whose atoms `types/` does not declare); not fixed here
- [ ] Live trial: cannot run before merge (the plugin loads from the main checkout). The reload marks stay unproved. After merge: `/chantier:chief-of-staff`, `/compact`, the next answer opens with the reload line.
