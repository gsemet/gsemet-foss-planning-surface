# Holes of src/core (CR-450, round 2, spec 4.9 and 4.10)

> Status after round 3: the figures and lists below are the round-2 baseline. Round 3 added 19 test files and re-ran the real machinery on the 19 files concerned: of the 416 cluster holes, 319 are killed and 97 remain (see `r3-rerun.md`, holes before and after per cluster, and the open list). No score dropped.

A hole is a mutant that no test of `test/core` kills (Survived or NoCoverage) in the core phase of the real run (sample of 51 files, 6,007 mutants). The others phase then ran the tests of the other layers on the holes' ranges: a hole one of them kills is labelled "killed only by another layer", the rest "no test kills it".

## Figures

| | holes |
| --- | --- |
| all holes (Survived + NoCoverage) | 1289 |
| listed as equivalent, apart | 2 |
| listed below | 1287 |
| no test kills it | 1252 |
| killed only by another layer | 35 |
| Survived / NoCoverage (listed below) | 1102 / 185 |
| holes in the numbered clusters (test-worthy, section 4) | 415 |

How each one is read: the 'Where tagged' column of the per-file list gives the cluster number (section 4) or the not-worth category (section 3). Timeouts of the others phase are not counted as kills (see the note, decision on Timeouts): 9 hole(s) timed out in another layer.

## 1. Equivalent mutants (listed apart)

Found by reading the code, not proven; two among the holes read for this triage. Everything else was judged observable.

| file:line | mutator | why equivalent |
| --- | --- | --- |
| navigation/previewNavigation.ts:50 | EqualityOperator | the loop bound `index < lines.length` becomes `<=`: the extra pass reads `lines[length]` (undefined), every regular expression and the next-line test then fail on it, nothing is returned; no observable difference. |
| mapping/textDiff.ts:23 | EqualityOperator | `prefix < limit` becomes `prefix <= limit`: at `prefix == limit` one of the two `charCodeAt` calls is NaN, `NaN === x` is false, the loop stops before `prefix += 1`; same result. |

## 2. Every hole, by file

Format: `line:column Mutator -> replacement` then the label and the tag. `NC` = NoCoverage (no test reaches the line), `S` = Survived. A killed-only-by-another-layer hole names the other-layer test.

### comments/commentModel.ts (46)

```text
55:18 S Regex -> /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z|[+-]\d{2}: | no test kills it | regex
55:18 S Regex -> /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z|[+-]\d{2} | no test kills it | regex
55:18 S Regex -> /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)(?:Z|[+-]\d{2}: | no test kills it | regex
55:18 S Regex -> /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z|[+-]\d:\d | no test kills it | regex
55:18 S Regex -> /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z|[^+-]\d{2 | no test kills it | regex
55:18 S Regex -> /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z|[+-]\D{2} | no test kills it | regex
55:18 S Regex -> /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z|[+-]\d{2} | no test kills it | regex
55:18 S Regex -> /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,9})?)?(?:Z|[+-]\d{2} | no test kills it | regex
59:39 S ConditionalExpression -> true | no test kills it | other
59:39 S EqualityOperator -> value.length < 40 | no test kills it | other
82:17 S MethodExpression -> Math.min(documentName.lastIndexOf("/"), documentName.lastIndexOf("\\") | no test kills it | other
86:16 S EqualityOperator -> dot >= 0 | no test kills it | other
92:17 S StringLiteral -> `` | no test kills it | message
97:17 S StringLiteral -> `` | no test kills it | message
101:17 S StringLiteral -> `` | no test kills it | message
109:17 NC StringLiteral -> `` | no test kills it | message
114:17 S StringLiteral -> `` | no test kills it | message
122:17 NC StringLiteral -> `` | no test kills it | message
127:17 S StringLiteral -> `` | no test kills it | message
131:17 S StringLiteral -> `` | no test kills it | message
135:73 S StringLiteral -> `` | no test kills it | message
136:18 S MethodExpression -> parsed.every(comment => comment === undefined) | no test kills it | other
136:30 S ArrowFunction -> () => undefined | no test kills it | other
136:43 S ConditionalExpression -> false | no test kills it | other
143:55 S ArrayDeclaration -> ["Stryker was here"] | no test kills it | other
144:31 S StringLiteral -> "Stryker was here!" | no test kills it | message
145:7 S ConditionalExpression -> false | no test kills it | other
145:48 NC StringLiteral -> "" | no test kills it | string
147:7 S LogicalOperator -> text.length > MAX_SIDECAR_BYTES && new TextEncoder().encode(text).leng | no test kills it | cluster 9
147:7 S ConditionalExpression -> false | no test kills it | cluster 9
147:7 S EqualityOperator -> text.length >= MAX_SIDECAR_BYTES | no test kills it | cluster 9
147:42 S ConditionalExpression -> false | no test kills it | cluster 9
147:42 S EqualityOperator -> new TextEncoder().encode(text).length >= MAX_SIDECAR_BYTES | no test kills it | cluster 9
148:20 S StringLiteral -> `` | no test kills it | cluster 9
153:11 S BlockStatement -> {} | no test kills it | cluster 9
154:20 S StringLiteral -> "" | no test kills it | cluster 9
156:39 S StringLiteral -> "" | no test kills it | cluster 9
157:56 S StringLiteral -> `` | no test kills it | cluster 9
158:49 S StringLiteral -> "" | no test kills it | cluster 9
159:52 S StringLiteral -> "" | no test kills it | cluster 9
160:57 S StringLiteral -> `` | no test kills it | cluster 9
165:43 S StringLiteral -> `` | no test kills it | cluster 9
168:19 S StringLiteral -> `` | no test kills it | cluster 9
216:45 S EqualityOperator -> endLine > line | only another layer: session/reviewReqComments.requirements.test.js | cluster 9
218:38 S EqualityOperator -> prefix.length < MAX_CONTEXT_LENGTH | no test kills it | cluster 9
219:38 S EqualityOperator -> suffix.length < MAX_CONTEXT_LENGTH | no test kills it | cluster 9
```

### comments/inlineThread.ts (33)

```text
30:20 S Regex -> /THREAD[ \t]*(?:\r?\n|$)/u | no test kills it | regex
30:20 S Regex -> /^THREAD[ \t]*(?:\r?\n)/u | no test kills it | regex
31:16 S Regex -> /(?: {1,2}|\t)/u | no test kills it | regex
57:11 S ConditionalExpression -> false | no test kills it | other
57:20 S StringLiteral -> "Stryker was here!" | no test kills it | string
66:44 S Regex -> /^\n/u | no test kills it | regex
66:53 S StringLiteral -> "Stryker was here!" | no test kills it | message
66:65 S Regex -> /\n$/u | no test kills it | regex
66:74 S StringLiteral -> "Stryker was here!" | no test kills it | message
80:74 S Regex -> /\s/gu | no test kills it | regex
81:10 S ConditionalExpression -> false | no test kills it | other
81:22 S StringLiteral -> "Stryker was here!" | no test kills it | string
81:27 NC StringLiteral -> "" | no test kills it | string
86:16 S MethodExpression -> text.replace(/\r\n?/gu, "\n").replace(/-->/gu, "-- >") | no test kills it | other
86:29 S Regex -> /\r\n/gu | no test kills it | regex
86:40 S StringLiteral -> "" | no test kills it | string
89:34 S Regex -> /[ \t]$/u | no test kills it | regex
89:46 S StringLiteral -> "Stryker was here!" | no test kills it | string
90:16 S ConditionalExpression -> false | no test kills it | other
90:28 S StringLiteral -> "Stryker was here!" | no test kills it | string
90:33 NC StringLiteral -> "Stryker was here!" | no test kills it | string
112:17 S Regex -> /<!--([\s\S]*?)-->$/u | no test kills it | regex
120:32 S ConditionalExpression -> true | no test kills it | other
120:112 S Regex -> /\r/u | no test kills it | regex
120:120 S StringLiteral -> "Stryker was here!" | no test kills it | string
135:55 S ConditionalExpression -> false | no test kills it | cluster 18
135:55 S EqualityOperator -> text.length >= MAX_THREAD_REPLY_LENGTH | no test kills it | cluster 18
137:41 S Regex -> /\r/u | no test kills it | regex
137:49 S StringLiteral -> "Stryker was here!" | no test kills it | string
139:7 S ConditionalExpression -> false | no test kills it | other
142:18 S Regex -> /[ \t]*/u | no test kills it | regex
149:70 S Regex -> /[ \t]$/u | no test kills it | regex
163:78 S MethodExpression -> line | no test kills it | other
```

### configuration/editorAssociationMigration.ts (4)

```text
8:40 S StringLiteral -> "" | only another layer: host/openingWatcher.test.js | data
33:44 S ConditionalExpression -> true | no test kills it | other
33:44 S LogicalOperator -> isRecord(entry) || entry.filenamePattern === MARKDOWN_PATTERN | no test kills it | other
34:10 S ConditionalExpression -> true | no test kills it | other
```

### directives/registry.ts (4)

```text
40:9 S ConditionalExpression -> false | no test kills it | other
40:48 NC BlockStatement -> {} | no test kills it | other
41:7 NC CallExpression -> ; | no test kills it | other
43:9 S ConditionalExpression -> false | no test kills it | other
```

### edits/textEdit.ts (17)

```text
32:51 S LogicalOperator -> left.start - right.start && left.end - right.end | no test kills it | other
32:79 NC ArithmeticOperator -> left.end + right.end | no test kills it | other
36:9 S ConditionalExpression -> false | no test kills it | other
36:9 S LogicalOperator -> !Number.isSafeInteger(edit.start) && !Number.isSafeInteger(edit.end) | no test kills it | other
72:42 S BlockStatement -> {} | no test kills it | other
73:9 S LogicalOperator -> (!Number.isSafeInteger(index) || index < 0) && index >= starts.length | no test kills it | other
73:9 S ConditionalExpression -> false | no test kills it | other
73:9 S ConditionalExpression -> false | no test kills it | other
73:9 S LogicalOperator -> !Number.isSafeInteger(index) && index < 0 | no test kills it | other
73:41 S ConditionalExpression -> false | no test kills it | other
73:54 S EqualityOperator -> index > starts.length | no test kills it | other
73:54 S ConditionalExpression -> false | no test kills it | other
73:78 NC BlockStatement -> {} | no test kills it | other
74:7 NC CallExpression -> ; | no test kills it | other
80:7 S CallExpression -> ; | no test kills it | other
84:7 S CallExpression -> ; | no test kills it | other
88:7 S CallExpression -> ; | no test kills it | other
```

### export/htmlExport.ts (9)

```text
50:59 S ConditionalExpression -> false | no test kills it | other
50:59 S ConditionalExpression -> true | no test kills it | other
50:59 S ConditionalExpression -> false | no test kills it | other
50:68 S StringLiteral -> "" | no test kills it | string
50:75 S ConditionalExpression -> false | no test kills it | other
50:75 S EqualityOperator -> kind !== "3" | no test kills it | other
50:84 S StringLiteral -> "" | no test kills it | string
66:11 S StringLiteral -> "Stryker was here!" | no test kills it | string
75:118 S StringLiteral -> "" | no test kills it | string
```

### find/findMatches.ts (15)

```text
45:62 S StringLiteral -> "" | no test kills it | string
47:68 S Regex -> /Invalid regular expression: /u | no test kills it | regex
47:102 S StringLiteral -> "Stryker was here!" | no test kills it | message
47:108 NC StringLiteral -> "" | no test kills it | message
58:68 S StringLiteral -> "" | no test kills it | string
58:91 NC StringLiteral -> `` | no test kills it | string
77:27 S Regex -> /\$(\$|&|<([^>]*)>|(\d))/gu | no test kills it | regex
79:49 NC StringLiteral -> "Stryker was here!" | no test kills it | string
83:9 S ConditionalExpression -> true | no test kills it | other
83:9 S LogicalOperator -> index >= match.groups.length || (digits as string).length === 2 | no test kills it | other
83:9 S EqualityOperator -> index > match.groups.length | no test kills it | other
83:9 S ConditionalExpression -> true | no test kills it | other
83:41 S ConditionalExpression -> true | no test kills it | other
84:9 S ConditionalExpression -> false | no test kills it | other
86:36 NC StringLiteral -> "Stryker was here!" | no test kills it | string
```

### frontmatter/fileLinks.ts (104)

