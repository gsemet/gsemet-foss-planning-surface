# Round 3 re-run: holes before and after (CR-450)

Command: `STUDIO_MUTATION_FILES=<the 19 files of work/logs/r3-sample-files.txt> just mutation-core`, run for real (compile, checker self-test, core phase, hole ranges, others phase, report reader). Baseline: `work/logs/r2-report-summary.json` (round 2, 51 sampled files). After: `work/logs/r3-report-summary.json`.

Exception to the Coder card: the run lasted about 33 minutes, so it went in a background shell, polled by the log (`work/logs/r3-run.log`, ends with `EXIT 0`).

## Run

| | value |
| --- | --- |
| wall clock | 33 min 18 s (14:35:40 to 15:09:00) |
| core phase | 14 min 55 s (1,744 mutants tested) |
| others phase | 17 min 50 s (1,492 mutants tested) |
| mutants in the report | 6,007 (unchanged: no src change) |
| statuses | 3,080 Killed, 384 Timeout, 729 Survived, 105 NoCoverage, 1,700 CompileError, 9 Ignored |
| tests run | 1,475, 163 test files, 0 left out |
| holes (sampled files and others) | 834 (was 1,289): 806 no test kills it, 28 killed only by another layer |

Machine: Windows 11, 16 logical processors, Node 24, concurrency 15.

## Holes per cluster (section 4 of holes-core.md)

A hole of the baseline counts as killed when it is no longer a hole of the new run (same file, line, column, mutator, replacement).

| # | Cluster | Holes before | Holes after | Killed |
|---|---|---|---|---|
| 1 | frontmatter/fileLinks.ts:139-224 | 47 | 21 | 26 |
| 2 | mapping/pastedImage.ts:19-19 | 2 | 0 | 2 |
| 3 | mapping/pastedImage.ts:29-33 | 4 | 2 | 2 |
| 4 | mapping/pastedImage.ts:41-50 | 9 | 1 | 8 |
| 5 | navigation/previewNavigation.ts:117-141 | 8 | 1 | 7 |
| 6 | navigation/previewNavigation.ts:39-44 | 5 | 0 | 5 |
| 7 | navigation/previewNavigation.ts:55-70 | 39 | 6 | 33 |
| 8 | protocol/hostToPage.ts:389-398 | 7 | 0 | 7 |
| 9 | comments/commentModel.ts:147-219 | 18 | 1 | 17 |
| 10 | myst/confLocator.ts:101-117 | 7 | 4 | 3 |
| 11 | mapping/labelRename.ts:40-61 | 17 | 8 | 9 |
| 12 | mapping/sourceMapping.ts:35-44 | 7 | 1 | 6 |
| 13 | mapping/textDiff.ts:8-29 | 42 | 4 | 38 |
| 14 | mapping/textDiff.ts:41-48 | 35 | 1 | 34 |
| 15 | paste/htmlToMarkdown.ts:49-65 | 18 | 0 | 18 |
| 16 | frontmatter/stemIndex.ts:141-143 | 7 | 3 | 4 |
| 17 | frontmatter/stemIndex.ts:161-193 | 12 | 4 | 8 |
| 18 | comments/inlineThread.ts:135-135 | 2 | 0 | 2 |
| 19 | frontmatter/sameData.ts:30-93 | 87 | 33 | 54 |
| 20 | frontmatter/schemaValidator.ts:52-63 | 18 | 3 | 15 |
| 21 | scroll/anchorPolicy.ts:79-85 | 11 | 1 | 10 |
| 22 | state/navigationHistory.ts:25-67 | 2 | 1 | 1 |
| 23 | navigation/openingPolicy.ts:36-36 | 1 | 0 | 1 |
| 24 | mapping/imageReference.ts:25-25 | 4 | 0 | 4 |
| 25 | preview/updatedRanges.ts:49-88 | 7 | 2 | 5 |
| | total | 416 | 97 | 319 |

319 of the 416 hole mutants of the clusters are killed (77%). 97 remain, listed below. `previewNavigation.ts:50` and `textDiff.ts:23` (`prefix <= limit`) are the two equivalents of holes-core.md section 1 (counted in the clusters, never killable).

## Score: no drop

Score per sub-folder, before (round 2) and after (this run). The sub-folders whose files were not sampled are carried over unchanged.

| Folder | Before | After |
|---|---|---|
| comments | 80 | 91.1 |
| configuration | 92.9 | 92.9 |
| directives | 86.2 | 86.2 |
| edits | 68.5 | 68.5 |
| export | 57.1 | 57.1 |
| find | 78.6 | 78.6 |
| frontmatter | 52.1 | 73.8 |
| mapping | 62.3 | 93.4 |
| myst | 80.2 | 84.0 |
| navigation | 72.1 | 95.0 |
| palette | 3.3 | 3.3 |
| paste | 54.6 | 58.5 |
| preview | 82.9 | 84.7 |
| protocol | 77.5 | 98.9 |
| render | 85.7 | 85.7 |
| scroll | 67.8 | 78.2 |
| security | 97.8 | 97.8 |
| state | 90 | 90.9 |
| syntax | 96.3 | 96.3 |


