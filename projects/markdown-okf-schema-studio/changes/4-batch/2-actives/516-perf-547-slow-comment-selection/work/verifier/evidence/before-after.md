# CR-516 Verifier: before and after

Before: base `1953eaaf08b1dcc7c071018abd4b0259acb0020e` (`origin/main`, the merge base).
After: pushed head `aeefa1b00c5a6bb0cfbc64e67de3994c3e904053`.

No screenshot or video: the change shows nothing new on screen; the pairs below are numbers and
page measurements. `<worktree>` is the CR's worktree, `<work>` the CR's work folder.

## How the "old code" build was made

An ignored directory of the worktree, `out/vbase`, instead of a second git worktree: the tests and
scripts of the head over the `src/` of the base. Run from `<worktree>` (removed at the end):

```
mkdir -p out/vbase
git archive HEAD src test scripts tsconfig.json package.json | tar -x -C out/vbase
rm -rf out/vbase/src
git archive origin/main src | tar -x -C out/vbase
rm out/vbase/test/core/preview/alignedFloat.test.ts   # imports a module the base does not have
cp .nvmrc out/vbase/
cd out/vbase && fnm exec -- node ../../node_modules/typescript/bin/tsc -p .
```

Its `src/` was equal to the base's: 410 files, every blob equal (`git ls-tree -r origin/main -- src`
against `git hash-object` of each file). `git diff origin/main HEAD -- scripts` is empty.

## Pairs

| Pair | Before | After | Shows |
| --- | --- | --- | --- |
| New and changed page tests | `new-tests-on-base-src.log`: 64 tests, 51 pass, 13 fail; restyle 3125 elements | `new-head-chromium.log` (6/6, restyle 26), `new-head-unit.log` (95/95) | the new-behaviour tests fail on the old code and pass on the new one |
| Layout, old against new | the base build, inside `layout-old-new.log` | the head build, same log | 256 comparisons, 0 with a difference |
| Mouse and keyboard behaviour, old against new | the base runtime page, inside `behaviour-old-new.log` | the head runtime page, same log | 93 step comparisons, 0 with a difference |
| Real VS Code window | runs 45895473044, 45895477080, 45896724578 at `1fc95289` (base `src/`) | runs 45918715713, 45918718450, 45918721402 at `e52cd28a` (carried to `aeefa1b0`) | `runs-check.log`: copies equal the forge artifacts; restyle 3109 to 41 |

## Reproduce

Before, in `<worktree>/out/vbase`:

```
STUDIO_REQUIRE_CHROMIUM=1 fnm exec -- node --import ./scripts/register-myst-patches.mjs --test --test-reporter=spec \
  out/test/page/commentRestyle.test.js out/test/page/alignedFloatLayout.test.js out/test/page/frameReadsInChromium.test.js \
  out/test/page/hoverFrames.test.js out/test/page/scrollSelection.test.js \
  out/test/page/modules/codeCopy.test.js out/test/page/modules/commentCompose.test.js
```

After, in `<worktree>` (after `fnm exec -- npm run compile`):

```
STUDIO_REQUIRE_CHROMIUM=1 fnm exec -- node --import ./scripts/register-myst-patches.mjs --test --test-reporter=spec \
  out/test/page/commentRestyle.test.js out/test/page/alignedFloatLayout.test.js out/test/page/frameReadsInChromium.test.js
STUDIO_REQUIRE_CHROMIUM=1 fnm exec -- node --import ./scripts/register-myst-patches.mjs --test --test-reporter=spec \
  out/test/page/hoverFrames.test.js out/test/page/scrollSelection.test.js out/test/page/modules/codeCopy.test.js \
  out/test/page/modules/commentCompose.test.js out/test/page/modules/commentEditorBehaviour.test.js \
  out/test/core/preview/alignedFloat.test.js out/test/page/linkEditModeClick.test.js
STUDIO_REQUIRE_CHROMIUM=1 fnm exec -- npm run test:breakout
```

Probes, in `<worktree>` with both builds present; the last argument is a new empty scratch folder:

```
fnm exec -- node --import ./scripts/register-myst-patches.mjs <work>/verifier/layout-compare.cjs <work>/scratch/<new folder>
fnm exec -- node --import ./scripts/register-myst-patches.mjs <work>/verifier/behaviour-compare.cjs <work>/scratch/<new folder>
```

Real-window runs: `gh run download <run id> --name perf-547-attempt-1 --dir <work>/scratch/artifacts-<run id>-verifier`,
then `fnm exec -- node <work>/verifier/runs-check.cjs`.