```text
49:7 S ConditionalExpression -> false | no test kills it | other
49:7 S BooleanLiteral -> annotation.tooltipShowsFields?.length | no test kills it | other
50:8 S BooleanLiteral -> annotation.showLineNumber | no test kills it | other
53:55 S Regex -> /\uFEFF/u | no test kills it | regex
55:43 S ConditionalExpression -> true | no test kills it | other
58:35 S ArrayDeclaration -> ["Stryker was here"] | no test kills it | other
60:42 S ConditionalExpression -> false | no test kills it | other
60:71 S ConditionalExpression -> false | no test kills it | other
66:22 S MethodExpression -> annotation.idMarker | no test kills it | other
85:11 NC BlockStatement -> {} | no test kills it | catch
92:10 S ConditionalExpression -> false | no test kills it | other
92:23 S StringLiteral -> "Stryker was here!" | no test kills it | string
98:9 S ConditionalExpression -> false | no test kills it | other
100:9 S ConditionalExpression -> true | no test kills it | other
100:9 S EqualityOperator -> parent !== current | no test kills it | other
111:8 S MethodExpression -> configured | no test kills it | other
111:48 S BooleanLiteral -> true | no test kills it | other
112:17 S MethodExpression -> configured | no test kills it | other
115:7 NC ArrayDeclaration -> [] | no test kills it | other
115:21 NC LogicalOperator -> workspaceRoots[0] && path.dirname(filePath) | no test kills it | other
118:77 S ConditionalExpression -> true | no test kills it | other
125:21 NC BooleanLiteral -> isWithin(candidate, path.resolve(filePath)) | no test kills it | other
126:21 NC MethodExpression -> ["index.md", "log.md"].every(name => fs.statSync(path.join(candidate,  | no test kills it | other
126:21 NC ArrayDeclaration -> [] | no test kills it | other
126:22 NC StringLiteral -> "" | no test kills it | string
126:34 NC StringLiteral -> "" | no test kills it | string
126:49 NC ArrowFunction -> () => undefined | no test kills it | other
126:99 NC ObjectLiteral -> {} | only another layer: page/fmtableReqFrontmatter.requirements.test.js | other
126:117 NC BooleanLiteral -> true | only another layer: page/fmtableReqFrontmatter.requirements.test.js | other
133:36 S ArrayDeclaration -> ["Stryker was here"] | no test kills it | other
138:52 NC ArrayDeclaration -> ["Stryker was here"] | no test kills it | other
139:39 S ConditionalExpression -> false | no test kills it | cluster 1
139:39 S EqualityOperator -> workspaceRoots.length >= 0 | no test kills it | cluster 1
139:39 S ConditionalExpression -> true | no test kills it | cluster 1
139:39 S EqualityOperator -> workspaceRoots.length <= 0 | no test kills it | cluster 1
141:7 NC ArrayDeclaration -> [] | no test kills it | cluster 1
150:7 S ConditionalExpression -> false | no test kills it | cluster 1
150:30 S MethodExpression -> navigationRoots.every(root => isWithin(root, detectedProjectRoot)) | no test kills it | cluster 1
150:51 S ArrowFunction -> () => undefined | no test kills it | cluster 1
176:37 S Regex -> /[A-Za-z]:[\\/]/u | no test kills it | cluster 1
176:37 S Regex -> /^[^A-Za-z]:[\\/]/u | no test kills it | cluster 1
176:37 S Regex -> /^[A-Za-z]:[^\\/]/u | no test kills it | cluster 1
176:72 S MethodExpression -> target.endsWith("\\\\") | no test kills it | cluster 1
190:24 S LogicalOperator -> rootPath(path.dirname(path.resolve(options.filePath))) && path.dirname | no test kills it | cluster 1
192:16 S ConditionalExpression -> true | no test kills it | cluster 1
194:7 NC MethodExpression -> resolution.endsWith("bundle-relative") | no test kills it | cluster 1
194:29 NC StringLiteral -> "" | no test kills it | cluster 1
195:46 NC StringLiteral -> `` | no test kills it | cluster 1
196:28 S ConditionalExpression -> false | no test kills it | cluster 1
196:68 NC StringLiteral -> `` | no test kills it | cluster 1
198:28 S EqualityOperator -> resolution !== "document-relative" | no test kills it | cluster 1
199:8 S ConditionalExpression -> false | no test kills it | cluster 1
199:8 S EqualityOperator -> navigationRoots.length <= 0 | no test kills it | cluster 1
199:8 S EqualityOperator -> navigationRoots.length >= 0 | no test kills it | cluster 1
199:55 NC ArrayDeclaration -> [] | no test kills it | cluster 1
200:7 NC ArrayDeclaration -> [] | no test kills it | cluster 1
201:7 S ConditionalExpression -> false | no test kills it | cluster 1
201:45 NC BooleanLiteral -> isWithin(root, candidate) | no test kills it | cluster 1
201:73 NC BlockStatement -> {} | no test kills it | cluster 1
202:37 NC StringLiteral -> `` | no test kills it | cluster 1
204:7 S ConditionalExpression -> false | no test kills it | cluster 1
204:7 S ConditionalExpression -> true | no test kills it | cluster 1
204:7 S EqualityOperator -> resolution !== "document-relative" | no test kills it | cluster 1
206:9 S MethodExpression -> containmentRoots.every(containmentRoot => isWithin(containmentRoot, ca | no test kills it | cluster 1
206:91 S BlockStatement -> {} | no test kills it | cluster 1
212:9 S ConditionalExpression -> false | no test kills it | cluster 1
212:42 NC BlockStatement -> {} | no test kills it | cluster 1
213:39 NC StringLiteral -> `` | no test kills it | cluster 1
215:9 S ConditionalExpression -> false | no test kills it | cluster 1
215:47 NC BooleanLiteral -> isWithin(realRoot, realPath) | no test kills it | cluster 1
215:78 NC BlockStatement -> {} | no test kills it | cluster 1
216:39 NC StringLiteral -> `` | no test kills it | cluster 1
218:9 S ConditionalExpression -> false | no test kills it | cluster 1
218:9 S ConditionalExpression -> true | no test kills it | cluster 1
218:9 S EqualityOperator -> resolution !== "document-relative" | no test kills it | cluster 1
220:11 S MethodExpression -> containmentRoots.every(containmentRoot => { try { return isWithin(fs.r | no test kills it | cluster 1
223:17 NC BlockStatement -> {} | no test kills it | cluster 1
224:18 NC BooleanLiteral -> true | no test kills it | cluster 1
226:11 NC BlockStatement -> {} | no test kills it | other
227:39 NC StringLiteral -> `` | no test kills it | string
231:37 NC StringLiteral -> `` | no test kills it | string
242:7 S ConditionalExpression -> false | no test kills it | other
242:63 NC StringLiteral -> `` | no test kills it | string
243:7 S ConditionalExpression -> false | no test kills it | other
243:59 NC StringLiteral -> "" | no test kills it | string
254:7 S ConditionalExpression -> true | no test kills it | other
257:11 NC StringLiteral -> `` | no test kills it | string
259:11 NC StringLiteral -> `` | no test kills it | string
260:11 S StringLiteral -> `` | no test kills it | string
263:7 S ConditionalExpression -> false | no test kills it | other
263:65 NC StringLiteral -> `` | no test kills it | string
287:13 S ConditionalExpression -> false | no test kills it | other
299:25 S LogicalOperator -> (navigationRoots.find(root => isWithin(root, filePath)) ?? navigationR | no test kills it | other
299:46 S ArrowFunction -> () => undefined | no test kills it | other
303:11 S LogicalOperator -> relative && path.basename(filePath) | no test kills it | other
303:69 S StringLiteral -> "" | no test kills it | string
325:7 NC CallExpression -> ; | no test kills it | other
328:43 S LogicalOperator -> item.arrayIndex && "scalar" | no test kills it | other
328:62 S StringLiteral -> "" | no test kills it | string
329:9 S ConditionalExpression -> false | no test kills it | other
330:5 S CallExpression -> ; | no test kills it | other
356:33 NC ArrayDeclaration -> ["Stryker was here"] | no test kills it | other
366:35 NC ArrayDeclaration -> ["Stryker was here"] | no test kills it | other
387:35 NC ArrayDeclaration -> ["Stryker was here"] | no test kills it | other
```

### frontmatter/frontmatterChanges.ts (14)

```text
28:56 S EqualityOperator -> index <= offset | no test kills it | other
53:12 S ConditionalExpression -> false | no test kills it | other
53:12 S ConditionalExpression -> true | no test kills it | other
53:12 S EqualityOperator -> endOffset <= startOffset + 1 | no test kills it | other
53:12 S EqualityOperator -> endOffset >= startOffset + 1 | no test kills it | other
53:24 S ArithmeticOperator -> startOffset - 1 | no test kills it | other
53:43 S Regex -> /\S/u | no test kills it | regex
53:54 S LogicalOperator -> body[endOffset - 1] && "" | no test kills it | other
53:59 S ArithmeticOperator -> endOffset + 1 | no test kills it | other
53:77 NC StringLiteral -> "Stryker was here!" | no test kills it | string
65:7 S ConditionalExpression -> false | no test kills it | other
69:47 NC StringLiteral -> "" | no test kills it | string
105:10 S ConditionalExpression -> false | no test kills it | other
105:31 S EqualityOperator -> ranges[0].start < 1 | no test kills it | other
```

### frontmatter/sameData.ts (96)

```text
25:9 S ConditionalExpression -> false | no test kills it | other
28:20 S MethodExpression -> Object.getOwnPropertySymbols(a) | no test kills it | other
28:59 S ArrowFunction -> () => undefined | no test kills it | other
29:20 S MethodExpression -> Object.getOwnPropertySymbols(b) | no test kills it | other
29:59 S ArrowFunction -> () => undefined | no test kills it | other
30:7 S ConditionalExpression -> false | no test kills it | cluster 19
30:51 NC BooleanLiteral -> true | no test kills it | cluster 19
31:25 S ArrowFunction -> () => undefined | no test kills it | cluster 19
31:37 NC ConditionalExpression -> false | no test kills it | cluster 19
31:37 NC ConditionalExpression -> true | no test kills it | cluster 19
31:37 NC LogicalOperator -> Object.prototype.propertyIsEnumerable.call(b, symbol) || same((a as Re | no test kills it | cluster 19
36:7 S ConditionalExpression -> false | no test kills it | cluster 19
37:21 S MethodExpression -> [...b] | no test kills it | cluster 19
37:21 S ArrayDeclaration -> [] | no test kills it | cluster 19
37:35 S ArrowFunction -> () => undefined | no test kills it | cluster 19
37:46 S ConditionalExpression -> true | no test kills it | cluster 19
37:46 S LogicalOperator -> typeof value === "object" && value !== null || !a.has(value) | no test kills it | cluster 19
37:46 S ConditionalExpression -> false | no test kills it | cluster 19
37:46 S ConditionalExpression -> true | no test kills it | cluster 19
37:46 S LogicalOperator -> typeof value === "object" || value !== null | no test kills it | cluster 19
37:46 S EqualityOperator -> typeof value !== "object" | no test kills it | cluster 19
37:46 S ConditionalExpression -> true | no test kills it | cluster 19
37:75 S ConditionalExpression -> true | no test kills it | cluster 19
37:75 S EqualityOperator -> value === null | no test kills it | cluster 19
37:93 S BooleanLiteral -> a.has(value) | no test kills it | cluster 19
40:9 S ConditionalExpression -> true | no test kills it | cluster 19
40:9 S ConditionalExpression -> false | no test kills it | cluster 19
40:9 S EqualityOperator -> typeof value === "object" | no test kills it | cluster 19
40:9 S LogicalOperator -> typeof value !== "object" && value === null | no test kills it | cluster 19
40:9 S ConditionalExpression -> false | no test kills it | cluster 19
40:38 S ConditionalExpression -> false | no test kills it | cluster 19
40:38 S EqualityOperator -> value !== null | no test kills it | cluster 19
40:61 NC BooleanLiteral -> true | no test kills it | cluster 19
41:39 S ArrowFunction -> () => undefined | no test kills it | cluster 19
42:9 S ConditionalExpression -> true | no test kills it | cluster 19
42:9 S EqualityOperator -> index <= 0 | no test kills it | cluster 19
43:5 NC CallExpression -> ; | no test kills it | cluster 19
49:7 S ConditionalExpression -> true | no test kills it | cluster 19
49:7 S ConditionalExpression -> false | no test kills it | cluster 19
49:7 S EqualityOperator -> a.size === b.size | no test kills it | cluster 19
49:33 NC BooleanLiteral -> true | no test kills it | cluster 19
50:21 S MethodExpression -> [...b.keys()] | no test kills it | cluster 19
50:21 S ArrayDeclaration -> [] | no test kills it | cluster 19
50:42 S ArrowFunction -> () => undefined | no test kills it | cluster 19
50:51 S ConditionalExpression -> true | no test kills it | cluster 19
50:51 S LogicalOperator -> typeof key === "object" && key !== null || !a.has(key) | no test kills it | cluster 19
50:51 S ConditionalExpression -> false | no test kills it | cluster 19
50:51 S ConditionalExpression -> true | no test kills it | cluster 19
50:51 S LogicalOperator -> typeof key === "object" || key !== null | no test kills it | cluster 19
50:51 S EqualityOperator -> typeof key !== "object" | no test kills it | cluster 19
50:51 S ConditionalExpression -> true | no test kills it | cluster 19
50:78 S ConditionalExpression -> true | no test kills it | cluster 19
50:78 S EqualityOperator -> key === null | no test kills it | cluster 19
50:94 S BooleanLiteral -> a.has(key) | no test kills it | cluster 19
52:9 S ConditionalExpression -> true | no test kills it | cluster 19
52:9 S ConditionalExpression -> false | no test kills it | cluster 19
52:21 S BlockStatement -> {} | no test kills it | cluster 19
53:11 S ConditionalExpression -> true | no test kills it | cluster 19
56:9 S ConditionalExpression -> true | no test kills it | cluster 19
56:9 S LogicalOperator -> typeof key !== "object" && key === null | no test kills it | cluster 19
56:9 S ConditionalExpression -> false | no test kills it | cluster 19
56:9 S ConditionalExpression -> false | no test kills it | cluster 19
56:9 S EqualityOperator -> typeof key === "object" | no test kills it | cluster 19
56:36 S EqualityOperator -> key !== null | no test kills it | cluster 19
56:36 S ConditionalExpression -> false | no test kills it | cluster 19
57:39 S ArrowFunction -> () => undefined | no test kills it | cluster 19
57:54 S ConditionalExpression -> false | no test kills it | cluster 19
58:9 S EqualityOperator -> index <= 0 | no test kills it | cluster 19
58:9 S ConditionalExpression -> true | no test kills it | cluster 19
59:5 NC CallExpression -> ; | no test kills it | cluster 19
61:10 NC BooleanLiteral -> false | no test kills it | cluster 19
65:25 S BlockStatement -> {} | no test kills it | cluster 19
67:9 S ConditionalExpression -> false | no test kills it | cluster 19
68:25 S EqualityOperator -> index <= a.length | no test kills it | cluster 19
68:55 S BlockStatement -> {} | no test kills it | cluster 19
69:11 S ConditionalExpression -> false | no test kills it | cluster 19
70:11 S ConditionalExpression -> false | no test kills it | cluster 19
75:12 S ConditionalExpression -> false | no test kills it | cluster 19
77:30 S BlockStatement -> {} | no test kills it | cluster 19
81:9 S ConditionalExpression -> true | no test kills it | cluster 19
81:9 S ConditionalExpression -> false | no test kills it | cluster 19
81:9 S ConditionalExpression -> false | no test kills it | cluster 19
81:9 S EqualityOperator -> left.length === right.length | no test kills it | cluster 19
81:9 S LogicalOperator -> left.length !== right.length && left.some((byte, index) => byte !== ri | no test kills it | cluster 19
81:41 S MethodExpression -> left.every((byte, index) => byte !== right[index]) | no test kills it | cluster 19
81:51 S ArrowFunction -> () => undefined | no test kills it | cluster 19
81:68 S ConditionalExpression -> false | no test kills it | cluster 19
81:68 S ConditionalExpression -> true | no test kills it | cluster 19
81:68 S EqualityOperator -> byte === right[index] | no test kills it | cluster 19
85:32 S ConditionalExpression -> false | no test kills it | cluster 19
93:7 S ConditionalExpression -> false | no test kills it | cluster 19
93:87 NC BooleanLiteral -> true | no test kills it | cluster 19
96:7 S LogicalOperator -> leftDepth !== undefined && rightDepth !== undefined | no test kills it | other
96:7 S ConditionalExpression -> false | no test kills it | other
96:34 S ConditionalExpression -> false | no test kills it | other
102:13 S BlockStatement -> {} | no test kills it | other
```

