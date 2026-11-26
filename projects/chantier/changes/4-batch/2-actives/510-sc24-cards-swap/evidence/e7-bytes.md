# Evidence 7: bytes, old start reading against the new brief

No model run. Worktree `batch-31-CR-510`, uncommitted tree (base `88d9ab40`), 2026-11-26, all
figures LF bytes.

## How each column was measured

- **Old start reading.** Child 6's old-card boot at the base, `evals/kit/quiz.py`
  `build_old_boot` on `git archive 88d9ab40 skills agents com.github.copilot`, unpacked in the CR
  folder's `work/scratch`:
  `uv run --no-sync --project $W python $S/e7_bytes.py $W $S 88d9ab40`, exit 0. The figure is the
  boot as the quiz counts it, its `=== <path>` headers included (260 to 660 bytes). `--plan`
  prints only the estimate, so the boot is measured from the same function.
- **New brief.** `brief <role> <unit>` at head on the fixture of `tests/test_brief.py`, Claude
  host, each of the run's two paths counted as one byte (so the figure holds on any machine):
  `uv run --locked --group dev pytest -q -s skills/chantier/scripts/cli/tests/test_brief_bytes.py`,
  18 passed, its `brief-bytes` lines.
- **Study.** `study-fable-v2`, section 2.2, "Start, new Claude" (declared), and section 1's
  measured real reading where it has one.
- **Card against target.** The card's LF bytes at head against the target its card child set
  (child 19: 1 KB = 1,000 bytes; child 20: 1 KB = 1,024; child 21: the sizes below).

## Table

| Role | Old start reading | New brief | Study: declared start (measured) | Card at head | Card target | Card against target |
| --- | --- | --- | --- | --- | --- | --- |
| cr-driver | 27,834 | 9,773 | 27,180 (44 KB) | 3,749 | 4,096 | within |
| release-driver | 26,404 | 9,531 | 25,806 (28 KB) | 3,809 | 3,072 | over by 737 |
| stack-driver | 34,714 | 9,179 | 34,054 (56 KB) | 3,783 | 4,096 | within |
| qa-driver | 24,776 | 6,032 | 24,122 (no run) | 1,567 | 2,048 | within |
| coder | 14,226 | 3,939 | 13,966 | 1,603 | 1,500 | over by 103 |
| conflict-resolver | 13,655 | 3,830 | "other workers" 11.2 to 12.5 KB, +826 | 1,494 | 1,500 | within |
| debugger | 13,338 | 3,617 | same group figure | 1,281 | 1,500 | within |
| inspector | 15,690 | 4,336 | 15,422 | 2,000 | 2,000 | within |
| investigator | 13,234 | 3,822 | same group figure | 1,486 | 1,500 | within |
| verifier | 24,229 | 5,448 | 23,963 (17.5 KB) | 3,112 | 3,000 | over by 112 |
| spec-writer | 12,584 | 2,933 | none | 1,667 | 1,500 | over by 167 |
| spec-critic | 13,080 | 2,838 | none | 1,572 | 1,500 | over by 72 |
| board-griller | 11,389 | 2,837 | 19,655 | section 1,914 (file 1,925) | section 2,000 | within |
| retro-critic | 12,319 | 2,738 | none | 1,565 | 1,500 | over by 65 |
| demo-explorer | 13,154 | 2,785 | same group figure | 1,612 | 1,500 | over by 112 |
| chief-of-staff | 202,936 | 24,351 | 202,396 (218 KB) | 5,999 | 6,000 | within |
| griller | 22,294 | 6,441 | 145,087 (36 KB) | 3,621 | 4,000 | within |
| foreman | 91,612 | 22,125 | 91,019 (144 KB) | 3,997 | 4,000 | within |

## The board Griller (sc19-Q1)

The board starts it with its fixed brief (`board/griller.py` `BRIEF`, 275 bytes unfilled) and the
user's words; it reads `references/griller.md`, section "Started from the board" first: 1,914
bytes (the file 1,925). Its `brief board-griller` file on the fixture is 2,837 bytes.

## Over target (Known gaps, Q4)

`release-driver.md` 3,809 (3,072), `spec-writer.md` 1,667 (1,500), `coder.md` 1,603 (1,500),
`verifier.md` 3,112 (3,000), `demo-explorer.md` 1,612 (1,500), `spec-critic.md` 1,572 (1,500),
`retro-critic.md` 1,565 (1,500). Every card is byte-identical to `cards-next/` at the base
(`git cat-file -s 88d9ab40:skills/chantier/cards-next/<card>` equals the head size): this CR
changes none of them. No target was raised.

## Boot targets of the Drivers

Child 20 also set whole-boot targets of 6, 6, 5 and 4 KB (CR, stack, release, QA driver) and
recorded that the cards alone cannot meet them (card, floor, facts and host rows). The briefs at
head are 9,773, 9,179, 9,531 and 6,032 bytes: over, as recorded there.
