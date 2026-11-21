Head: d20b0bf409d91de02ad54dd0c8371ca662c92cbb

Description-only pass of PR 450, judged at d20b0bf, command `gh pr view 450 --repo gsemet/markdown-okf-schema-studio --json body,title,headRefOid` (headRefOid = the head above). NOT VERIFIED.

Failed:
1. Fold missing (audit 2): the body has no `<details><summary>Details</summary>` block; Changes, Impacts, Test plan and Internal references are all visible.
2. Internal reference outside Internal references (audit 3): Test plan Review line says "round 4"; Deliverables says "measured by the verifier" (a role as the doer of the work).
3. Screenshots are links into a commit (`raw.githubusercontent.com/.../bf652330.../*.png`), not uploads by the forge's CLI, and they are not shown side by side as images (template, Deliverables); a restack can drop that commit.
4. Human decisions section is absent; not checked against 02-answers.md here (absence is allowed only when no decision shapes the change).
