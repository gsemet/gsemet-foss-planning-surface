import sys
sys.path.insert(0, sys.argv[1])
from merge import *

R = "REVIEW-"

# 069 -> 054
merge(R + "054", R + "069",
      title="The host writes comment changes one after another within the file limits and drops a malformed create message",
      suffix="; a create message is dropped without an answer unless its anchor has integer lines with 1 <= line <= endLine, a quote of at most 500 characters and a prefix and suffix of at most 32 characters, and its body has 1 to 10 000 characters.",
      rename={"Valid message": "Valid create message", "Invalid messages": "Invalid create messages", "Accepted limits": "Accepted limits of a create message"})

# 070, 071 -> 074
merge(R + "074", R + "070",
      title="Reply, resolve, reopen and delete change the named thread only, and a malformed message changes nothing",
      suffix="; a reply, resolve or delete message is dropped without an answer unless it has a non-empty thread id, a reply has a body of 1 to 10 000 characters and a resolve has a boolean resolved flag.",
      rename={"Valid reply": "Valid reply message", "Invalid reply": "Invalid reply message", "Accepted limits": "Accepted limits of a reply message"})
merge(R + "074", R + "071",
      rename={"Valid messages": "Valid resolve and delete messages", "Invalid messages": "Invalid resolve and delete messages"})

# 101 -> 100
merge(R + "100", R + "101",
      title="A thread follows its quote in the plain text, narrowed by its context, or is orphaned and keeps its lines",
      suffix=", and, when the quote cannot be found and its old lines do not resemble it, mark the thread as orphaned and keep its stored lines and comments")

# 216 -> SwRS 017
merge(R + "017", R + "216",
      title="The quote of a thread is highlighted once in its block, also over a line break of the source",
      suffix="; a run of whitespace of the text node, such as the line break of a paragraph or list item wrapped over several lines of the source, matches a space of the quote, and the matched text is highlighted as one highlight.",
      rename={"Boundary: ": "Boundary: "})

# 156 -> 152
merge(R + "152", R + "156",
      title="The showComments setting and the Comments button hide and show every review mark, and a message of another render changes nothing",
      suffix="; a previewShowComments message that names another document, revision or request than the page's does not change the show-comments state.",
      rename={"Current message": "Current show-comments message", "Stale message": "Stale show-comments message"})

# 178 -> 186, 192
merge(R + "186", R + "178",
      title="The host appends a valid reply inside the thread comment under the author",
      suffix="; a previewThreadReply message is dropped unless it has an edit id, integer lines with 1 <= line <= endLine and a text of 1 to 10 000 characters that is not blank.",
      scen="""### Scenario (nominal): Valid reply message

- GIVEN a previewThreadReply message with an edit id, lines 5 and 8 and the text ok
- WHEN the message is validated
- THEN it is accepted

### Scenario (refusal): Invalid reply message

| Input | Outcome |
| --- | --- |
| A missing edit id | dropped |
| Line 0 | dropped |
| An end line before the line | dropped |
| A blank text in a previewThreadReply | dropped |
| A text of 10 001 characters in a previewThreadReply | dropped |
""")
merge(R + "192", R + "178",
      title="Deleting an inline thread removes whole lines, and a malformed delete message changes nothing",
      suffix="; a previewThreadDelete message is dropped unless it has an edit id and integer lines with 1 <= line <= endLine.",
      scen="""### Scenario (nominal): Valid delete message

- GIVEN a previewThreadDelete message with an edit id and lines 5 and 8
- WHEN the message is validated
- THEN it is accepted

### Scenario (refusal): Invalid delete message

| Input | Outcome |
| --- | --- |
| A missing edit id | dropped |
| Line 0 | dropped |
| An end line before the line | dropped |
""")