### frontmatter/schemaRegistry.ts (8)

```text
31:35 S ArrowFunction -> () => undefined | no test kills it | other
34:5 NC CallExpression -> ; | no test kills it | other
35:5 NC CallExpression -> ; | no test kills it | other
43:5 S CallExpression -> ; | no test kills it | other
48:53 S BlockStatement -> {} | no test kills it | other
49:41 S BlockStatement -> {} | no test kills it | other
50:5 S CallExpression -> ; | no test kills it | other
52:3 S CallExpression -> ; | no test kills it | other
```

### frontmatter/schemaValidator.ts (38)

```text
25:19 S ConditionalExpression -> true | no test kills it | other
25:19 S EqualityOperator -> typeof schema !== "object" | no test kills it | other
34:3 S CallExpression -> ; | no test kills it | other
44:7 S ConditionalExpression -> true | no test kills it | other
46:5 S CallExpression -> ; | no test kills it | other
51:3 S CallExpression -> ; | no test kills it | other
52:25 S ConditionalExpression -> true | no test kills it | cluster 20
52:25 S EqualityOperator -> typeof expandedBranch !== "object" | no test kills it | cluster 20
52:61 S BlockStatement -> {} | no test kills it | cluster 20
54:5 S CallExpression -> ; | no test kills it | cluster 20
55:5 S CallExpression -> ; | no test kills it | cluster 20
61:7 NC ConditionalExpression -> false | no test kills it | cluster 20
61:18 NC BooleanLiteral -> false | no test kills it | cluster 20
61:31 NC BooleanLiteral -> false | no test kills it | cluster 20
62:7 NC ConditionalExpression -> false | no test kills it | cluster 20
62:7 NC EqualityOperator -> schema !== false | no test kills it | cluster 20
62:18 NC BooleanLiteral -> true | no test kills it | cluster 20
62:38 NC ConditionalExpression -> false | no test kills it | cluster 20
62:38 NC EqualityOperator -> typeof schema === "object" | no test kills it | cluster 20
62:73 NC BooleanLiteral -> true | no test kills it | cluster 20
63:10 NC ConditionalExpression -> true | no test kills it | cluster 20
63:10 NC ConditionalExpression -> false | no test kills it | cluster 20
63:10 NC EqualityOperator -> getCachedValidator(schema)(value) !== true | no test kills it | cluster 20
63:48 NC BooleanLiteral -> false | no test kills it | cluster 20
70:61 S BlockStatement -> {} | no test kills it | other
73:42 NC BlockStatement -> {} | no test kills it | other
74:9 NC BlockStatement -> {} | no test kills it | other
75:7 NC CallExpression -> ; | no test kills it | other
80:42 S BlockStatement -> {} | no test kills it | other
81:18 S EqualityOperator -> typeof node === "object" | no test kills it | other
82:9 S ConditionalExpression -> true | no test kills it | other
82:35 NC BlockStatement -> {} | no test kills it | other
83:7 NC CallExpression -> ; | no test kills it | other
84:7 NC CallExpression -> ; | no test kills it | other
86:46 S CallExpression -> ; | no test kills it | other
88:3 S CallExpression -> ; | no test kills it | other
89:66 NC CallExpression -> ; | no test kills it | other
90:3 S CallExpression -> ; | no test kills it | other
```

### frontmatter/stemIndex.ts (41)

```text
31:10 S ConditionalExpression -> true | no test kills it | other
31:10 S ConditionalExpression -> false | no test kills it | other
31:10 S EqualityOperator -> relative !== "" | no test kills it | other
31:23 S StringLiteral -> "Stryker was here!" | no test kills it | string
31:30 S LogicalOperator -> !relative.startsWith("..") || !path.isAbsolute(relative) | no test kills it | other
31:31 S MethodExpression -> relative.endsWith("..") | no test kills it | other
42:10 S EqualityOperator -> first <= second | no test kills it | other
42:32 S EqualityOperator -> first >= second | no test kills it | other
42:32 S ConditionalExpression -> false | no test kills it | other
42:32 S ConditionalExpression -> true | no test kills it | other
42:32 S EqualityOperator -> first <= second | no test kills it | other
67:75 S EqualityOperator -> limit >= 0 | no test kills it | other
67:75 S ConditionalExpression -> true | no test kills it | other
68:12 S MethodExpression -> [...this.candidatesByStem.keys()] | no test kills it | other
78:75 S EqualityOperator -> limit >= 0 | no test kills it | other
96:19 S BooleanLiteral -> true | no test kills it | other
101:13 S ConditionalExpression -> false | no test kills it | other
102:13 S ConditionalExpression -> false | no test kills it | other
102:50 NC BlockStatement -> {} | no test kills it | other
103:21 NC BooleanLiteral -> false | no test kills it | other
106:13 S ConditionalExpression -> true | no test kills it | other
111:5 S CallExpression -> ; | no test kills it | other
141:11 S ConditionalExpression -> false | no test kills it | cluster 16
141:11 S LogicalOperator -> (!entry.isFile() && !entry.isSymbolicLink() || path.extname(entry.name | no test kills it | cluster 16
141:11 S LogicalOperator -> !entry.isFile() && !entry.isSymbolicLink() && path.extname(entry.name) | no test kills it | cluster 16
141:12 S ConditionalExpression -> false | no test kills it | cluster 16
141:31 NC BooleanLiteral -> entry.isSymbolicLink() | no test kills it | cluster 16
142:12 S ConditionalExpression -> false | no test kills it | cluster 16
143:12 S ConditionalExpression -> false | no test kills it | cluster 16
161:10 S ArrayDeclaration -> [] | no test kills it | cluster 17
161:10 S MethodExpression -> [...new Set(roots.map(canonicalRoot))] | no test kills it | cluster 17
161:61 S StringLiteral -> "" | no test kills it | cluster 17
165:10 S ArrayDeclaration -> [] | no test kills it | cluster 17
165:10 S MethodExpression -> [...new Set(roots.map(canonicalRoot))] | no test kills it | cluster 17
165:70 S BlockStatement -> {} | no test kills it | cluster 17
166:9 S BlockStatement -> {} | no test kills it | cluster 17
168:14 S StringLiteral -> `` | no test kills it | cluster 17
169:13 NC BlockStatement -> {} | no test kills it | cluster 17
170:14 NC StringLiteral -> `` | no test kills it | cluster 17
172:11 S StringLiteral -> "" | no test kills it | cluster 17
193:9 S ConditionalExpression -> true | no test kills it | cluster 17
```

### mapping/imageReference.ts (11)

```text
10:33 S ArrayDeclaration -> [] | no test kills it | data
10:34 S StringLiteral -> "" | no test kills it | data
10:41 S StringLiteral -> "" | no test kills it | data
10:48 S StringLiteral -> "" | no test kills it | data
10:56 S StringLiteral -> "" | no test kills it | data
10:63 S StringLiteral -> "" | no test kills it | data
10:71 S StringLiteral -> "" | no test kills it | data
25:19 S ConditionalExpression -> true | no test kills it | cluster 24
25:19 S LogicalOperator -> document.includes("\\") && image.includes("\\") | no test kills it | cluster 24
25:37 S StringLiteral -> "" | no test kills it | cluster 24
25:61 S StringLiteral -> "" | no test kills it | cluster 24
```

### mapping/labelRename.ts (17)

```text
40:7 S ConditionalExpression -> false | no test kills it | cluster 11
40:7 S ConditionalExpression -> false | no test kills it | cluster 11
40:7 S LogicalOperator -> (!Number.isSafeInteger(line) || line < 1) && !isValidLabelName(oldName | no test kills it | cluster 11
40:7 S LogicalOperator -> !Number.isSafeInteger(line) && line < 1 | no test kills it | cluster 11
40:38 S ConditionalExpression -> false | no test kills it | cluster 11
46:9 S ConditionalExpression -> false | no test kills it | cluster 11
46:18 S UnaryOperator -> +1 | no test kills it | cluster 11
51:7 S ConditionalExpression -> false | no test kills it | cluster 11
51:7 S ConditionalExpression -> true | no test kills it | cluster 11
51:7 S EqualityOperator -> end >= start | no test kills it | cluster 11
51:7 S EqualityOperator -> end <= start | no test kills it | cluster 11
51:27 S ArithmeticOperator -> end + 1 | no test kills it | cluster 11
51:40 S StringLiteral -> "" | no test kills it | cluster 11
51:46 S AssignmentOperator -> end += 1 | no test kills it | cluster 11
54:36 S MethodExpression -> content.trimEnd() | no test kills it | cluster 11
55:37 S MethodExpression -> content.trimStart() | no test kills it | cluster 11
61:7 S ConditionalExpression -> false | no test kills it | cluster 11
```

### mapping/pastedImage.ts (22)

```text
12:8 S StringLiteral -> "" | only another layer: session/pasteImageWrite.test.js | data
12:21 S StringLiteral -> "" | no test kills it | data
12:33 S StringLiteral -> "" | no test kills it | data
12:46 S StringLiteral -> "" | no test kills it | data
16:87 S StringLiteral -> "" | no test kills it | data
16:100 S StringLiteral -> "" | no test kills it | data
19:39 S ArithmeticOperator -> 10 / 1024 | only another layer: session/paletteReq.requirements.test.js | cluster 2
19:39 S ArithmeticOperator -> 10 * 1024 / 1024 | only another layer: session/paletteReq.requirements.test.js | cluster 2
29:5 S ConditionalExpression -> true | no test kills it | cluster 3
29:5 S EqualityOperator -> bytes.length > offset + signature.length | no test kills it | cluster 3
29:21 S ArithmeticOperator -> offset - signature.length | no test kills it | cluster 3
33:18 S ArrayDeclaration -> [] | no test kills it | cluster 3
41:5 NC ConditionalExpression -> case "image/jpeg": | no test kills it | cluster 4
41:10 S StringLiteral -> "" | no test kills it | cluster 4
42:5 NC ConditionalExpression -> case "image/gif": | no test kills it | cluster 4
42:10 S StringLiteral -> "" | no test kills it | cluster 4
43:5 NC ConditionalExpression -> case "image/webp": | no test kills it | cluster 4
43:10 S StringLiteral -> "" | no test kills it | cluster 4
44:5 S ConditionalExpression -> default: | no test kills it | cluster 4
50:10 S Regex -> /[A-Za-z0-9+/]*={0,2}$/u | no test kills it | cluster 4
50:10 S Regex -> /^[A-Za-z0-9+/]*={0,2}/u | no test kills it | cluster 4
60:23 S EqualityOperator -> index < MAX_SUFFIX | no test kills it | other
```

### mapping/sourceMapping.ts (11)

```text
35:5 S ConditionalExpression -> false | no test kills it | cluster 12
35:5 S ConditionalExpression -> false | no test kills it | cluster 12
35:5 S LogicalOperator -> (!Number.isSafeInteger(startLine) || !Number.isSafeInteger(endLine)) & | no test kills it | cluster 12
35:5 S LogicalOperator -> !Number.isSafeInteger(startLine) && !Number.isSafeInteger(endLine) | no test kills it | cluster 12
37:8 S EqualityOperator -> startLine <= 1 | only another layer: host/previewTiming.test.js | cluster 12
37:8 S ConditionalExpression -> false | no test kills it | cluster 12
44:9 S ConditionalExpression -> true | no test kills it | cluster 12
78:13 S Regex -> /[1-9]\d*$/u | no test kills it | regex
78:13 S Regex -> /^[1-9]\d*/u | no test kills it | regex
85:67 S StringLiteral -> `` | no test kills it | string
85:83 S ArithmeticOperator -> domOrder - 1 | no test kills it | other
```

### mapping/textDiff.ts (76)

