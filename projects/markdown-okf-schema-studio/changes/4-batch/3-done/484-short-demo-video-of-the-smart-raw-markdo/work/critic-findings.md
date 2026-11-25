# Spec critic findings to apply (2026-11-25), none touches behaviour

1. Drop open questions 1 and 2: Q46 goes in section 8 (PR, `-assets` fallback), Q47 in section 4 (Comment button kept); list both under "Autonomous decisions" as the Griller's choices under Q45.
2. Section 7: the `clip-kit-test` recipe is `fnm exec -- node scripts/node-test.mjs clip-kit "docs/demo-video/clip-kit/lib/*.test.mjs"` (`node --test <dir>/` fails; the helper writes the JUnit report).
3. Section 6: also reword the recipe's lines made wrong by Size and Frame rate: section 5 trap row "the master is 1920x1080 whatever the scale"; section 3 table WebM "1920x1080, 30 fps" and poster "frame 0, 1920x1080"; section 3 "960 px wide (half the master)"; section 6 "the three named frames" (one more per mark); section 2 the `Mark <id>` "`-` for none" convention (keep or drop it explicitly).
4. `scenario.mjs` exports `EXPECTED`; `storyboard.test.mjs` asserts it equals the "Expected paste" fenced block of the shipped `clip.md`.
5. The parser skips lines inside fenced code blocks; the shipped-file test asserts section 2 has no `Step`/`Migrate` field.
6. Front matter `status: approved` (Q38, dated), with a note that times follow the batch's take; not `draft`.