No sub-folder lost a point; the overall score of the 19 sampled files rose (comments +11.1, frontmatter +21.6, mapping +31.1, navigation +22.9, protocol +21.4, scroll +10.4, myst +3.7, paste +3.9, preview +1.8, state +0.9).

One mutant newly appears as a hole: `previewNavigation.ts:18:24` Regex (Survived). Cause not investigated (no test was removed or changed, no src change); to look at in a next round, likely a column shift or a kill credited to another test of the first run.

## Remaining cluster holes (97)

Why they remain, by group:

- fileLinks 176, 199-224 (21): the containment branch of a document-relative link and the `realpath` fallbacks. Several are NoCoverage (the catch of `realpathSync` on a broken link, which needs a link the disk cannot make here without privileges) and the `every` to `some` swaps need two navigation roots with a link contained by one only. Killable with a second root fixture; left for a next round.
- sameData 37-81 (33): the `a.has(value)` fast path of Set/Map comparison and the byte-array branch. Read, not proven: most look equivalent in effect (the slow path reaches the same verdict), the others need Set/Map members that are objects. Left, not worth more tests.
- previewNavigation 66-70 (6): regular expression variants of the heading id suffix that match the same inputs except on exotic whitespace.
- labelRename 46-51 (8): the CRLF trimming of the end of line; needs a document ending in a lone CR. Killable.
- stemIndex 141-172 (7), confLocator 101-117 (4), schemaValidator 52-62 (3), pastedImage 29-44 (3), textDiff 23-41 (5), others (one to two each): boundary or no-coverage variants; textDiff 25 and 41 (`prefix >= 0`, `suffix >= 0`) look equivalent by reading (the guard is redundant with `charCodeAt` returning NaN); not proven.

All 97 are classed "open" in `work/coder/r3.md`; none is a regression.

### Full list