```text
8:10 S ConditionalExpression -> true | no test kills it | cluster 13
8:10 S ConditionalExpression -> true | no test kills it | cluster 13
8:10 S LogicalOperator -> code >= 0xd800 || code <= 0xdbff | no test kills it | cluster 13
8:10 S EqualityOperator -> code > 0xd800 | no test kills it | cluster 13
8:28 S EqualityOperator -> code < 0xdbff | no test kills it | cluster 13
8:28 S ConditionalExpression -> true | no test kills it | cluster 13
12:10 S ConditionalExpression -> true | no test kills it | cluster 13
12:10 S ConditionalExpression -> true | no test kills it | cluster 13
12:10 S LogicalOperator -> code >= 0xdc00 || code <= 0xdfff | no test kills it | cluster 13
12:10 S EqualityOperator -> code > 0xdc00 | no test kills it | cluster 13
12:28 S ConditionalExpression -> true | no test kills it | cluster 13
12:28 S EqualityOperator -> code < 0xdfff | no test kills it | cluster 13
23:10 S ConditionalExpression -> true | no test kills it | cluster 13
25:10 S EqualityOperator -> prefix >= 0 | no test kills it | cluster 13
25:10 S ConditionalExpression -> true | no test kills it | cluster 13
26:5 S LogicalOperator -> (before[prefix - 1] === "\r" && before[prefix] === "\n" || after[prefi | no test kills it | cluster 13
26:5 S LogicalOperator -> (before[prefix - 1] === "\r" && before[prefix] === "\n" || after[prefi | no test kills it | cluster 13
26:5 S ConditionalExpression -> false | no test kills it | cluster 13
26:5 S ConditionalExpression -> false | no test kills it | cluster 13
26:5 S LogicalOperator -> before[prefix - 1] === "\r" && before[prefix] === "\n" && after[prefix | no test kills it | cluster 13
26:6 S ConditionalExpression -> true | no test kills it | cluster 13
26:6 S ConditionalExpression -> false | no test kills it | cluster 13
26:6 S LogicalOperator -> before[prefix - 1] === "\r" || before[prefix] === "\n" | no test kills it | cluster 13
26:6 S EqualityOperator -> before[prefix - 1] !== "\r" | no test kills it | cluster 13
26:13 S ArithmeticOperator -> prefix + 1 | no test kills it | cluster 13
26:29 S StringLiteral -> "" | no test kills it | cluster 13
26:37 S ConditionalExpression -> true | no test kills it | cluster 13
26:37 S EqualityOperator -> before[prefix] !== "\n" | no test kills it | cluster 13
26:56 S StringLiteral -> "" | no test kills it | cluster 13
27:9 S ConditionalExpression -> false | no test kills it | cluster 13
27:15 S ArithmeticOperator -> prefix + 1 | no test kills it | cluster 13
27:31 S StringLiteral -> "" | no test kills it | cluster 13
27:39 NC ConditionalExpression -> true | no test kills it | cluster 13
27:39 NC EqualityOperator -> after[prefix] !== "\n" | no test kills it | cluster 13
27:57 NC StringLiteral -> "" | no test kills it | cluster 13
28:9 S LogicalOperator -> isHighSurrogate(before.charCodeAt(prefix - 1)) || isLowSurrogate(befor | no test kills it | cluster 13
28:9 S ConditionalExpression -> false | no test kills it | cluster 13
28:43 S ArithmeticOperator -> prefix + 1 | no test kills it | cluster 13
29:9 S ConditionalExpression -> false | no test kills it | cluster 13
29:9 S LogicalOperator -> isHighSurrogate(after.charCodeAt(prefix - 1)) || isLowSurrogate(after. | no test kills it | cluster 13
29:42 S ArithmeticOperator -> prefix + 1 | no test kills it | cluster 13
41:10 S ConditionalExpression -> false | no test kills it | cluster 14
41:10 S EqualityOperator -> suffix >= 0 | no test kills it | cluster 14
41:10 S EqualityOperator -> suffix <= 0 | no test kills it | cluster 14
42:28 S ArithmeticOperator -> before.length + suffix | no test kills it | cluster 14
43:27 S ArithmeticOperator -> after.length + suffix | no test kills it | cluster 14
45:7 S ConditionalExpression -> false | no test kills it | cluster 14
45:7 S LogicalOperator -> (before[beforeBoundary - 1] === "\r" && before[beforeBoundary] === "\n | no test kills it | cluster 14
45:7 S ConditionalExpression -> false | no test kills it | cluster 14
45:7 S LogicalOperator -> (before[beforeBoundary - 1] === "\r" && before[beforeBoundary] === "\n | no test kills it | cluster 14
45:7 S ConditionalExpression -> false | no test kills it | cluster 14
45:7 S LogicalOperator -> before[beforeBoundary - 1] === "\r" && before[beforeBoundary] === "\n" | no test kills it | cluster 14
45:8 S ConditionalExpression -> false | no test kills it | cluster 14
45:8 S LogicalOperator -> before[beforeBoundary - 1] === "\r" || before[beforeBoundary] === "\n" | no test kills it | cluster 14
45:8 S ConditionalExpression -> true | no test kills it | cluster 14
45:8 S EqualityOperator -> before[beforeBoundary - 1] !== "\r" | no test kills it | cluster 14
45:15 S ArithmeticOperator -> beforeBoundary + 1 | no test kills it | cluster 14
45:39 S StringLiteral -> "" | no test kills it | cluster 14
45:47 S ConditionalExpression -> true | no test kills it | cluster 14
45:47 S EqualityOperator -> before[beforeBoundary] !== "\n" | no test kills it | cluster 14
45:74 S StringLiteral -> "" | no test kills it | cluster 14
46:11 S ConditionalExpression -> false | no test kills it | cluster 14
46:11 S LogicalOperator -> after[afterBoundary - 1] === "\r" || after[afterBoundary] === "\n" | no test kills it | cluster 14
46:11 S ConditionalExpression -> true | no test kills it | cluster 14
46:11 S EqualityOperator -> after[afterBoundary - 1] !== "\r" | no test kills it | cluster 14
46:17 S ArithmeticOperator -> afterBoundary + 1 | no test kills it | cluster 14
46:40 S StringLiteral -> "" | no test kills it | cluster 14
46:48 S ConditionalExpression -> true | no test kills it | cluster 14
46:48 S EqualityOperator -> after[afterBoundary] !== "\n" | no test kills it | cluster 14
46:73 S StringLiteral -> "" | no test kills it | cluster 14
47:11 S ConditionalExpression -> false | no test kills it | cluster 14
47:11 S LogicalOperator -> isHighSurrogate(before.charCodeAt(beforeBoundary - 1)) || isLowSurroga | no test kills it | cluster 14
47:45 S ArithmeticOperator -> beforeBoundary + 1 | no test kills it | cluster 14
48:11 S LogicalOperator -> isHighSurrogate(after.charCodeAt(afterBoundary - 1)) || isLowSurrogate | no test kills it | cluster 14
48:11 S ConditionalExpression -> false | no test kills it | cluster 14
48:44 S ArithmeticOperator -> afterBoundary + 1 | no test kills it | cluster 14
```

### myst/confLocator.ts (16)

```text
11:52 S StringLiteral -> "" | no test kills it | data
11:70 S StringLiteral -> "" | no test kills it | data
37:11 S BlockStatement -> {} | no test kills it | catch
44:10 S ConditionalExpression -> false | no test kills it | other
44:23 S StringLiteral -> "Stryker was here!" | no test kills it | string
88:32 S ConditionalExpression -> false | no test kills it | other
101:19 S EqualityOperator -> now() - cached.checkedAt <= CONF_RECHECK_MS | no test kills it | cluster 10
106:7 NC CallExpression -> ; | no test kills it | cluster 10
109:19 S ConditionalExpression -> true | no test kills it | cluster 10
109:54 S ConditionalExpression -> true | no test kills it | cluster 10
117:28 NC ArrayDeclaration -> ["Stryker was here"] | no test kills it | cluster 10
117:48 NC ArrayDeclaration -> ["Stryker was here"] | no test kills it | cluster 10
117:61 NC BooleanLiteral -> true | no test kills it | cluster 10
132:13 S MethodExpression -> conf.extensions.every(name => name === "myst_parser" || name === "myst | no test kills it | other
132:70 S ConditionalExpression -> false | no test kills it | other
132:79 S StringLiteral -> "" | no test kills it | string
```

### navigation/openingPolicy.ts (1)

```text
36:56 S EqualityOperator -> group.lastActive >= best.lastActive | no test kills it | cluster 23
```

### navigation/previewNavigation.ts (70)

```text
35:7 S ConditionalExpression -> false | no test kills it | other
35:7 S LogicalOperator -> !suffix.includes("#") && !fragment | no test kills it | other
35:24 S StringLiteral -> "" | no test kills it | string
39:22 S Regex -> /^L([1-9]\d*)(?:-L([1-9]\d*))?/u | no test kills it | cluster 6
39:22 S Regex -> /L([1-9]\d*)(?:-L([1-9]\d*))?$/u | no test kills it | cluster 6
39:22 S Regex -> /^L([1-9]\d*)(?:-L([1-9]\d))?$/u | no test kills it | cluster 6
43:12 S ConditionalExpression -> true | no test kills it | cluster 6
43:36 S EqualityOperator -> endLine < lines.length | no test kills it | cluster 6
47:41 S StringLiteral -> "" | no test kills it | string
48:35 S MethodExpression -> value.trim().toUpperCase() | no test kills it | other
48:35 S MethodExpression -> value | no test kills it | other
48:70 S Regex -> /[^\p{L}\P{N}_\s-]/gu | no test kills it | regex
48:93 S StringLiteral -> "Stryker was here!" | no test kills it | string
48:105 S Regex -> /\s/gu | no test kills it | regex
51:24 S ConditionalExpression -> false | no test kills it | other
53:9 S LogicalOperator -> wasInFence && fence !== undefined | no test kills it | other
53:23 S ConditionalExpression -> false | no test kills it | other
55:20 S Regex -> /^ {0,3}\(([A-Za-z0-9_.:-]+)\)=\s*/u | no test kills it | cluster 7
55:20 S Regex -> / {0,3}\(([A-Za-z0-9_.:-]+)\)=\s*$/u | no test kills it | cluster 7
55:20 S Regex -> /^ {0,3}\(([A-Za-z0-9_.:-]+)\)=\S*$/u | no test kills it | cluster 7
58:21 S Regex -> /(?:^|\s)\^([^\s]+)\s*/u | no test kills it | cluster 7
58:21 S Regex -> /(?:\s)\^([^\s]+)\s*$/u | no test kills it | cluster 7
58:21 S Regex -> /(?:^|\s)\^([^\s]+)\S*$/u | no test kills it | cluster 7
62:20 S Regex -> /<h[^1-6]\b[^>]*\bid=["']([^"']+)["'][^>]*>/iu | no test kills it | cluster 7
62:20 S Regex -> /<h[1-6]\b[^>]\bid=["']([^"']+)["'][^>]*>/iu | no test kills it | cluster 7
62:20 S Regex -> /<h[1-6]\b[>]*\bid=["']([^"']+)["'][^>]*>/iu | no test kills it | cluster 7
62:20 S Regex -> /<h[1-6]\b[^>]*\bid=["']([^"'])["'][^>]*>/iu | no test kills it | cluster 7
62:20 S Regex -> /<h[1-6]\b[^>]*\bid=["'](["']+)["'][^>]*>/iu | no test kills it | cluster 7
62:20 S Regex -> /<h[1-6]\b[^>]*\bid=[^"']([^"']+)["'][^>]*>/iu | no test kills it | cluster 7
62:20 S Regex -> /<h[1-6]\b[^>]*\bid=["']([^"']+)[^"'][^>]*>/iu | no test kills it | cluster 7
62:20 S Regex -> /<h[1-6]\b[^>]*\bid=["']([^"']+)["'][^>]>/iu | no test kills it | cluster 7
62:20 S Regex -> /<h[1-6]\b[^>]*\bid=["']([^"']+)["'][>]*>/iu | no test kills it | cluster 7
63:9 S LogicalOperator -> htmlId || htmlId === target | no test kills it | cluster 7
63:9 S ConditionalExpression -> false | no test kills it | cluster 7
63:19 NC ConditionalExpression -> true | no test kills it | cluster 7
63:19 NC EqualityOperator -> htmlId !== target | no test kills it | cluster 7
63:38 NC BlockStatement -> {} | no test kills it | cluster 7
64:27 NC ArithmeticOperator -> index - 1 | no test kills it | cluster 7
64:47 NC ArithmeticOperator -> index - 1 | no test kills it | cluster 7
66:17 S Regex -> / {0,3}#{1,6}\s+(.+?)\s*#*\s*$/u | no test kills it | cluster 7
66:17 S Regex -> /^ {0,3}#{1,6}\s(.+?)\s*#*\s*$/u | no test kills it | cluster 7
66:17 S Regex -> /^ {0,3}#{1,6}\S+(.+?)\s*#*\s*$/u | no test kills it | cluster 7
68:11 S Regex -> / {0,3}(?:=+|-+)\s*$/u | no test kills it | cluster 7
68:11 S Regex -> /^ {0,3}(?:=+|-+)\s*/u | no test kills it | cluster 7
68:11 S Regex -> /^ {0,3}(?:=|-+)\s*$/u | no test kills it | cluster 7
68:11 S Regex -> /^ {0,3}(?:=+|-+)\S*$/u | no test kills it | cluster 7
68:60 S StringLiteral -> "Stryker was here!" | no test kills it | cluster 7
68:66 S MethodExpression -> lines[index] | no test kills it | cluster 7
69:39 S Regex -> /\s\{#([^}\s]+)\}\s*$/u | no test kills it | cluster 7
69:39 S Regex -> /\s*\{#([^}\s]+)\}\s*/u | no test kills it | cluster 7
69:39 S Regex -> /\S*\{#([^}\s]+)\}\s*$/u | no test kills it | cluster 7
69:39 S Regex -> /\s*\{#([^}\s]+)\}\S*$/u | no test kills it | cluster 7
70:42 S Regex -> /\s*\{#[^}\s]+\}\s*/u | no test kills it | cluster 7
70:42 S Regex -> /\S*\{#[^}\s]+\}\s*$/u | no test kills it | cluster 7
70:42 S Regex -> /\s\{#[^}\s]+\}\s*$/u | no test kills it | cluster 7
70:42 S Regex -> /\s*\{#[^}\s]+\}\S*$/u | no test kills it | cluster 7
90:28 S MethodExpression -> marker | no test kills it | other
91:30 S MethodExpression -> identity | no test kills it | other
92:7 S ConditionalExpression -> false | no test kills it | other
92:7 S LogicalOperator -> !normalizedMarker && !normalizedIdentity | no test kills it | other
99:10 S EqualityOperator -> index <= 0 | no test kills it | other
117:19 S MethodExpression -> request | no test kills it | cluster 5
121:36 S StringLiteral -> "" | no test kills it | cluster 5
123:7 S LogicalOperator -> trimmed.startsWith("?") || resourcePathPart(trimmed) === "" | no test kills it | cluster 5
123:26 S StringLiteral -> "" | no test kills it | cluster 5
123:34 S ConditionalExpression -> true | no test kills it | cluster 5
136:12 S LogicalOperator -> !wiki || rawScheme !== undefined | no test kills it | cluster 5
138:36 S StringLiteral -> "" | only another layer: session/toolbarReq.requirements.test.js | cluster 5
141:39 S StringLiteral -> "" | no test kills it | cluster 5
158:11 S BlockStatement -> {} | no test kills it | catch
```

### palette/emoji.ts (52)

