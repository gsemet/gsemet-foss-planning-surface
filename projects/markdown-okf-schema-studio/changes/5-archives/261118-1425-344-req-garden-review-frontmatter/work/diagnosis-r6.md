# Diagnosis r6: stepSchemaProblem times out (heavy CI run 44305385374 at 6322956)

## Cause
The test's expectation is wrong; the extension is behaving as designed (a known issue).
`stepSchemaProblem` (test/integration/previewEditing.test.ts:1064-1085) writes `type: [\n` into
`_schema/finding.schema.yaml` and waits for the html to match `/Schema could not be parsed/`.
For a `.yaml` schema, `parseSchemaFile` (src/core/frontmatter/okfFrontmatter.ts, ~line 175-181) runs
`parseDocument(raw).toJS()`. The `yaml` library's `parseDocument` does not throw on syntax errors
(they go to `doc.errors`), so nothing reaches the `catch` that builds the "Schema could not be
parsed: ..." warning (okfFrontmatter.ts ~line 413-421). The table keeps rendering and the message
never appears; `waitFor` (10 s) expires.
Only a `.json` / `.json5` schema throws (`JSON.parse`) and yields that warning.

## Proof
- Unit test test/core/frontmatter/diagReq.frontmatter.requirements.test.ts:68-92 states it:
  a broken JSON5 schema gives exactly one `Schema could not be parsed: ` warning; for a YAML schema
  (`type: [a\n`) it asserts the message is absent: "Known issue: a YAML syntax error of the schema is
  not reported as a parse failure."
- The step is the first to use a broken YAML schema and the only place the message is awaited in
  test/integration (grep). It never ran before (earlier heavy runs stopped earlier).
- Not an ordering or editor-state problem: the log shows `stepSchemaOrderAndBadge` (line 1381, runs
  before; stepSchemaProblem is line 1412) passed, since the run reached stepSchemaProblem and the
  stack (previewEditing.test.js:1255) is in it. Its preconditions (typed document, schema found
  assertions at 1068-1070) passed: the failure is at the waitFor at 1076, not at the asserts.
- No literal control byte involved: the regex `/Schema could not be parsed/u` is plain text.
- Not run locally: the stack needs the xvfb heavy job; the proof is by code reading plus the unit test.

## Minimal test-side fix (file test/integration/previewEditing.test.ts, lines 1071-1084)
Break the schema through a JSON5 file that outranks nothing but replaces the YAML one:
`.yaml` is preferred over `.json5` (matchSchemaFile), so move the YAML file aside.
```ts
const schemaPath = path.join(directory, "_schema", "finding.schema.yaml");
const asidePath = `${schemaPath}.aside`;
const json5Path = path.join(directory, "_schema", "finding.schema.json5");
fs.renameSync(schemaPath, asidePath);
fs.writeFileSync(json5Path, "{ type: 'object', properties: ", "utf8");
try { ...unchanged refresh + waitFor "Schema could not be parsed" ... }
finally {
  fs.rmSync(json5Path, { force: true });
  fs.renameSync(asidePath, schemaPath);
  ...unchanged refresh + waitFor "schema found again" ...
}
```
(drop `schemaText` and the two `writeFileSync(schemaPath, ...)` lines). The broken text is the same
as the unit test's, which is known to throw. Residual risk: if the schema directory listing is
cached across the refresh, the new file might not be seen; then the refresh should also be preceded
by the same wait the existing step already uses. Alternative that avoids it: change the claim of the
step (SwRS-FMSCHEMA-023 wording) to the JSON5 case only, which is what the unit test already covers.
