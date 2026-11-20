p="requirements/tiers/log.md"
raw=open(p,encoding="utf-8",newline="").read()
nl="\r\n" if "\r\n" in raw else "\n"
t=raw.replace("\r\n","\n")
E='''### Garden the requirements of toolbar-navigation and lifecycle-sync (CR 346, round 1)

- Merged (old superseded by new, scenarios, verification notes and `depends_on` folded into the new one):
  TOOLBAR-013 into LIFE-169; TOOLBAR-056 and 058 into 054; 065 into 059; 083 into 079; 113 into 077;
  122 and 126 into 120; 133 into 037; 022 into 018; 002 into 025; 005 into 003; 011 into 010; 132 into 009;
  014 and 131 into 012; LIFE-010 into LIFE-003; LIFE-055 into LIFE-049; LIFE-097 into LIFE-100 and LIFE-108
  (a defaults scenario in each); LIFE-171 into LIFE-001 (the Agents scenarios). Every old ID is replaced in
  the markers, the `depends_on` lists and the Main paths.
- Changed: SwRS-LIFE-004 is retitled and written in observable words; the internal scenarios of LIFE-069 and
  LIFE-156 moved to a verification line; LIFE-149 is no longer exempt; TOOLBAR-007 gets the scenario "The
  collapsed choice is kept for the workspace"; the scenario "Table handle strip at the top of the page" moved
  from TOOLBAR-001 to SwRS-TABLE-007 (a table-editing SwRS, which already specified the handle strip; the
  marker of tableMoves.ts moved with it). The draft StRS TOOLBAR-002 and 003 and the draft SwRS TOOLBAR-003,
  004, 006, 008, 009, 010 and 012 are now `proposed`.
- Reparented (`derives_from`): LIFE-100 and 108 to StRS-LIFE-010; LIFE-026 to LIFE-003 and TRUST-001; 032 to
  LIFE-003 and LIFE-005; 049 to LIFE-003, 005 and 007; 156 to LIFE-021; 069 and 071 to LIFE-005; 119 to
  LIFE-010; 125 to LIFE-010 and LIFE-014; 018 to LIFE-001; 002 to LIFE-007; 172 to BLOCK-001. The StRS-TOOLBAR
  references of SwRS-LIFE-169, LIFE-170 and TRUST-001 are dropped; StRS-TOOLBAR-001 depends on LIFE-169 and 170.
- Added: StRS-MDOKFSTUDIO-LIFE-022 "Closing a preview or a folder leaves nothing behind" (proposed), with two
  Main paths on SwRS-LIFE-143; its test marker is `test/integration/workspaceDisposal.test.ts`.
- StRS: TOOLBAR-001 and LIFE-014 are retitled and rewritten; TOOLBAR-011's clause now covers only links in the
  page (`allowOutsideWorkspaceLinks` is read on the frontmatter-link path only); stray `## User Need` headings
  removed; Main paths reshaped on TOOLBAR-001, 013, 014, LIFE-001, 005, 007, 010 and 021.
- Added: a `### Use case diagram` on each of the 17 in-force StRS of the two scopes (LIFE-001, 003, 005, 007,
  010, 014, 021, 022; TOOLBAR-001, 002, 003, 004, 006, 009, 011, 013, 014).
- Not done in this round (rounds 2 and 3): markers moved to the code that carries them, the CSS split, moved
  and new tests. Sources: the markers touched are in `src/` scrollCore.ts, scrollSync.ts and `test/`
  sourceMapping, runtimeScroll, pageSettings, trustReq, workspaceDisposal, tableMoves.

'''
k="## 2026-11-17\n\n"
assert k in t
t=t.replace(k,k+E,1)
open(p,"w",encoding="utf-8",newline="").write(t.replace("\n",nl))