```text
26:55 S ArrayDeclaration -> [] | only another layer: page/modules/editActions.test.js | data
27:4 S StringLiteral -> "" | no test kills it | data
27:26 S StringLiteral -> "" | no test kills it | data
28:7 S StringLiteral -> "" | no test kills it | data
29:7 S StringLiteral -> "" | no test kills it | data
30:7 S StringLiteral -> "" | no test kills it | data
31:7 S StringLiteral -> "" | no test kills it | data
32:7 S StringLiteral -> "" | no test kills it | data
33:7 S StringLiteral -> "" | no test kills it | data
34:7 S StringLiteral -> "" | only another layer: page/modules/editActions.test.js | data
35:4 S StringLiteral -> "" | no test kills it | data
35:14 S StringLiteral -> "" | no test kills it | data
35:34 S StringLiteral -> "" | only another layer: page/modules/editPalette.test.js | data
36:7 S StringLiteral -> "" | no test kills it | data
37:7 S StringLiteral -> "" | no test kills it | data
38:7 S StringLiteral -> "" | no test kills it | data
39:7 S StringLiteral -> "" | no test kills it | data
40:7 S StringLiteral -> "" | no test kills it | data
41:7 S StringLiteral -> "" | only another layer: page/modules/editActions.test.js | data
42:4 S StringLiteral -> "" | no test kills it | data
42:14 S StringLiteral -> "" | no test kills it | data
42:24 S StringLiteral -> "" | no test kills it | data
44:7 S StringLiteral -> "" | no test kills it | data
45:7 S StringLiteral -> "" | no test kills it | data
46:7 S StringLiteral -> "" | only another layer: page/modules/editActions.test.js | data
47:4 S StringLiteral -> "" | no test kills it | data
47:12 S StringLiteral -> "" | no test kills it | data
47:30 S StringLiteral -> "" | no test kills it | data
48:7 S StringLiteral -> "" | no test kills it | data
49:7 S StringLiteral -> "" | no test kills it | data
50:7 S StringLiteral -> "" | only another layer: page/modules/editActions.test.js | data
51:4 S StringLiteral -> "" | no test kills it | data
51:15 S StringLiteral -> "" | no test kills it | data
51:26 S StringLiteral -> "" | no test kills it | data
52:7 S StringLiteral -> "" | no test kills it | data
53:7 S StringLiteral -> "" | no test kills it | data
54:7 S StringLiteral -> "" | no test kills it | data
55:7 S StringLiteral -> "" | no test kills it | data
56:7 S StringLiteral -> "" | only another layer: page/modules/editActions.test.js | data
57:4 S StringLiteral -> "" | no test kills it | data
57:15 S StringLiteral -> "" | no test kills it | data
57:37 S StringLiteral -> "" | only another layer: page/modules/editPalette.test.js | data
58:7 S StringLiteral -> "" | only another layer: page/modules/editPalette.test.js | data
59:7 S StringLiteral -> "" | no test kills it | data
60:7 S StringLiteral -> "" | no test kills it | data
61:7 S StringLiteral -> "" | no test kills it | data
62:7 S StringLiteral -> "" | only another layer: page/modules/editActions.test.js | data
69:21 S StringLiteral -> "" | only another layer: page/modules/editActions.test.js | data
70:33 S StringLiteral -> "" | only another layer: page/modules/editActions.test.js | data
71:20 S MethodExpression -> entry | only another layer: page/modules/editActions.test.js | other
71:49 S MethodExpression -> entry | only another layer: page/modules/editActions.test.js | other
71:61 S ArithmeticOperator -> space - 1 | only another layer: page/modules/editActions.test.js | other
```

### palette/paletteIcons.ts (6)

```text
11:3 S StringLiteral -> "" | only another layer: page/modules/slashMenu.test.js | data
11:87 S StringLiteral -> "" | no test kills it | data
14:3 S StringLiteral -> "" | only another layer: page/modules/slashMenu.test.js | data
14:75 S StringLiteral -> "" | no test kills it | data
15:12 S StringLiteral -> "" | no test kills it | data
18:3 S StringLiteral -> "" | no test kills it | data
```

### paste/htmlToMarkdown.ts (346)