# 007 -> 006, 009
merge(R + "006", R + "007",
      title="The host posts the baseline rendering while the side-by-side diff is on and takes only a well-formed switch message",
      suffix="; the switch message previewSideBySideChanged is accepted only with a boolean on field for the current render, and any other is dropped.",
      scen="""### Scenario (nominal): A well-formed switch message

| Input | Outcome |
| --- | --- |
| previewSideBySideChanged with on true or false for the current render | accepted |

### Scenario (refusal): Dropped switch messages

| Input | Outcome |
| --- | --- |
| previewSideBySideChanged with a non-boolean or no on | dropped |
| A switch message of a stale render | dropped |
""")
merge(R + "009", R + "007",
      title="A changed block shows as a side-by-side diff, and a malformed baseline message is dropped",
      suffix="; the baseline message previewBaselineDiff is accepted only with an html string of at most 20 MiB and at most 100 000 hunks of non-negative integer lines whose ends are not more than one before their starts, for the current render, and any other is dropped.",
      scen="""### Scenario (nominal): A well-formed baseline message

| Input | Outcome |
| --- | --- |
| previewBaselineDiff with an html string and hunks of non-negative integers whose ends are at least one before their starts | accepted for the current render |

### Scenario (refusal): Dropped baseline messages

| Input | Outcome |
| --- | --- |
| previewBaselineDiff with a non-string html, no hunks, a negative or fractional line, an end more than one before its start, or a null hunk | dropped |
| An html of more than 20 MiB, or more than 100 000 hunks | dropped |
| A baseline message of a stale render | dropped |
""")

# 005, 010 -> 009
merge(R + "009", R + "005",
      title="A changed block shows as a side-by-side diff with its word marks, and a malformed baseline message is dropped",
      suffix="; the removed and added words are the character ranges found by comparing the block at the last commit with the current block word by word, consecutive changed words merged into one range, all words of both texts being marked when the comparison would exceed 4 000 000 word pairs.",
      rename={"Changed words": "Changed words of a card", "Size limit": "Word diff size limit"})
merge(R + "009", R + "010",
      title="A changed block shows as a side-by-side diff with its word marks, cut by line hunks, and a malformed baseline message is dropped",
      suffix="; the changed blocks are found from line hunks that give the last-commit lines and the current lines as 1-based inclusive ranges, with an empty side for lines only added or only removed, merged with the hunk next to them when only blank lines separate them, ignoring differences of line endings, and reported as one hunk when more than 20 000 lines differ or more than 2000 edits are needed.",
      rename={"Size limits and block mapping": "Hunk size limits and block mapping"})

# 200, 203 -> 195
merge(R + "195", R + "200",
      title="The host posts the lines that differ from the last commit, read from Git for small files",
      suffix="; it reports the added and modified lines of the shown text as 1-based ranges, merging adjacent lines and keeping separate edits as separate ranges, reports no range for a difference of line endings, of a missing final newline or of deleted lines only, and reports the whole differing middle as one range when more than 20 000 lines differ or more than 2000 edits are needed.",
      rename={"Size limits": "Range size limits"})
merge(R + "195", R + "203",
      suffix="; it reads the text at HEAD through the built-in Git extension without starting a process, returns nothing when Git cannot give it or when the shown text, the document or the HEAD text is not a file under 1 MiB, and announces a change of the Git state only when the HEAD commit id has changed.")

# 208 -> 207
merge(R + "207", R + "208",
      title="Changed blocks get a thin change bar that moves nothing, and malformed ranges are ignored",
      suffix="; a range that is not a pair of integers with 1 <= start <= end is ignored, as is a range list that is not a list.")

# FMEDIT-054 -> FMEDIT-016
merge("FMEDIT-016", "FMEDIT-054",
      title="The host refuses a value that breaks YAML, the field type or the schema, and ignores a malformed save message",
      suffix="; a previewFrontmatterSave message that does not name a non-empty editId and fieldName, or that carries a field outside its accepted shape, is ignored without a reply.")

# FMSCHEMA-060 -> FMSCHEMA-050
merge("FMSCHEMA-050", "FMSCHEMA-060",
      title="Links resolve from the configured or default root and stay inside it",
      suffix="; a non-empty markdownOkfSchemaStudio.frontmatter.bundleRoot or projectRoot replaces the default root, a relative path being taken from the first workspace folder, and markdownOkfSchemaStudio.frontmatter.allowOutsideWorkspaceLinks decides whether a document-relative link may leave every workspace folder.")

refs_fix({"REVIEW-069": "REVIEW-054", "REVIEW-070": "REVIEW-074", "REVIEW-071": "REVIEW-074",
          "REVIEW-101": "REVIEW-100", "REVIEW-216": "REVIEW-017", "REVIEW-156": "REVIEW-152",
          "REVIEW-178": "REVIEW-186", "REVIEW-007": "REVIEW-006", "REVIEW-005": "REVIEW-009",
          "REVIEW-010": "REVIEW-009", "REVIEW-200": "REVIEW-195", "REVIEW-203": "REVIEW-195",
          "REVIEW-208": "REVIEW-207", "FMEDIT-054": "FMEDIT-016", "FMSCHEMA-060": "FMSCHEMA-050"})
