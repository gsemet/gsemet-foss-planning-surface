import io

path = r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/507-sc21-cards-foreman/work/verify.md"
text = io.open(path, encoding="utf-8", newline="").read()


def swap(old, new):
    global text
    assert text.count(old) == 1, old
    text = text.replace(old, new)


start = text.index("Base: `24111e6d")
end = text.index("Paths: `<worktree>`")
head_block = """Base: `24111e6d9920a7ff3e8f210613186dd65d802ec8` (origin/main). Judgments so far: `03f973e4f0d0756c9b5fa77ed0f888f941745dbe` (NOT VERIFIED, F1 to F6); `88d9ab4`, first pass (NOT VERIFIED, F7 and F8); `88d9ab4`, second pass (NOT VERIFIED, F7 alone); `88d9ab4`, third pass (VERIFIED, F7's unmet part accepted and stated in Known gaps); `88d9ab4`, this fourth pass, the posted description alone.

Result: **VERIFIED**. The description posted again at 04:48:23Z differs from the third pass's by one new Autonomous decisions bullet and the checked `Verified` box; both hold.

## D. The description as posted now: VERIFIED (judged at 88d9ab4)

`gh pr view 487 --repo gsemet/chantier --json headRefOid,baseRefName,isDraft,state,mergeable,updatedAt,body` (`r17-pr.log`), then `uv run --no-project python -I work/verifier/scripts/r17/body.py`:

```text
headRefOid 88d9ab40d706ce2442821ad77385812af35ba846 base main OPEN draft MERGEABLE updatedAt 2026-11-26T04:48:23Z
local bytes 33295 bom False crlf False
posted chars 33282 crlf in posted False bom False
posted == local True
lines before 370 now 372            (split on newline, against posted-r16.md)
== insert  now 104-105
+ - The inventory rows found to restate a tested rule without naming its case are left as they are, and
+   stated in Known gaps.
== replace 346 now 348
- - [ ] Verified
+ - [x] Verified at `88d9ab4`
name hits 0
```

| Claim, posted line | Proof |
| --- | --- |
| New bullet, 104-105: the rows are left as they are | a read of those rows in the four inventories this pass: the `check` cells of C-045 (`help grill-critic`), C-732 (`help merge-series-stack`), H-412 and H-1566 (`floor.md:5`) and H-1026 (`help host-turn-end`) name no quiz case; C-576 still names `a8-push-refused-default-branch`; `ls -la --time-style=full-iso evidence/`: newest file 05:27:32 local, as at the third pass |
| New bullet: "stated in Known gaps" | posted lines 165-168 name H-412, H-1566, C-732, C-045, H-1026 and C-576, and say no search for every such row was made |
| New bullet: a decision taken without the user | `$CHANTIER log CR-507`, 04:44:45Z: "F7 left (five rows a case tests do not name it), accepted: Known gaps narrowed and reposted" |
| "Verified at `88d9ab4`", 348 | same log: `04:47:55Z driver verdict result=VERIFIED head=88d9ab40d706ce2442821ad77385812af35ba846`, the last verdict at the head, before the post at 04:48:23Z; `git rev-parse HEAD` is that SHA and `git status --porcelain` prints nothing |
| "CI green at `88d9ab4`", 349 | `gh pr checks 487`: the three `just check` jobs, `just eval-dry-run` and `just scenario (ubuntu-latest)` pass (run 45748025918) |
| Renders, no internal reference, no image, no username | `body.py`: sections Summary to Known gaps (1, 12, 89, 95, 142), one fold 228-369, no `![` or `<img`; CR and child references on lines 353 and 359 only, under "Internal references" (351); no username or home path. The new bullet is a list item with an indented continuation, ahead of the next bullet; no `STALE` mark |

Observation, not a failure: the new bullet gives no reason for leaving the rows, which the PR template asks of an Autonomous decisions bullet; the Verifier card's description checks do not include it.

"""
text = text[:start] + head_block + text[end:]

swap(
    "## F8. The PR description as posted: VERIFIED (judged at 88d9ab4)",
    "## F8. The PR description as posted at the third pass: VERIFIED (judged at 88d9ab4, carried by D: the other lines are unchanged)",
)
swap(
    "on a body that differs from today's in lines 159-167 only",
    "on a body that differs from the third pass's in lines 159-167 only",
)
swap(
    "\"CI green at `88d9ab4`\": C27. \"Verified\" unchecked: no claim.",
    "\"CI green at `88d9ab4`\": C27. \"Verified at `88d9ab4`\", now checked: D.",
)
swap(
    "### C27. CI at head, the long gate included: VERIFIED (re-read this pass)",
    "### C27. CI at head, the long gate included: VERIFIED (re-read this fourth pass)",
)
swap(
    "### C28. Review box: VERIFIED (re-read this pass)",
    "### C28. Review box: VERIFIED (re-read this fourth pass; now posted line 347)",
)
swap(
    "### C29. Rendering, images, names: VERIFIED (searched again on today's body)",
    "### C29. Rendering, images, names: VERIFIED (third pass's body; searched again on today's in D)",
)
swap(
    "## Claims carried\n",
    "## Claims carried\n\nFourth pass: every claim outside D is carried from the third pass: the head and the worktree are the same, no evidence file changed, and the two changed body places enter no other proof.\n",
)
swap(
    "This pass: none seen.",
    "Fourth pass: the rules command was run in the same step as the card's first read, not after it; some shell calls used a chain, and one changed folder into the worktree.\n\nThird pass: none seen.",
)

io.open(path, "w", encoding="utf-8", newline="").write(text)
print("ok", text.count("Head: 88d9ab40d706ce2442821ad77385812af35ba846"))
