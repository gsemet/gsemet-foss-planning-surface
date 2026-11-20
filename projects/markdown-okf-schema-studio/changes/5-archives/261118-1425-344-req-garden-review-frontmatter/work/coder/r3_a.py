import sys; sys.path.insert(0, sys.argv[0].rsplit("/",1)[0])
from r3_mark import *
f="test/core/frontmatter/okfFrontmatter.test.ts"
text,crlf=read(f)
ids="FMEDIT-004 FMEDIT-029 FMEDIT-037 FMEDIT-043 FMSCHEMA-001 FMSCHEMA-019 FMSCHEMA-023 FMSCHEMA-029 FMSCHEMA-039 FMSCHEMA-046 FMSCHEMA-050 FMSCHEMA-055 FMSCHEMA-084 FMSCHEMA-005".split()
blk="".join(f"// @tests_req {P}{i}\n" for i in ids)+"\n"
assert blk in text
write(f,text.replace(blk,""),crlf)
T=lambda s:'test("'+s
add(f,{
 'test("extractFrontmatter detects and parses':["FMSCHEMA-001"],
 'test("fieldIconType maps':["FMSCHEMA-029"],
 'test("frontmatter field patches preserve':["FMEDIT-043"],
 'test("frontmatter scalar and object edits':["FMEDIT-043"],
 'test("frontmatter array edits keep':["FMEDIT-043"],
 'test("frontmatter key renames preserve':["FMEDIT-043"],
 'test("frontmatter field removal preserves':["FMEDIT-029","FMEDIT-043"],
 'test("extractFrontmatter rejects a document':["FMSCHEMA-001"],
 'test("extractFrontmatter reports invalid YAML':["FMSCHEMA-001"],
 'test("findSchemaDirectory walks':["FMSCHEMA-019"],
 'test("findSchemaDirectory still finds':["FMSCHEMA-019"],
 'test("matchSchemaFile matches':["FMSCHEMA-019"],
 'test("resolveSchemaRefs inlines':["FMSCHEMA-023"],
 'test("effectiveProperties collapses':["FMSCHEMA-029"],
 'test("analyzeFrontmatter yields schema-ordered':["FMSCHEMA-029"],
 'test("analyzeFrontmatter surfaces an info':["FMSCHEMA-005"],
 'test("reduced mode explains':["FMSCHEMA-019"],
 'test("unmatched OKF-like SKILL':["FMSCHEMA-005"],
 'test("analyzeFrontmatter validates enums':["FMSCHEMA-084"],
 'test("analyzeFrontmatter inspects annotated':["FMSCHEMA-046","FMSCHEMA-084"],
 'test("analyzeFrontmatter attaches nested link':["FMSCHEMA-084"],
 'test("file-link union applicability honors':["FMSCHEMA-046","FMSCHEMA-050"],
 'test("file-link union applicability preserves':["FMSCHEMA-046"],
 'test("filename-stem links recheck symlink':["FMSCHEMA-055"],
 'test("filename-stem links report W15':["FMSCHEMA-055"],
 'test("strict mode warns':["FMSCHEMA-084"],
 'test("missing required fields are exposed':["FMSCHEMA-039"],
 'test("json5 and json schema formats':["FMSCHEMA-023"],
 'test("value patch rewrites only':["FMEDIT-043"],
 'test("value patch for an anchored':["FMEDIT-043"],
 'test("value patch for a nested map':["FMEDIT-043"],
 'test("appending a sequence item keeps':["FMEDIT-043"],
 'test("value patch with an unchanged':["FMEDIT-043"],
 'test("value patch fills an empty':["FMEDIT-043"],
 'test("a multi-line value on a plain field':["FMEDIT-004"],
 'test("frontmatter field removal keeps the comment':["FMEDIT-029"],
 'test("frontmatter add with afterField':["FMEDIT-037"],
 'test("T25: additionalPropertiesAllowed':["FMSCHEMA-084"],
 'test("T41: a schema field goes between':["FMEDIT-037"],
 'test("T41: a schema field skips':["FMEDIT-037"],
 'test("T41: a custom key goes after':["FMEDIT-037"],
 'test("T41: beforeField inserts above the named':["FMEDIT-037"],
 'test("T41: plain scalar safety':["FMEDIT-037"],
 'test("T41: plainScalar writes':["FMEDIT-037"],
 'test("T41: without plainScalar':["FMEDIT-037"],
 'test("T41: plainScalar quotes':["FMEDIT-037"],
 'test("T41: beforeField on the first key':["FMEDIT-037"],
 'test("frontmatter patches stay minimal':["FMEDIT-043"],
})
