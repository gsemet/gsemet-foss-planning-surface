# SC19 evidence: links, floor, grep, file list

- Floor: `cmp skills/chantier/cards-next/floor.md skills/chantier/references/floor.md` prints nothing (byte-identical, 554 bytes).
- Nothing loads `cards-next/`: `grep -rn "cards-next" skills/chantier/references skills/chantier/SKILL.md agents com.github.copilot hooks roles.yaml` returns 0 lines (only `brief --cards` reads it).
- topics.json: 9 topics, each `review_by: "0.16.0"`; validated with the CLI's `load_topics` without error. Readings are relative to `cards-next/`.
- Links: the topic links `../pr-template.md` and `../concepts.md` are forward links to child 23 (SC21), not yet present in `cards-next/`; every other link resolves.
- Forbidden strings (CR numbers, "epoch", BOM, CRLF): none found.
- Files added, all under `skills/chantier/cards-next/`: 11 cards, `floor.md`, `topics.json`, 9 topics. No file outside it changed.
- Owed at the Driver's push: `git show HEAD:<path>` byte checks and `git diff --stat <base>..HEAD` (no commit here).
- `just test` timing: no test added, 0 s added.

## Round 2 additions

- floor.md: `cmp` against references/floor.md, identical.
- Trigger alignment: for each of the 9 topics in topics.json, the trigger text is a substring of every card of the topic's roles (script run in round 2: all true, 16 role checks).
- Card and topic bytes: `cards-bytes.md`, all within budget.