- cluster 1: src/core/frontmatter/fileLinks.ts:176:72 MethodExpression -> `target.endsWith("\\\\")` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:199:8 EqualityOperator -> `navigationRoots.length >= 0` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:199:55 ArrayDeclaration -> `[]` (NoCoverage, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:200:7 ArrayDeclaration -> `[]` (NoCoverage, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:204:7 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:204:7 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:204:7 EqualityOperator -> `resolution !== "document-relative"` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:206:9 MethodExpression -> `containmentRoots.every(containmentRoot => isWithin(containmentRoot, candidate))` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:206:91 BlockStatement -> `{}` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:212:9 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:212:42 BlockStatement -> `{}` (NoCoverage, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:213:39 StringLiteral -> ```` (NoCoverage, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:215:9 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:215:78 BlockStatement -> `{}` (NoCoverage, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:216:39 StringLiteral -> ```` (NoCoverage, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:218:9 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:218:9 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:218:9 EqualityOperator -> `resolution !== "document-relative"` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:220:11 MethodExpression -> `containmentRoots.every(containmentRoot => { try { return isWithin(fs.realpathSyn` (Survived, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:223:17 BlockStatement -> `{}` (NoCoverage, no test kills it)
- cluster 1: src/core/frontmatter/fileLinks.ts:224:18 BooleanLiteral -> `true` (NoCoverage, no test kills it)
- cluster 3: src/core/mapping/pastedImage.ts:29:5 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 3: src/core/mapping/pastedImage.ts:29:21 ArithmeticOperator -> `offset - signature.length` (Survived, no test kills it)
- cluster 4: src/core/mapping/pastedImage.ts:44:5 ConditionalExpression -> `default:` (Survived, no test kills it)
- cluster 5: src/core/navigation/previewNavigation.ts:123:34 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 7: src/core/navigation/previewNavigation.ts:66:17 Regex -> `/^ {0,3}#{1,6}\s(.+?)\s*#*\s*$/u` (Survived, no test kills it)
- cluster 7: src/core/navigation/previewNavigation.ts:68:60 StringLiteral -> `"Stryker was here!"` (Survived, no test kills it)
- cluster 7: src/core/navigation/previewNavigation.ts:68:66 MethodExpression -> `lines[index]` (Survived, no test kills it)
- cluster 7: src/core/navigation/previewNavigation.ts:69:39 Regex -> `/\S*\{#([^}\s]+)\}\s*$/u` (Survived, no test kills it)
- cluster 7: src/core/navigation/previewNavigation.ts:69:39 Regex -> `/\s*\{#([^}\s]+)\}\S*$/u` (Survived, no test kills it)
- cluster 7: src/core/navigation/previewNavigation.ts:70:42 Regex -> `/\s*\{#[^}\s]+\}\S*$/u` (Survived, no test kills it)
- cluster 9: src/core/comments/commentModel.ts:147:7 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 10: src/core/myst/confLocator.ts:101:19 EqualityOperator -> `now() - cached.checkedAt <= CONF_RECHECK_MS` (Survived, no test kills it)
- cluster 10: src/core/myst/confLocator.ts:117:28 ArrayDeclaration -> `["Stryker was here"]` (NoCoverage, no test kills it)
- cluster 10: src/core/myst/confLocator.ts:117:48 ArrayDeclaration -> `["Stryker was here"]` (NoCoverage, no test kills it)
- cluster 10: src/core/myst/confLocator.ts:117:61 BooleanLiteral -> `true` (NoCoverage, no test kills it)
- cluster 11: src/core/mapping/labelRename.ts:46:9 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 11: src/core/mapping/labelRename.ts:51:7 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 11: src/core/mapping/labelRename.ts:51:7 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 11: src/core/mapping/labelRename.ts:51:7 EqualityOperator -> `end >= start` (Survived, no test kills it)
- cluster 11: src/core/mapping/labelRename.ts:51:7 EqualityOperator -> `end <= start` (Survived, no test kills it)
- cluster 11: src/core/mapping/labelRename.ts:51:27 ArithmeticOperator -> `end + 1` (Survived, no test kills it)
- cluster 11: src/core/mapping/labelRename.ts:51:40 StringLiteral -> `""` (Survived, no test kills it)
- cluster 11: src/core/mapping/labelRename.ts:51:46 AssignmentOperator -> `end += 1` (Survived, no test kills it)
- cluster 12: src/core/mapping/sourceMapping.ts:44:9 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 13: src/core/mapping/textDiff.ts:23:10 EqualityOperator -> `prefix <= limit` (Survived, no test kills it)
- cluster 13: src/core/mapping/textDiff.ts:23:10 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 13: src/core/mapping/textDiff.ts:25:10 EqualityOperator -> `prefix >= 0` (Survived, no test kills it)
- cluster 13: src/core/mapping/textDiff.ts:25:10 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 14: src/core/mapping/textDiff.ts:41:10 EqualityOperator -> `suffix >= 0` (Survived, no test kills it)
- cluster 16: src/core/frontmatter/stemIndex.ts:141:12 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 16: src/core/frontmatter/stemIndex.ts:141:31 BooleanLiteral -> `entry.isSymbolicLink()` (NoCoverage, no test kills it)
- cluster 16: src/core/frontmatter/stemIndex.ts:143:12 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 17: src/core/frontmatter/stemIndex.ts:161:61 StringLiteral -> `""` (Survived, no test kills it)
- cluster 17: src/core/frontmatter/stemIndex.ts:169:13 BlockStatement -> `{}` (NoCoverage, no test kills it)
- cluster 17: src/core/frontmatter/stemIndex.ts:170:14 StringLiteral -> ```` (NoCoverage, no test kills it)
- cluster 17: src/core/frontmatter/stemIndex.ts:172:11 StringLiteral -> `""` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:37:21 MethodExpression -> `[...b]` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:37:46 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:37:46 LogicalOperator -> `typeof value === "object" && value !== null || !a.has(value)` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:37:46 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:37:46 LogicalOperator -> `typeof value === "object" || value !== null` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:37:46 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:37:75 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:40:9 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:40:9 LogicalOperator -> `typeof value !== "object" && value === null` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:40:9 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:40:38 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:50:21 MethodExpression -> `[...b.keys()]` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:50:51 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:50:51 LogicalOperator -> `typeof key === "object" && key !== null || !a.has(key)` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:50:51 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:50:51 LogicalOperator -> `typeof key === "object" || key !== null` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:50:51 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:50:78 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:56:9 LogicalOperator -> `typeof key !== "object" && key === null` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:56:9 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:56:9 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:56:36 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:68:25 EqualityOperator -> `index <= a.length` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:68:55 BlockStatement -> `{}` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:69:11 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:70:11 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:77:30 BlockStatement -> `{}` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:81:9 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:81:9 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:81:9 LogicalOperator -> `left.length !== right.length && left.some((byte, index) => byte !== right[index]` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:81:41 MethodExpression -> `left.every((byte, index) => byte !== right[index])` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:81:51 ArrowFunction -> `() => undefined` (Survived, no test kills it)
- cluster 19: src/core/frontmatter/sameData.ts:81:68 ConditionalExpression -> `false` (Survived, no test kills it)
- cluster 20: src/core/frontmatter/schemaValidator.ts:52:25 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 20: src/core/frontmatter/schemaValidator.ts:62:7 ConditionalExpression -> `false` (NoCoverage, no test kills it)
- cluster 20: src/core/frontmatter/schemaValidator.ts:62:18 BooleanLiteral -> `true` (NoCoverage, no test kills it)
- cluster 21: src/core/scroll/anchorPolicy.ts:79:12 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 22: src/core/state/navigationHistory.ts:25:9 EqualityOperator -> `this.entries.length >= NAVIGATION_HISTORY_CAP` (Survived, no test kills it)
- cluster 25: src/core/preview/updatedRanges.ts:49:32 ConditionalExpression -> `true` (Survived, no test kills it)
- cluster 25: src/core/preview/updatedRanges.ts:49:32 EqualityOperator -> `selections.length >= 0` (Survived, no test kills it)
    
