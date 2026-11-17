# `> [!NOTE]` followed by `> # heading` takes the heading as the alert title

Type: gap · Priority: P3 · Filed 2026-11-01 from CR 223 round 2 (point for the owner)

## Today

`> [!NOTE]\n> # h\n> b` renders an admonition titled "h". GitHub shows the default "Note" title and
a real `<h1>` inside the alert. This is the same on `origin/main`, so CR 223 did not cause it.
The MyST path treats a leading quoted heading as the admonition title (code in
`src/core/render/mystGithubAlerts.ts`; exact line to confirm).

## Expected

Owner decision first: keep the title shortcut (a feature for MyST users) or match GitHub.
If matching GitHub, the heading stays a heading in the body and the title is the default.

Proof: render test with the input above, compared with `gh api markdown -f mode=gfm`.
