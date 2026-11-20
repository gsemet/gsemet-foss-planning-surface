# CR-351 before/after (Verifier)

Before: base 768570c0f6c317b0bacdb9360a96e50f3c136dd6 (CR-350's head, the CR's parent).
After: d4a00894f923617c3152d6067ec9491a59a3ac79 (pushed head).

No screen pair: the evidence plan names none (test-only change, "No visual change"). The
before/after of this CR is a width table, not a picture:

| Pair | What it shows | Where |
| --- | --- | --- |
| machine font vs pinned font | the twelve case widths and the tick matrix width with Segoe UI / Consolas (705 px) and with the pinned KaTeX fonts (719 px) | `work/verifier/matrix-r2.md`, W-nopin and W-pin, at d4a0089 |
| case 11 old text vs new text, pinned | old text 688 px, stays (fails its "breaks out" verdict); new text 894 px, breaks out | `work/verify.md`, claim C6, at d4a0089 |

Reproduce: the probe `work/scratch/fontProbe.test.ts` copied under `test/page/`, `npx tsc -p .`,
copy removed, then `node --import ./scripts/register-myst-patches.mjs --test out/test/page/<probe>.js`
(add `NO_PIN=1` for the machine font); remove the built probe afterwards.

Linux pair: not captured. No CI job runs the breakout tests in a browser (both `static` jobs skip
them, "no Chromium can start here"), and this session has no Linux run (see `work/verify.md`, C4).