```text
13:45 S StringLiteral -> "" | no test kills it | data
13:53 S StringLiteral -> "" | no test kills it | data
13:70 S StringLiteral -> "" | no test kills it | data
13:78 S StringLiteral -> "" | no test kills it | data
13:90 S StringLiteral -> "" | no test kills it | data
14:3 S StringLiteral -> "" | no test kills it | data
14:13 S StringLiteral -> "" | no test kills it | data
14:23 S StringLiteral -> "" | no test kills it | data
14:32 S StringLiteral -> "" | no test kills it | data
14:39 S StringLiteral -> "" | no test kills it | data
14:47 S StringLiteral -> "" | no test kills it | data
14:57 S StringLiteral -> "" | no test kills it | data
14:67 S StringLiteral -> "" | no test kills it | data
14:79 S StringLiteral -> "" | no test kills it | data
14:89 S StringLiteral -> "" | no test kills it | data
14:98 S StringLiteral -> "" | no test kills it | data
15:30 S StringLiteral -> "" | no test kills it | data
15:37 S StringLiteral -> "" | no test kills it | data
15:48 S StringLiteral -> "" | no test kills it | data
15:59 S StringLiteral -> "" | no test kills it | data
15:69 S StringLiteral -> "" | no test kills it | data
15:79 S StringLiteral -> "" | no test kills it | data
15:87 S StringLiteral -> "" | no test kills it | data
15:94 S StringLiteral -> "" | no test kills it | data
16:3 S StringLiteral -> "" | no test kills it | data
16:13 S StringLiteral -> "" | no test kills it | data
16:39 S StringLiteral -> "" | no test kills it | data
16:81 S StringLiteral -> "" | no test kills it | data
16:87 S StringLiteral -> "" | no test kills it | data
16:93 S StringLiteral -> "" | no test kills it | data
17:3 S StringLiteral -> "" | no test kills it | data
17:14 S StringLiteral -> "" | no test kills it | data
17:25 S StringLiteral -> "" | no test kills it | data
17:36 S StringLiteral -> "" | no test kills it | data
17:48 S StringLiteral -> "" | no test kills it | data
17:56 S StringLiteral -> "" | no test kills it | data
17:68 S StringLiteral -> "" | no test kills it | data
17:74 S StringLiteral -> "" | no test kills it | data
17:80 S StringLiteral -> "" | no test kills it | data
17:86 S StringLiteral -> "" | no test kills it | data
18:3 S StringLiteral -> "" | no test kills it | data
18:12 S StringLiteral -> "" | no test kills it | data
18:21 S StringLiteral -> "" | no test kills it | data
18:30 S StringLiteral -> "" | no test kills it | data
18:36 S StringLiteral -> "" | no test kills it | data
19:18 S Regex -> /^(?:https?:|mailto:|tel:|#|\/|\.\.\/|[^:/?#]*(?:[/?#]|$))/iu | no test kills it | regex
19:18 S Regex -> /^(?:https:|mailto:|tel:|#|\/|\.\.?\/|[^:/?#]*(?:[/?#]|$))/iu | no test kills it | regex
19:18 S Regex -> /^(?:https?:|mailto:|tel:|#|\/|\.\.?\/|[^:/?#](?:[/?#]|$))/iu | no test kills it | regex
19:18 S Regex -> /^(?:https?:|mailto:|tel:|#|\/|\.\.?\/|[:/?#]*(?:[/?#]|$))/iu | no test kills it | regex
19:18 S Regex -> /^(?:https?:|mailto:|tel:|#|\/|\.\.?\/|[^:/?#]*(?:[/?#]))/iu | no test kills it | regex
30:55 S Regex -> /\s/gu | no test kills it | regex
35:29 S ArrowFunction -> () => undefined | no test kills it | other
35:40 S ConditionalExpression -> false | no test kills it | other
35:55 S StringLiteral -> "" | no test kills it | string
41:7 S ConditionalExpression -> false | no test kills it | other
41:41 NC BooleanLiteral -> true | no test kills it | other
49:10 S ConditionalExpression -> false | no test kills it | cluster 15
49:10 S ConditionalExpression -> false | no test kills it | cluster 15
49:20 S StringLiteral -> "" | no test kills it | cluster 15
49:30 S ConditionalExpression -> false | no test kills it | cluster 15
49:40 S StringLiteral -> "" | no test kills it | cluster 15
49:53 S EqualityOperator -> Number(value) > 600 | no test kills it | cluster 15
54:10 S LogicalOperator -> /white-space:pre/u.test(css) || /monospace|consolas|menlo|courier/u.te | no test kills it | cluster 15
58:15 S MethodExpression -> value | no test kills it | cluster 15
59:7 S ConditionalExpression -> false | no test kills it | cluster 15
59:7 S ConditionalExpression -> false | no test kills it | cluster 15
59:7 S LogicalOperator -> url === "" && /[\u0000-\u001f]/u.test(url) | no test kills it | cluster 15
59:15 S StringLiteral -> "Stryker was here!" | no test kills it | cluster 15
65:7 S ConditionalExpression -> false | no test kills it | cluster 15
65:35 NC StringLiteral -> "" | no test kills it | cluster 15
65:53 NC Regex -> /[^<>]/gu | no test kills it | cluster 15
65:91 NC Regex -> /\S/gu | no test kills it | cluster 15
65:99 NC StringLiteral -> "" | no test kills it | cluster 15
65:108 NC StringLiteral -> "" | no test kills it | cluster 15
72:14 S Regex -> /([^\p{L}\p{N}])_|_(?=[^\p{L}\p{N}]|$)/gu | no test kills it | regex
72:14 S Regex -> /(^|[\p{L}\p{N}])_|_(?=[^\p{L}\p{N}]|$)/gu | no test kills it | regex
72:14 S Regex -> /(^|[^\p{L}\p{N}])_|_(?![^\p{L}\p{N}]|$)/gu | no test kills it | regex
72:14 S Regex -> /(^|[^\p{L}\P{N}])_|_(?=[^\p{L}\p{N}]|$)/gu | no test kills it | regex
72:14 S Regex -> /(^|[^\P{L}\p{N}])_|_(?=[^\p{L}\p{N}]|$)/gu | no test kills it | regex
72:14 S Regex -> /(^|[^\p{L}\p{N}])_|_(?=[^\p{L}\p{N}])/gu | no test kills it | regex
72:14 S Regex -> /(^|[^\p{L}\p{N}])_|_(?=[\p{L}\p{N}]|$)/gu | no test kills it | regex
72:14 S Regex -> /(^|[^\p{L}\p{N}])_|_(?=[^\P{L}\p{N}]|$)/gu | no test kills it | regex
72:14 S Regex -> /(^|[^\p{L}\p{N}])_|_(?=[^\p{L}\P{N}]|$)/gu | no test kills it | regex
72:84 NC StringLiteral -> "" | no test kills it | string
72:89 NC StringLiteral -> "" | no test kills it | string
73:21 S StringLiteral -> "" | no test kills it | string
78:14 S Regex -> /(\s*)(#{1,6})(\s|$)/u | no test kills it | regex
78:14 S Regex -> /^(\S*)(#{1,6})(\s|$)/u | no test kills it | regex
78:14 S Regex -> /^(\s*)(#)(\s|$)/u | no test kills it | regex
78:14 S Regex -> /^(\s*)(#{1,6})(\s)/u | no test kills it | regex
79:14 S Regex -> /(\s*)([>+-])(\s)/u | no test kills it | regex
79:14 S Regex -> /^(\s)([>+-])(\s)/u | no test kills it | regex
79:14 S Regex -> /^(\S*)([>+-])(\s)/u | no test kills it | regex
79:14 S Regex -> /^(\s*)([>+-])(\S)/u | no test kills it | regex
79:36 S StringLiteral -> "" | no test kills it | string
80:14 S Regex -> /^(\s)(\d+)([.)])(\s)/u | no test kills it | regex
80:14 S Regex -> /^(\S*)(\d+)([.)])(\s)/u | no test kills it | regex
80:14 S Regex -> /^(\s*)(\d+)([^.)])(\s)/u | no test kills it | regex
80:14 S Regex -> /^(\s*)(\D+)([.)])(\s)/u | no test kills it | regex
80:14 S Regex -> /^(\s*)(\d+)([.)])(\S)/u | no test kills it | regex
80:14 S Regex -> /^(\s*)(\d)([.)])(\s)/u | no test kills it | regex
80:40 S StringLiteral -> "" | no test kills it | string
84:27 S Regex -> /`/gu | no test kills it | regex
85:44 NC MethodExpression -> Math.min(max, run.length) | no test kills it | other
87:18 S ConditionalExpression -> false | no test kills it | other
87:18 S Regex -> /`|`$/u | no test kills it | regex
87:18 S LogicalOperator -> /^`|`$/u.test(text) && /^ .* $/u.test(text) && text.trim() !== "" | no test kills it | other
87:18 S Regex -> /^`|`/u | no test kills it | regex
87:42 S ConditionalExpression -> false | no test kills it | other
87:42 S Regex -> /^ .* /u | no test kills it | regex
87:42 S Regex -> / .* $/u | no test kills it | regex
87:42 S Regex -> /^ . $/u | no test kills it | regex
87:66 NC ConditionalExpression -> true | no test kills it | other
87:66 NC EqualityOperator -> text.trim() === "" | no test kills it | other
87:66 NC MethodExpression -> text | no test kills it | other
87:82 NC StringLiteral -> "Stryker was here!" | no test kills it | string
87:88 NC StringLiteral -> "" | no test kills it | string
87:101 NC StringLiteral -> "" | no test kills it | string
97:17 S Regex -> /(\s*)([\s\S]*?)(\s*)$/u | no test kills it | regex
98:17 S ConditionalExpression -> false | no test kills it | other
98:30 S StringLiteral -> "Stryker was here!" | no test kills it | string
102:45 NC BooleanLiteral -> true | no test kills it | other
103:26 S ConditionalExpression -> true | no test kills it | other
104:55 NC Regex -> /\s/gu | no test kills it | regex
104:55 NC Regex -> /\S+/gu | no test kills it | regex
104:64 NC StringLiteral -> "" | no test kills it | string
106:77 NC StringLiteral -> "Stryker was here!" | no test kills it | string
107:7 S ConditionalExpression -> false | no test kills it | other
107:24 S StringLiteral -> "" | no test kills it | string
107:48 NC StringLiteral -> "" | no test kills it | string
107:55 NC StringLiteral -> "" | no test kills it | string
108:86 S StringLiteral -> "Stryker was here!" | no test kills it | string
109:10 S ConditionalExpression -> false | no test kills it | other
109:50 NC StringLiteral -> "" | no test kills it | string
109:67 NC StringLiteral -> "" | no test kills it | string
113:109 S Regex -> /\s/gu | no test kills it | regex
119:5 NC ConditionalExpression -> case "br": | no test kills it | other
119:10 S StringLiteral -> "" | no test kills it | string
120:14 NC StringLiteral -> "" | no test kills it | string
122:10 S StringLiteral -> "" | no test kills it | string
123:10 S StringLiteral -> "" | no test kills it | string
124:10 S StringLiteral -> "" | no test kills it | string
125:41 S BooleanLiteral -> false | no test kills it | other
125:63 S StringLiteral -> "" | no test kills it | string
125:77 S Regex -> /^`\S+`$/u | no test kills it | regex
125:77 S Regex -> /^`\s+`/u | no test kills it | regex
125:77 S Regex -> /`\s+`$/u | no test kills it | regex
125:77 S Regex -> /^`\s`$/u | no test kills it | regex
125:89 S StringLiteral -> "Stryker was here!" | no test kills it | string
128:19 S MethodExpression -> attr(node, "alt").replace(/\s+/gu, " ") | no test kills it | other
128:45 S Regex -> /\s/gu | no test kills it | regex
128:54 S StringLiteral -> "" | no test kills it | string
129:32 S Regex -> /data:/iu | no test kills it | regex
130:31 S ConditionalExpression -> false | no test kills it | other
130:39 S StringLiteral -> "Stryker was here!" | no test kills it | string
130:44 NC StringLiteral -> "" | no test kills it | string
133:14 S ConditionalExpression -> true | no test kills it | other
133:78 S EqualityOperator -> entry.name !== "checked" | no test kills it | other
133:78 S ConditionalExpression -> true | no test kills it | other
133:115 NC StringLiteral -> "" | no test kills it | string
133:125 NC StringLiteral -> "Stryker was here!" | no test kills it | string
138:11 S MethodExpression -> text | no test kills it | other
138:11 S ConditionalExpression -> false | no test kills it | other
138:27 S StringLiteral -> "Stryker was here!" | no test kills it | string
138:38 NC StringLiteral -> "Stryker was here!" | no test kills it | string
139:20 S MethodExpression -> text | no test kills it | other
139:50 S StringLiteral -> "" | no test kills it | string
141:5 S ConditionalExpression -> default: | no test kills it | other
146:16 S ConditionalExpression -> false | no test kills it | other
146:24 S StringLiteral -> "" | no test kills it | string
147:34 S ConditionalExpression -> false | no test kills it | other
147:42 S StringLiteral -> "" | no test kills it | string
147:49 S ConditionalExpression -> false | no test kills it | other
147:57 S StringLiteral -> "" | no test kills it | string
147:67 S ConditionalExpression -> false | no test kills it | other
147:75 S StringLiteral -> "" | no test kills it | string
148:18 S ConditionalExpression -> false | no test kills it | other
148:18 S ConditionalExpression -> false | no test kills it | other
148:18 S ConditionalExpression -> false | no test kills it | other
148:26 S StringLiteral -> "" | no test kills it | string
148:35 S ConditionalExpression -> false | no test kills it | other
148:43 S StringLiteral -> "" | no test kills it | string
148:50 S ConditionalExpression -> false | no test kills it | other
148:58 S StringLiteral -> "" | no test kills it | string
148:70 S Regex -> /text-decoration[^;]line-through/u | no test kills it | regex
156:10 S MethodExpression -> text.replace(/[ \t]*\\\n[ \t]*/gu, "\\\n").replace(/(?:\\\n)+$/u, ""). | no test kills it | other
157:14 S Regex -> /[^ \t]*\\\n[ \t]*/gu | no test kills it | regex
157:14 S Regex -> /[ \t]\\\n[ \t]*/gu | no test kills it | regex
157:14 S Regex -> /[ \t]*\\\n[^ \t]*/gu | no test kills it | regex
157:14 S Regex -> /[ \t]*\\\n[ \t]/gu | no test kills it | regex
157:36 S StringLiteral -> "" | no test kills it | string
158:14 S Regex -> /(?:\\\n)$/u | no test kills it | regex
158:14 S Regex -> /(?:\\\n)+/u | no test kills it | regex
158:29 S StringLiteral -> "Stryker was here!" | no test kills it | string
159:14 S Regex -> /^(?:\\\n)/u | no test kills it | regex
159:14 S Regex -> /(?:\\\n)+/u | no test kills it | regex
159:29 S StringLiteral -> "Stryker was here!" | no test kills it | string
160:21 S StringLiteral -> "" | no test kills it | string
162:14 S Regex -> /(\[[ x]\])\s+/u | no test kills it | regex
163:44 S StringLiteral -> "" | no test kills it | string
167:27 S Regex -> /`/gu | no test kills it | regex
168:56 NC MethodExpression -> Math.min(max, run.length + 1) | no test kills it | other
168:70 NC ArithmeticOperator -> run.length - 1 | no test kills it | other
170:50 S Regex -> /\n$/u | no test kills it | regex
175:17 S MethodExpression -> node.childNodes.every(child => isElement(child) && child.tagName === " | no test kills it | other
175:49 S ConditionalExpression -> true | no test kills it | other
175:69 S ConditionalExpression -> true | no test kills it | other
176:7 S MethodExpression -> node.childNodes | no test kills it | other
176:95 S StringLiteral -> "Stryker was here!" | no test kills it | string
177:25 NC BooleanLiteral -> false | no test kills it | other
177:37 NC StringLiteral -> "" | no test kills it | string
178:47 S StringLiteral -> "" | no test kills it | string
184:19 S Regex -> /(?:^|\S)(?:language|lang|highlight-source|highlight-text)-([\w+#.-]+) | no test kills it | regex
187:10 NC StringLiteral -> "Stryker was here!" | no test kills it | string
191:42 S ConditionalExpression -> false | no test kills it | other
191:51 S StringLiteral -> "Stryker was here!" | no test kills it | string
200:14 S LogicalOperator -> child.tagName === "ul" || child.tagName === "ol" || items.length > 0 | no test kills it | other
200:15 S ConditionalExpression -> true | no test kills it | other
200:41 NC ConditionalExpression -> false | no test kills it | other
200:41 NC EqualityOperator -> child.tagName !== "ol" | no test kills it | other
200:59 NC StringLiteral -> "" | no test kills it | string
200:68 S ConditionalExpression -> true | no test kills it | other
200:68 S EqualityOperator -> items.length >= 0 | no test kills it | other
201:14 NC ConditionalExpression -> true | no test kills it | other
201:14 NC ConditionalExpression -> false | no test kills it | other
201:32 NC StringLiteral -> "" | no test kills it | string
201:40 NC ConditionalExpression -> false | no test kills it | other
201:40 NC EqualityOperator -> child.tagName !== "ol" | no test kills it | other
201:58 NC StringLiteral -> "" | no test kills it | string
212:20 S ConditionalExpression -> true | no test kills it | other
212:94 NC StringLiteral -> "" | no test kills it | string
213:20 S ConditionalExpression -> true | no test kills it | other
213:87 NC ArrayDeclaration -> [] | no test kills it | other
215:48 S Regex -> /(?:-|\d+\.) /u | no test kills it | regex
215:48 S Regex -> /^(?:-|\d\.) /u | no test kills it | regex
217:60 NC StringLiteral -> "" | no test kills it | string
217:77 S StringLiteral -> "Stryker was here!" | no test kills it | string
229:16 S ConditionalExpression -> true | no test kills it | other
229:35 S StringLiteral -> "" | no test kills it | string
237:10 S ConditionalExpression -> false | no test kills it | other
237:30 S LogicalOperator -> node.tagName === "table" && node.childNodes.some(containsTable) | no test kills it | other
237:30 S ConditionalExpression -> false | no test kills it | other
237:47 S StringLiteral -> "" | no test kills it | string
237:58 S MethodExpression -> node.childNodes.every(containsTable) | no test kills it | other
242:7 S ConditionalExpression -> false | no test kills it | other
244:5 S ConditionalExpression -> true | no test kills it | other
244:26 S ConditionalExpression -> true | no test kills it | other
245:39 S EqualityOperator -> row.length >= 0 | no test kills it | other
245:39 S ConditionalExpression -> true | no test kills it | other
245:57 S MethodExpression -> row.some(cell => Number(attr(cell, "colspan") || 1) <= 1 && Number(att | no test kills it | other
246:48 S ConditionalExpression -> true | no test kills it | other
246:55 S ConditionalExpression -> true | no test kills it | other
246:55 S ConditionalExpression -> false | no test kills it | other
246:55 S LogicalOperator -> attr(cell, "rowspan") && 1 | no test kills it | other
246:66 S StringLiteral -> "" | no test kills it | string
247:9 S MethodExpression -> cell.childNodes.every(containsTable) | no test kills it | other
249:74 S StringLiteral -> "Stryker was here!" | no test kills it | string
249:96 S StringLiteral -> "" | no test kills it | string
249:109 S Regex -> /\s/gu | no test kills it | regex
249:118 S StringLiteral -> "" | no test kills it | string
252:12 S MethodExpression -> cells.map(row => row.map(cell => text(cell)).filter(value => value !== | no test kills it | other
252:31 S MethodExpression -> row.map(cell => text(cell)) | no test kills it | other
252:79 S ConditionalExpression -> true | no test kills it | other
252:89 S StringLiteral -> "Stryker was here!" | no test kills it | string
253:25 S ConditionalExpression -> true | no test kills it | other
253:34 S StringLiteral -> "Stryker was here!" | no test kills it | string
268:17 S Regex -> /mso-list:\S*(?!none)[^;]*?level(\d+)/u | no test kills it | regex
268:17 S Regex -> /mso-list:\s*(?!none)[^;]*?level(\d)/u | no test kills it | regex
270:15 S MethodExpression -> element.childNodes.map(child => inline(child, { plain: false })).join( | no test kills it | other
270:72 S BooleanLiteral -> true | no test kills it | other
270:106 S StringLiteral -> "" | no test kills it | string
271:18 S Regex -> /(?:[·•●○▪■§o*-]|\(?\d+[.)]|\(?[a-zA-Z][.)])(?:\s+|$)/u | no test kills it | regex
271:18 S Regex -> /^(?:[·•●○▪■§o*-]|\(\d+[.)]|\(?[a-zA-Z][.)])(?:\s+|$)/u | no test kills it | regex
271:18 S Regex -> /^(?:[·•●○▪■§o*-]|\(?\d[.)]|\(?[a-zA-Z][.)])(?:\s+|$)/u | no test kills it | regex
271:18 S Regex -> /^(?:[·•●○▪■§o*-]|\(?\d+[^.)]|\(?[a-zA-Z][.)])(?:\s+|$)/u | no test kills it | regex
271:18 S Regex -> /^(?:[·•●○▪■§o*-]|\(?\D+[.)]|\(?[a-zA-Z][.)])(?:\s+|$)/u | no test kills it | regex
271:18 S Regex -> /^(?:[·•●○▪■§o*-]|\(?\d+[.)]|\([a-zA-Z][.)])(?:\s+|$)/u | no test kills it | regex
271:18 S Regex -> /^(?:[·•●○▪■§o*-]|\(?\d+[.)]|\(?[^a-zA-Z][.)])(?:\s+|$)/u | no test kills it | regex
271:18 S Regex -> /^(?:[·•●○▪■§o*-]|\(?\d+[.)]|\(?[a-zA-Z][.)])(?:\s+)/u | no test kills it | regex
271:18 S Regex -> /^(?:[·•●○▪■§o*-]|\(?\d+[.)]|\(?[a-zA-Z][^.)])(?:\s+|$)/u | no test kills it | regex
271:18 S Regex -> /^(?:[·•●○▪■§o*-]|\(?\d+[.)]|\(?[a-zA-Z][.)])(?:\s|$)/u | no test kills it | regex
274:14 S ConditionalExpression -> false | no test kills it | other
274:53 S MethodExpression -> marker[0] | no test kills it | other
292:67 NC StringLiteral -> "" | no test kills it | data
296:9 S ConditionalExpression -> false | no test kills it | other
296:29 S LogicalOperator -> SKIPPED.has(node.tagName) && hidden(node) | no test kills it | other
298:11 S ConditionalExpression -> true | no test kills it | other
299:9 S CallExpression -> ; | no test kills it | other
300:38 S BooleanLiteral -> true | no test kills it | other
305:9 S ConditionalExpression -> true | no test kills it | other
308:9 S CallExpression -> ; | no test kills it | other
309:13 S ConditionalExpression -> true | no test kills it | other
309:27 S StringLiteral -> "Stryker was here!" | no test kills it | string
313:5 S CallExpression -> ; | no test kills it | other
316:9 S CallExpression -> ; | no test kills it | other
319:38 S BooleanLiteral -> true | no test kills it | other
324:9 S Regex -> /h[1-6]$/u | no test kills it | regex
324:9 S Regex -> /^h[1-6]/u | no test kills it | regex
325:103 S StringLiteral -> "Stryker was here!" | no test kills it | string
326:28 S StringLiteral -> "" | no test kills it | string
326:41 S Regex -> /\s/gu | no test kills it | regex
326:50 S StringLiteral -> "" | no test kills it | string
327:11 S ConditionalExpression -> true | no test kills it | other
327:20 S StringLiteral -> "Stryker was here!" | no test kills it | string
328:16 S ConditionalExpression -> false | no test kills it | other
328:16 S ConditionalExpression -> false | no test kills it | other
328:16 S ConditionalExpression -> false | no test kills it | other
328:16 S ConditionalExpression -> false | no test kills it | other
328:24 S StringLiteral -> "" | no test kills it | message
328:31 S ConditionalExpression -> false | no test kills it | other
328:39 S StringLiteral -> "" | no test kills it | message
328:52 S ConditionalExpression -> false | no test kills it | other
328:60 S StringLiteral -> "" | no test kills it | message
328:68 S ConditionalExpression -> false | no test kills it | other
328:76 S StringLiteral -> "" | no test kills it | message
328:89 S ConditionalExpression -> false | no test kills it | other
328:97 S StringLiteral -> "" | no test kills it | message
329:11 S MethodExpression -> node.childNodes.every(hasBlock) | no test kills it | other
332:13 S ConditionalExpression -> true | no test kills it | other
332:22 S StringLiteral -> "Stryker was here!" | no test kills it | string
336:11 S ConditionalExpression -> true | no test kills it | other
336:20 S StringLiteral -> "Stryker was here!" | no test kills it | string
339:11 S ConditionalExpression -> true | no test kills it | other
339:21 S StringLiteral -> "Stryker was here!" | no test kills it | string
341:75 S ConditionalExpression -> true | no test kills it | other
341:95 S ConditionalExpression -> true | no test kills it | other
342:52 S Regex -> /\r\n/gu | no test kills it | regex
342:63 S StringLiteral -> "" | no test kills it | string
343:11 S ConditionalExpression -> true | no test kills it | other
343:11 S MethodExpression -> code | no test kills it | other
343:27 S StringLiteral -> "Stryker was here!" | no test kills it | string
349:16 S ConditionalExpression -> true | no test kills it | other
349:16 S EqualityOperator -> tag !== "div" | no test kills it | other
349:24 S StringLiteral -> "" | no test kills it | string
349:57 NC BlockStatement -> {} | no test kills it | other
352:11 NC ConditionalExpression -> true | no test kills it | other
352:11 NC ConditionalExpression -> false | no test kills it | other
352:11 NC EqualityOperator -> code.trim() === "" | no test kills it | other
352:11 NC MethodExpression -> code | no test kills it | other
352:27 NC StringLiteral -> "Stryker was here!" | no test kills it | string
367:32 S ConditionalExpression -> true | no test kills it | other
369:9 S ConditionalExpression -> true | no test kills it | other
369:9 S MethodExpression -> code | no test kills it | other
369:25 S StringLiteral -> "Stryker was here!" | no test kills it | string
371:10 S MethodExpression -> convertBlocks(tree.childNodes).join("\n\n").replace(/\n{3,}/gu, "\n\n" | no test kills it | other
371:74 S StringLiteral -> "" | no test kills it | string
```

