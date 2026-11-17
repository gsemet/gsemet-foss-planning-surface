# Behaviour note — schema-less number field cannot be committed

Today: in a note without a schema, `rating: 4.5` opens the multi-line YAML box ("4.5\n"). Enter adds a
line (by design, FMEDIT-015 kept); Cmd/Ctrl+Enter shows "Enter a valid number." and writes nothing.

Cause: in `saveValue`, the YAML-box branch makes `fieldValue` the raw text (a string), then the number
check `Number.isFinite(fieldValue)` runs on that string and always fails — even "3.5" with no newline.
The trailing newline is not the real cause; the number check never accepts any text from the YAML box.

After: Cmd/Ctrl+Enter in that box commits: the text trimmed is checked as a number, the YAML text is
posted as today (`fieldValueFormat: "yaml"`), the host parses it and writes `rating: 3.5`; the editor
closes. Enter still adds a line. Schema number fields (one-line number input) are unchanged.

Requirements touched (all proposed SwRS, no approved requirement): SwRS-MDOKFSTUDIO-FMEDIT-003 (add a
row to the "invalid number" table for the schema-less YAML box), SwRS-MDOKFSTUDIO-FMEDIT-004 (YAML box
scenario, unchanged keys). FMEDIT-015 and FMEDIT-007 are superseded already (by 004 and 003).

Open choices and proposals:
1. Non-number text in a schema-less number box (e.g. `high`, `null`, `[1, 2]`): (A, proposed) keep
   refusing with "Enter a valid number." (narrow fix, as the intent's direction); (B) skip the number
   check in the YAML box, so the host writes any valid YAML (`rating: high`) since no schema constrains it.
2. Replay c6-3 presses Enter and expects a commit, which contradicts the owner's decision: proposed,
   change its step to Enter then Meta+Enter (one-line edit in the QA skill scenario).
3. Discoverability: the YAML box has no key hint (the text box has "Enter saves · Shift+Enter adds a
   line"). Proposed: no hint in this fix; backlog item for a "Cmd/Ctrl+Enter saves" title on YAML boxes.
