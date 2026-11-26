# CR-511 before and after (text only)

- Before (base): `266b784f008d6d9c6a5e7e1f9eabacefb0552dee`
- After (pushed head): `5d2626debacb20ffa6a5599ff21ba3397d781ff0`
- No screenshot: no visual change. No detached worktree: every "before" is read with git from the
  base commit.

`WT` is `C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-511`.

## 1. The inventory and its test

Before: absent.

    git -C WT cat-file -e 266b784:docs/proofs/cards-inventory.md
    fatal: path 'docs/proofs/cards-inventory.md' exists on disk, but not in '266b784'   (exit 128)
    git -C WT cat-file -e 266b784:skills/chantier/scripts/cli/tests/test_cards_inventory.py
    fatal: path 'skills/chantier/scripts/cli/tests/test_cards_inventory.py' exists on disk, but not in '266b784'   (exit 128)

After: 1,474,636 bytes (blob 43719c9b), 4629 rows, 329 open; the test passes (verify.md, claim 2).

## 2. The context hand-back at 130,000 tokens

    git -C WT grep -n -E "130,000" 266b784 5d2626d -- <cr, stack, release driver cards>

Before: only `stack-driver.md:11`. After: `cr-driver.md:15`, `release-driver.md:13`,
`stack-driver.md:13`.

## 3. Card text about output the CLI no longer prints

    git -C WT grep -n -i -E "opening lines|skeleton|writes:. line|writes line" 266b784 5d2626d -- skills/chantier/references

Before: `concepts.md:78,82,88,99,103,105`, `topics/cr-review-step.md:3`, `topics/cr-workers.md:5`,
`topics/direct-mode-p2.md:4`, `topics/direct-mode-switch-p4.md:3`, `topics/qa-order.md:3`,
`topics/trouble-worker.md:3` describe printed opening lines, a prompt skeleton or a worker writes
line. After: none of these; the remaining matches are unrelated (`status-layout.md` table
skeleton, the host write guard's `writes:` line).

## 4. Restored rows

    uv run --no-sync --project C:/Users/gaeta/Projets/chantier python -I -B -X utf8 <work>/verifier/vf_claims.py WT restored <the 37 ids>

For each of the 37 ids the home's quoted span is in the card at the head (`head: True`) and not at
the base (`base: False`).

## 5. Card sizes, LF bytes (`git -C WT ls-tree -r -l <sha> -- <cards>`)

| card | before | after |
|---|---|---|
| cr-driver.md | 3749 | 5066 |
| stack-driver.md | 3783 | 4821 |
| release-driver.md | 3809 | 4685 |
| foreman.md | 3997 | 4426 |
| conflict-resolver.md | 1494 | 1535 |
| qa-driver.md | 1567 | 1755 |
| griller.md | 1925 | 1925 |
| griller-skill.md | 3621 | 3621 |

## 6. Brief byte ceilings (`git -C WT diff 266b784 5d2626d -- .../tests/test_brief_bytes.py`)

cr-driver 9900 to 11100, release-driver 9600 to 10500, stack-driver 9200 to 10300, qa-driver 6100
to 6300, foreman 22200 to 22600.