### preview/contentPatch.ts (31)

```text
32:27 S StringLiteral -> "" | no test kills it | data
48:44 S ConditionalExpression -> true | no test kills it | other
48:44 S EqualityOperator -> attribute.name !== name | no test kills it | other
53:8 S ConditionalExpression -> true | no test kills it | other
54:39 S ConditionalExpression -> true | no test kills it | other
54:39 S LogicalOperator -> attribute.name === "id" || attribute.value === CONTENT_ID | no test kills it | other
54:39 S ConditionalExpression -> true | no test kills it | other
54:66 S ConditionalExpression -> true | no test kills it | other
58:31 S ConditionalExpression -> true | no test kills it | other
63:31 S ConditionalExpression -> true | no test kills it | other
64:9 S ConditionalExpression -> true | no test kills it | other
64:28 S StringLiteral -> "" | no test kills it | string
86:23 S BooleanLiteral -> false | no test kills it | other
90:57 S ConditionalExpression -> true | no test kills it | other
90:57 S EqualityOperator -> end > start | no test kills it | other
112:38 S StringLiteral -> `` | no test kills it | string
113:37 S StringLiteral -> `` | no test kills it | string
134:19 S ConditionalExpression -> false | no test kills it | other
134:19 S EqualityOperator -> i >= normalizedHtml.length | no test kills it | other
134:19 S EqualityOperator -> i <= normalizedHtml.length | no test kills it | other
134:54 S BlockStatement -> {} | no test kills it | other
146:3 S CallExpression -> ; | no test kills it | other
147:42 S ConditionalExpression -> true | no test kills it | other
148:10 S EqualityOperator -> rememberedShells.size >= MAX_REMEMBERED_SHELLS | no test kills it | other
163:3 S CallExpression -> ; | no test kills it | other
185:10 S EqualityOperator -> inner.length < MAX_PATCH_CONTENT_LENGTH | no test kills it | other
185:10 S ConditionalExpression -> true | no test kills it | other
186:9 S Regex -> /nonce\S*=/iu | no test kills it | regex
217:42 S EqualityOperator -> diagnostic.text.length < MAX_PATCH_DIAGNOSTIC_TEXT | no test kills it | other
218:10 S EqualityOperator -> diagnostic.severity.length < MAX_PATCH_DIAGNOSTIC_SEVERITY | no test kills it | other
255:8 S ConditionalExpression -> true | no test kills it | other
```

### preview/flushWait.ts (7)

```text
19:7 S ConditionalExpression -> false | no test kills it | other
19:20 S BlockStatement -> {} | no test kills it | other
27:18 S EqualityOperator -> Date.now() > deadline | no test kills it | other
42:7 S CallExpression -> ; | no test kills it | other
78:18 S MethodExpression -> reason.replace(/\s+/gu, " ") | no test kills it | other
78:33 S Regex -> /\s/gu | no test kills it | regex
78:62 S Regex -> /\./u | no test kills it | regex
```

### preview/themeTokens.ts (2)

```text
16:39 S StringLiteral -> "" | only another layer: page/chartCsp.test.js | data
100:115 S StringLiteral -> "" | no test kills it | string
```

### preview/updatedRanges.ts (7)

```text
49:32 S ConditionalExpression -> true | no test kills it | cluster 25
49:32 S EqualityOperator -> selections.length >= 0 | no test kills it | cluster 25
51:43 S ArithmeticOperator -> change.startLine + change.text.split("\n").length + 1 | no test kills it | cluster 25
51:80 S StringLiteral -> "" | no test kills it | cluster 25
52:12 S MethodExpression -> selections.every(selection => selection.startLine <= last && selection | no test kills it | cluster 25
52:74 S EqualityOperator -> selection.endLine > first | no test kills it | cluster 25
88:10 S EqualityOperator -> ranges.length >= MAX_UPDATED_RANGES | no test kills it | cluster 25
```

### protocol/hostToPage.ts (42)

```text
388:27 S StringLiteral -> "" | no test kills it | data
388:49 S StringLiteral -> "" | no test kills it | data
388:58 S StringLiteral -> "" | no test kills it | data
388:67 S StringLiteral -> "" | no test kills it | data
388:85 S StringLiteral -> "" | no test kills it | data
389:36 S ArithmeticOperator -> 20 / 1024 | no test kills it | cluster 8
389:36 S ArithmeticOperator -> 20 * 1024 / 1024 | no test kills it | cluster 8
394:9 S LogicalOperator -> !next && typeof next !== "object" | no test kills it | cluster 8
394:18 S ConditionalExpression -> false | no test kills it | cluster 8
398:31 S ConditionalExpression -> false | no test kills it | cluster 8
398:31 S LogicalOperator -> !pin && typeof pin !== "object" | no test kills it | cluster 8
398:39 S ConditionalExpression -> false | no test kills it | cluster 8
400:52 S EqualityOperator -> message.contentHtml.length >= MAX_PATCH_CONTENT_LENGTH | no test kills it | other
402:46 S EqualityOperator -> message.label.length >= 500 | no test kills it | other
403:82 S ConditionalExpression -> false | no test kills it | other
403:82 S EqualityOperator -> message.message.length >= 20000 | no test kills it | other
406:10 S EqualityOperator -> diagnostics.length < MAX_PATCH_DIAGNOSTICS | no test kills it | other
407:39 S ConditionalExpression -> true | no test kills it | other
407:39 S ConditionalExpression -> true | no test kills it | other
407:39 S LogicalOperator -> entry && typeof entry.severity === "string" || entry.severity.length < | no test kills it | other
407:39 S LogicalOperator -> entry || typeof entry.severity === "string" | no test kills it | other
407:48 S ConditionalExpression -> true | no test kills it | other
408:12 S EqualityOperator -> entry.severity.length < 50 | no test kills it | other
408:12 S ConditionalExpression -> true | no test kills it | other
408:77 S EqualityOperator -> entry.text.length < 20000 | no test kills it | other
408:77 S ConditionalExpression -> true | no test kills it | other
409:13 S ConditionalExpression -> true | no test kills it | other
409:13 S ConditionalExpression -> false | no test kills it | other
409:13 S EqualityOperator -> entry.code !== undefined | no test kills it | other
409:42 S ConditionalExpression -> true | no test kills it | other
409:42 S LogicalOperator -> typeof entry.code === "string" || entry.code.length <= 100 | no test kills it | other
409:76 S EqualityOperator -> entry.code.length < 100 | no test kills it | other
409:76 S ConditionalExpression -> true | no test kills it | other
411:31 S ArithmeticOperator -> 20 / 1024 | no test kills it | other
411:31 S ArithmeticOperator -> 20 * 1024 / 1024 | no test kills it | other
415:45 S EqualityOperator -> message.html.length >= MAX_BASELINE_LENGTH | no test kills it | other
417:36 S EqualityOperator -> hunks.length < MAX_BASELINE_HUNKS | no test kills it | other
418:20 S ConditionalExpression -> false | no test kills it | other
420:95 S EqualityOperator -> value as number > 0 | no test kills it | other
421:12 S ConditionalExpression -> true | no test kills it | other
421:64 S EqualityOperator -> end as number > (start as number) - 1 | no test kills it | other
496:21 S ConditionalExpression -> false | no test kills it | other
```

### render/blockTagTitle.ts (5)

```text
27:7 S EqualityOperator -> tag.length < max | no test kills it | other
28:19 S MethodExpression -> tag.startsWith("/>") | no test kills it | other
28:40 NC StringLiteral -> "" | no test kills it | string
29:13 S MethodExpression -> tag.slice(0, Math.max(1, max - closing.length - 1)).trimStart() | no test kills it | other
39:17 S MethodExpression -> (args ?? "").replace(/\s+/gu, " ") | no test kills it | other
```

### render/chartData.ts (19)

```text
29:10 S Regex -> /(?:[a-z][a-z0-9+.-]*:|\/\/)/iu | no test kills it | regex
29:48 S MethodExpression -> url | no test kills it | other
34:7 S ConditionalExpression -> false | only another layer: page/modules/vegaChart.test.js | other
34:8 S MethodExpression -> source | no test kills it | other
37:9 S ConditionalExpression -> false | no test kills it | other
42:142 S StringLiteral -> "" | no test kills it | message
53:9 S ConditionalExpression -> false | no test kills it | other
53:9 S EqualityOperator -> depth >= 64 | no test kills it | other
54:31 S BlockStatement -> {} | no test kills it | other
55:45 S ArithmeticOperator -> depth - 1 | no test kills it | other
62:42 S MethodExpression -> url | no test kills it | other
62:63 S MethodExpression -> url | no test kills it | other
65:20 S ArithmeticOperator -> depth - 1 | no test kills it | other
78:10 S StringLiteral -> "" | no test kills it | string
80:11 S StringLiteral -> "" | no test kills it | data
83:5 NC ConditionalExpression -> case "too-large": | no test kills it | other
83:10 NC StringLiteral -> "" | no test kills it | string
84:14 NC StringLiteral -> `` | no test kills it | string
86:14 NC StringLiteral -> `` | no test kills it | string
```

### render/mystNode.ts (7)

```text
75:12 S ConditionalExpression -> true | no test kills it | other
75:12 S EqualityOperator -> node.data.included !== true | no test kills it | other
75:12 S ConditionalExpression -> false | no test kills it | other
75:35 S BooleanLiteral -> false | no test kills it | other
75:42 NC ObjectLiteral -> {} | no test kills it | other
75:76 NC StringLiteral -> "" | no test kills it | string
125:9 S ConditionalExpression -> true | no test kills it | other
```

### render/radioGroups.ts (11)

```text
26:7 S ConditionalExpression -> false | no test kills it | other
39:29 S EqualityOperator -> line <= to | no test kills it | other
40:9 S Regex -> /^[^\s>]*$/u | no test kills it | regex
40:9 S Regex -> /^[\S>]*$/u | no test kills it | regex
40:51 NC StringLiteral -> "Stryker was here!" | no test kills it | string
59:29 S UnaryOperator -> +1 | no test kills it | other
67:53 S StringLiteral -> `` | no test kills it | string
79:51 S StringLiteral -> "" | no test kills it | data
96:7 S ConditionalExpression -> false | no test kills it | other
96:7 S LogicalOperator -> before.identifier && before.label | no test kills it | other
159:9 S ConditionalExpression -> true | no test kills it | other
```

### scroll/anchorPolicy.ts (68)

```text
79:12 S ConditionalExpression -> true | no test kills it | cluster 21
85:11 S ConditionalExpression -> false | no test kills it | cluster 21
85:11 S LogicalOperator -> (!finite(block.top) || !finite(block.height) || block.height < 0 || !f | no test kills it | cluster 21
85:11 S LogicalOperator -> (!finite(block.top) || !finite(block.height) || block.height < 0) && ! | no test kills it | cluster 21
85:11 S ConditionalExpression -> false | no test kills it | cluster 21
85:11 S LogicalOperator -> (!finite(block.top) || !finite(block.height)) && block.height < 0 | no test kills it | cluster 21
85:11 S ConditionalExpression -> false | no test kills it | cluster 21
85:11 S LogicalOperator -> !finite(block.top) && !finite(block.height) | no test kills it | cluster 21
85:11 S ConditionalExpression -> false | no test kills it | cluster 21
85:58 S ConditionalExpression -> false | no test kills it | cluster 21
85:58 S EqualityOperator -> block.height <= 0 | no test kills it | cluster 21
86:35 S ConditionalExpression -> false | no test kills it | other
86:35 S EqualityOperator -> block.line <= 1 | no test kills it | other
86:51 NC BlockStatement -> {} | no test kills it | other
89:21 S ConditionalExpression -> true | no test kills it | other
89:21 S LogicalOperator -> finite(block.endLine) || block.endLine > block.line | no test kills it | other
89:46 S ConditionalExpression -> true | no test kills it | other
89:46 S EqualityOperator -> block.endLine >= block.line | no test kills it | other
92:19 S ConditionalExpression -> true | no test kills it | other
92:19 S EqualityOperator -> tops.length >= 0 | no test kills it | other
92:39 S ConditionalExpression -> false | no test kills it | other
94:29 S EqualityOperator -> index <= tops.length | no test kills it | other
95:15 S ConditionalExpression -> true | no test kills it | other
100:5 S MethodExpression -> raw | no test kills it | other
100:31 S ArithmeticOperator -> left.y + right.y | no test kills it | other
100:31 S LogicalOperator -> left.y - right.y && left.line - right.line | no test kills it | other
100:51 NC ArithmeticOperator -> left.line + right.line | no test kills it | other
104:11 S ConditionalExpression -> false | no test kills it | other
104:11 S EqualityOperator -> point.y <= last.y | no test kills it | other
104:11 S ConditionalExpression -> false | no test kills it | other
104:11 S LogicalOperator -> point.y < last.y && point.line < last.line | no test kills it | other
104:31 S ConditionalExpression -> false | no test kills it | other
104:31 S EqualityOperator -> point.line <= last.line | no test kills it | other
105:11 S LogicalOperator -> point.y === last.y || point.line === last.line | no test kills it | other
105:11 S ConditionalExpression -> false | no test kills it | other
105:11 S ConditionalExpression -> true | no test kills it | other
105:11 S EqualityOperator -> point.y !== last.y | no test kills it | other
105:33 NC ConditionalExpression -> true | no test kills it | other
105:33 NC EqualityOperator -> point.line !== last.line | no test kills it | other
108:12 S EqualityOperator -> map.length >= 1 | no test kills it | other
108:12 S ConditionalExpression -> true | no test kills it | other
112:9 S ConditionalExpression -> false | no test kills it | other
112:9 S ConditionalExpression -> false | no test kills it | other
112:9 S LogicalOperator -> map.length === 0 && !finite(y) | no test kills it | other
113:9 S ConditionalExpression -> false | no test kills it | other
113:9 S EqualityOperator -> y < map[0].y | no test kills it | other
114:25 S EqualityOperator -> index <= map.length | no test kills it | other
116:11 S EqualityOperator -> y < next.y | no test kills it | other
118:13 S ConditionalExpression -> false | no test kills it | other
122:16 NC ArithmeticOperator -> map.length + 1 | no test kills it | other
126:9 S ConditionalExpression -> false | no test kills it | other
126:9 S LogicalOperator -> map.length === 0 && !finite(line) | no test kills it | other
126:9 S ConditionalExpression -> false | no test kills it | other
127:9 S EqualityOperator -> line < map[0].line | no test kills it | other
127:9 S ConditionalExpression -> false | no test kills it | other
128:25 S EqualityOperator -> index <= map.length | no test kills it | other
130:11 S EqualityOperator -> line < next.line | no test kills it | other
132:13 S ConditionalExpression -> false | no test kills it | other
136:16 NC ArithmeticOperator -> map.length + 1 | no test kills it | other
142:12 S EqualityOperator -> top <= offset | no test kills it | other
147:20 S EqualityOperator -> y <= offset * 2 | no test kills it | other
228:47 S EqualityOperator -> now >= expected.expiresAt | no test kills it | other
232:17 S ArithmeticOperator -> Math.min(expected.fromLine, expected.line) + 1 | no test kills it | other
234:9 S EqualityOperator -> topLine > low | no test kills it | other
234:27 S EqualityOperator -> topLine < high | no test kills it | other
253:24 S MethodExpression -> [...changes] | no test kills it | other
253:59 S ArithmeticOperator -> right.startLine + left.startLine | no test kills it | other
255:9 S ConditionalExpression -> true | no test kills it | other
```

### security/spanColors.ts (6)

```text
52:47 NC StringLiteral -> "Stryker was here!" | no test kills it | string
64:29 NC StringLiteral -> "Stryker was here!" | no test kills it | string
65:17 S MethodExpression -> match[2] ?? "" | no test kills it | other
65:30 NC StringLiteral -> "Stryker was here!" | no test kills it | string
72:16 S MethodExpression -> parts | no test kills it | other
84:41 NC StringLiteral -> "Stryker was here!" | no test kills it | string
```

### state/boundedState.ts (7)

```text
5:43 S StringLiteral -> "" | no test kills it | data
23:44 S EqualityOperator -> capacity <= 1 | no test kills it | other
37:9 S ConditionalExpression -> false | no test kills it | other
37:38 NC BlockStatement -> {} | no test kills it | other
85:35 S ConditionalExpression -> true | no test kills it | other
111:7 S ConditionalExpression -> false | only another layer: session/blockReq.requirements.test.js | other
111:32 S BlockStatement -> {} | only another layer: session/blockReq.requirements.test.js | other
```

### state/headingFold.ts (6)

```text
37:9 S LogicalOperator -> level !== undefined || hidingLevel === undefined | only another layer: page/modules/headingFold.test.js | other
37:9 S ConditionalExpression -> true | no test kills it | other
37:9 S ConditionalExpression -> true | only another layer: page/modules/headingFold.test.js | other
37:32 S ConditionalExpression -> true | only another layer: page/modules/headingFold.test.js | other
67:7 S LogicalOperator -> !value && typeof value !== "object" | no test kills it | other
67:17 S ConditionalExpression -> false | no test kills it | other
```

### state/navigationHistory.ts (3)

```text
25:9 S EqualityOperator -> this.entries.length >= NAVIGATION_HISTORY_CAP | no test kills it | cluster 22
67:12 S ConditionalExpression -> true | no test kills it | cluster 22
71:74 NC BlockStatement -> {} | only another layer: session/toolbarReq.requirements.test.js | other
```

### state/previewTheme.ts (6)

```text
3:47 S StringLiteral -> "" | only another layer: session/diagReq.viewState.requirements.test.js | data
29:7 S ConditionalExpression -> false | no test kills it | other
29:7 S LogicalOperator -> !value && typeof value !== "object" | no test kills it | other
29:17 S ConditionalExpression -> false | no test kills it | other
29:44 NC BlockStatement -> {} | no test kills it | other
30:12 NC BooleanLiteral -> true | no test kills it | other
```

### state/previewViewPreferences.ts (1)

```text
52:26 S ConditionalExpression -> true | no test kills it | other
```

### syntax/markdownSyntax.ts (2)

```text
43:42 S StringLiteral -> "Stryker was here!" | no test kills it | string
44:23 S EqualityOperator -> index <= lines.length | no test kills it | other
```

## 3. Holes not worth a test

Outside the numbered clusters, each category below is left without a test, for the reason on its line.

| category | holes | why not worth a test |
| --- | --- | --- |
| catalogue and data-table literals (emoji list, tag and extension sets, icon markup) | 128 | a test per entry would restate the table; the entries are data, and a wrong entry is caught by the user-facing checks that use them |
| message, title and label texts | 20 | wording of a user-visible text; the project keeps these out of tests unless a requirement fixes the text (the `mdokf-messages` ignorer already excludes the clearest ones) |
| other string constants (separators, keys, fallbacks) | 137 | mostly joined into expressions the tests already read; a few matter and sit inside the numbered clusters instead |
| empty `catch` blocks after a file-system error | 3 | the fallback after an unreadable file depends on the platform and the disk; a unit test would mock the file system to prove a no-op |
| regular-expression anchor, quantifier and class variants | 112 | each variant needs a hand-built malformed input; the parsers are covered on typical and rejected inputs, and the variants outside the clusters guard shapes no rule of the SwRS names |
| other conditions and operators outside the numbered clusters | 472 | single guards of already-validated input, or redundant with a second guard in the same function; to be re-read after round 3 if the score of the file stays low |

The 'other' category is the largest and the least certain: it is a residue, not a verdict. Round 3 should not spend tests on it before the clusters below are done.

## 4. Test-worthy holes, in the order round 3 should take them

25 clusters. Each is one function or block where a few tests would kill the whole group; the representative mutant is the first no-coverage or boundary one. Security and data-safety clusters come first, then parsing boundaries, then state caps. 'SwRS to tag' is read from the existing tests of the file, to be confirmed against `requirements/` before tagging with `@tests_req`.

| # | file:line | mutator | replacement | what a test should pin | holes | SwRS to tag |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | frontmatter/fileLinks.ts:201 | BooleanLiteral (NC) | `isWithin(root, candidate)` | link containment: the root and real-path checks that keep a link inside the workspace (the no-coverage mutants switch the check off) | 47 (17 NC) | SwRS-MDOKFSTUDIO-FMSCHEMA-046, SwRS-MDOKFSTUDIO-FMSCHEMA-067 |
| 2 | mapping/pastedImage.ts:19 | ArithmeticOperator | `10 / 1024` | the 10 MiB pasted-image size cap | 2 | SwRS-MDOKFSTUDIO-PALETTE-196 |
| 3 | mapping/pastedImage.ts:29 | EqualityOperator | `bytes.length > offset + signature.length` | image signature sniffing (PNG, JPEG, GIF, WebP header bytes and offsets) | 4 | SwRS-MDOKFSTUDIO-PALETTE-196 |
| 4 | mapping/pastedImage.ts:41 | ConditionalExpression (NC) | `case "image/jpeg":` | MIME to image kind mapping and the base64 validity check | 9 (3 NC) | SwRS-MDOKFSTUDIO-PALETTE-196 |
| 5 | navigation/previewNavigation.ts:123 | LogicalOperator | `trimmed.startsWith("?") \|\| resourcePathPart(trimme` | which link requests are blocked (scheme, absolute target, empty anchor) | 8 | SwRS-MDOKFSTUDIO-TOOLBAR-090, SwRS-MDOKFSTUDIO-TOOLBAR-102 |
| 6 | navigation/previewNavigation.ts:43 | EqualityOperator | `endLine < lines.length` | line-range anchors `#L3-L5` (end bound against the document length) | 5 | SwRS-MDOKFSTUDIO-TOOLBAR-090, SwRS-MDOKFSTUDIO-TOOLBAR-102 |
| 7 | navigation/previewNavigation.ts:63 | EqualityOperator (NC) | `htmlId !== target` | label, block id, HTML id and heading anchors (regular expression anchors and quantifiers) | 39 (5 NC) | SwRS-MDOKFSTUDIO-TOOLBAR-090, SwRS-MDOKFSTUDIO-TOOLBAR-102 |
| 8 | protocol/hostToPage.ts:389 | ArithmeticOperator | `20 / 1024` | the 20 MiB patch-content cap and the pin / next object guards of the host message validator | 7 | SwRS-MDOKFSTUDIO-TRUST-059, SwRS-MDOKFSTUDIO-BLOCK-003 |
| 9 | comments/commentModel.ts:147 | EqualityOperator | `text.length >= MAX_SIDECAR_BYTES` | sidecar size, context length and line-range bounds (`>` against `>=`) | 18 | SwRS-MDOKFSTUDIO-REVIEW-004, SwRS-MDOKFSTUDIO-REVIEW-001 |
| 10 | myst/confLocator.ts:106 | CallExpression (NC) | `;` | conf.py cache: recheck interval, mtime and size invalidation, unreadable file fallback | 7 (4 NC) | SwRS-MDOKFSTUDIO-MYST-066 |
| 11 | mapping/labelRename.ts:51 | AssignmentOperator | `end += 1` | label rename guards (line below 1, invalid names) and the CRLF end-of-line trimming | 17 | SwRS-MDOKFSTUDIO-MYST-038, SwRS-MDOKFSTUDIO-MYST-045 |
| 12 | mapping/sourceMapping.ts:37 | EqualityOperator | `startLine <= 1` | source line validation (start line below 1, non-integer) and line-ending detection | 7 | none on its tests: find it in requirements/ |
| 13 | mapping/textDiff.ts:27 | EqualityOperator (NC) | `after[prefix] !== "\n"` | common prefix: CRLF pair and surrogate pair are never split | 41 (3 NC) | SwRS-MDOKFSTUDIO-BLOCK-042 |
| 14 | mapping/textDiff.ts:41 | EqualityOperator | `suffix >= 0` | common suffix: CRLF pair and surrogate pair are never split | 35 | SwRS-MDOKFSTUDIO-BLOCK-042 |
| 15 | paste/htmlToMarkdown.ts:65 | Regex (NC) | `/[^<>]/gu` | font weight 600 bold threshold, code-block detection, links with spaces or angle brackets | 18 (5 NC) | SwRS-MDOKFSTUDIO-PALETTE-217, SwRS-MDOKFSTUDIO-PALETTE-229 |
| 16 | frontmatter/stemIndex.ts:141 | BooleanLiteral (NC) | `entry.isSymbolicLink()` | which directory entries are indexed (symbolic links, non-Markdown files, stem mismatch) | 7 (1 NC) | SwRS-MDOKFSTUDIO-FMSCHEMA-055 |
| 17 | frontmatter/stemIndex.ts:170 | StringLiteral (NC) | ```` | index cache key and invalidation by root | 12 (2 NC) | SwRS-MDOKFSTUDIO-FMSCHEMA-055 |
| 18 | comments/inlineThread.ts:135 | EqualityOperator | `text.length >= MAX_THREAD_REPLY_LENGTH` | reply length cap (`>` against `>=`) | 2 | SwRS-MDOKFSTUDIO-REVIEW-167, SwRS-MDOKFSTUDIO-REVIEW-186 |
| 19 | frontmatter/sameData.ts:43 | CallExpression (NC) | `;` | structural equality of YAML data: Set and Map keys, byte arrays, type tags | 87 (10 NC) | none on its tests: find it in requirements/ |
| 20 | frontmatter/schemaValidator.ts:62 | EqualityOperator (NC) | `schema !== false` | boolean schemas `true` and `false` and the object guard (no-coverage mutants) | 18 (13 NC) | none on its tests: find it in requirements/ |
| 21 | scroll/anchorPolicy.ts:85 | EqualityOperator | `block.height <= 0` | scroll anchor block validation (finite top and height, negative height) | 11 | SwRS-MDOKFSTUDIO-LIFE-119, SwRS-MDOKFSTUDIO-LIFE-100 |
| 22 | state/navigationHistory.ts:25 | EqualityOperator | `this.entries.length >= NAVIGATION_HISTORY_CAP` | history cap and the can-go-forward bound | 2 | SwRS-MDOKFSTUDIO-TOOLBAR-059 |
| 23 | navigation/openingPolicy.ts:36 | EqualityOperator | `group.lastActive >= best.lastActive` | most recently active tab on a tie (`>` against `>=`) | 1 | SwRS-MDOKFSTUDIO-LIFE-184, SwRS-MDOKFSTUDIO-LIFE-183 |
| 24 | mapping/imageReference.ts:25 | LogicalOperator | `document.includes("\\") && image.includes("\\")` | Windows path detection of an image reference | 4 | SwRS-MDOKFSTUDIO-PALETTE-192 |
| 25 | preview/updatedRanges.ts:49 | EqualityOperator | `selections.length >= 0` | updated-range selection overlap and the range cap (`>` against `>=`) | 7 | SwRS-MDOKFSTUDIO-LIFE-094 |

Cluster order is the order of the table (1 first). Sizes add up to 415 holes, 32% of the holes listed.
