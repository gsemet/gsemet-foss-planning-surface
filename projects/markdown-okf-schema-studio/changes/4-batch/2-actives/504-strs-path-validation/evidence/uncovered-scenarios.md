# CR-504: declared scenarios and paths with no marker

Computed on the worktree at the end of round 6. A SwRS scenario is covered by a `@tests_req <SwRS-ID>#S<n>` line; a StRS path by an `@accepts_req` or `@tests_req <StRS-ID>#S<n>` line. In-force requirements only (not exempt, not deprecated, superseded or archived). SwRS scenarios declared: 2623, with no marker: 722. StRS paths declared: 156, with no marker: 67.

Some entries come from round 3, which drops the fragment of a test that checks no declared scenario instead of guessing one; the others were uncovered before (the first pass gave `S1` when nothing matched, so the later scenarios of a SwRS were never marked). Whether each is a missing test or a scenario worded wider than any test is for the owner or a following CR.

## SwRS scenarios with no marker

| SwRS | Scenario | Title |
|---|---|---|
| SwRS-MDOKFSTUDIO-BLOCK-001 | S4 | Block editor still waiting for its source |
| SwRS-MDOKFSTUDIO-BLOCK-001 | S6 | Nothing to tidy up |
| SwRS-MDOKFSTUDIO-BLOCK-001 | S7 | Edit mode on keeps the reading layout |
| SwRS-MDOKFSTUDIO-BLOCK-001 | S8 | Hover and click do not reflow |
| SwRS-MDOKFSTUDIO-BLOCK-004 | S4 | Keys that belong to other controls |
| SwRS-MDOKFSTUDIO-BLOCK-017 | S3 | Pointer or focus leaves |
| SwRS-MDOKFSTUDIO-BLOCK-026 | S1 | Emphasis and link markup |
| SwRS-MDOKFSTUDIO-BLOCK-026 | S2 | Link label |
| SwRS-MDOKFSTUDIO-BLOCK-026 | S3 | Ambiguous text |
| SwRS-MDOKFSTUDIO-BLOCK-033 | S6 | A click inside the frame stays inside it |
| SwRS-MDOKFSTUDIO-BLOCK-033 | S8 | Cell that cannot be parsed |
| SwRS-MDOKFSTUDIO-BLOCK-033 | S11 | The frame is a one pixel accent frame with monospace text |
| SwRS-MDOKFSTUDIO-BLOCK-033 | S12 | The text box grows with its text |
| SwRS-MDOKFSTUDIO-BLOCK-041 | S5 | A further edit after the refresh |
| SwRS-MDOKFSTUDIO-BLOCK-053 | S3 | The host restores the original text |
| SwRS-MDOKFSTUDIO-BLOCK-058 | S5 | Nothing applied |
| SwRS-MDOKFSTUDIO-BLOCK-058 | S7 | A block that changed under the host |
| SwRS-MDOKFSTUDIO-BLOCK-061 | S4 | Enter continues a quote prefix or the indentation |
| SwRS-MDOKFSTUDIO-BLOCK-061 | S6 | Enter inside a fenced code block |
| SwRS-MDOKFSTUDIO-BLOCK-061 | S7 | The key stays native |
| SwRS-MDOKFSTUDIO-BLOCK-069 | S2 | Marker keys stay native |
| SwRS-MDOKFSTUDIO-BLOCK-069 | S3 | Editor key edits keep the browser undo stack |
| SwRS-MDOKFSTUDIO-BLOCK-069 | S4 | No native editing command |
| SwRS-MDOKFSTUDIO-BLOCK-069 | S7 | Repeated spaces and Enter are typed as they are |
| SwRS-MDOKFSTUDIO-BLOCK-079 | S3 | Caret position decides |
| SwRS-MDOKFSTUDIO-BLOCK-079 | S8 | Page replaced before the save is rendered |
| SwRS-MDOKFSTUDIO-BLOCK-087 | S1 | Three blocks |
| SwRS-MDOKFSTUDIO-BLOCK-087 | S3 | The properties table |
| SwRS-MDOKFSTUDIO-BLOCK-087 | S6 | Other input on the bar |
| SwRS-MDOKFSTUDIO-BLOCK-094 | S6 | Trailing line breaks are dropped |
| SwRS-MDOKFSTUDIO-BLOCK-102 | S4 | The button is hidden while its editor is open |
| SwRS-MDOKFSTUDIO-BLOCK-109 | S1 | Every body bar holds the two arrows |
| SwRS-MDOKFSTUDIO-BLOCK-109 | S6 | A click on an enabled arrow asks the host for the swap |
| SwRS-MDOKFSTUDIO-BLOCK-109 | S10 | A result for the render the page shows |
| SwRS-MDOKFSTUDIO-BLOCK-117 | S1 | Swap |
| SwRS-MDOKFSTUDIO-BLOCK-117 | S2 | The separator is kept as it is |
| SwRS-MDOKFSTUDIO-BLOCK-127 | S9 | The host refuses a paste after the closing fence of an include directive |
| SwRS-MDOKFSTUDIO-BLOCK-130 | S4 | A refused keyboard move can be retried |
| SwRS-MDOKFSTUDIO-BLOCK-140 | S2 | The anchor is the block clicked or opened last |
| SwRS-MDOKFSTUDIO-BLOCK-140 | S3 | Shift+Arrow grows and shrinks the selection |
| SwRS-MDOKFSTUDIO-BLOCK-140 | S5 | Escape or a plain click clears the selection |
| SwRS-MDOKFSTUDIO-BLOCK-140 | S6 | Reading mode |
| SwRS-MDOKFSTUDIO-BLOCK-140 | S7 | Keys that belong to other controls or chords |
| SwRS-MDOKFSTUDIO-BLOCK-148 | S5 | The properties table is never selected |
| SwRS-MDOKFSTUDIO-BLOCK-156 | S4 | The moved selection is selected again at its new place |
| SwRS-MDOKFSTUDIO-BLOCK-156 | S6 | A repeated key moves once and a refusal keeps the selection |
| SwRS-MDOKFSTUDIO-BLOCK-156 | S8 | The host refuses a span that cannot move |
| SwRS-MDOKFSTUDIO-BLOCK-166 | S3 | The page announces the answer |
| SwRS-MDOKFSTUDIO-BLOCK-166 | S5 | The keys stay with the browser |
| SwRS-MDOKFSTUDIO-BLOCK-166 | S6 | A held key sends one request until the host answers |
| SwRS-MDOKFSTUDIO-BLOCK-169 | S2 | Where the cut span sits in the document |
| SwRS-MDOKFSTUDIO-BLOCK-174 | S3 | Padded clipboard |
| SwRS-MDOKFSTUDIO-BLOCK-174 | S6 | Empty clipboard |
| SwRS-MDOKFSTUDIO-BLOCK-191 | S1 | First and later saves |
| SwRS-MDOKFSTUDIO-BLOCK-193 | S1 | Render during editing |
| SwRS-MDOKFSTUDIO-BLOCK-193 | S3 | Work queued twice and a host lock without page editor |
| SwRS-MDOKFSTUDIO-BLOCK-193 | S5 | A content patch closes an open block editor without cancelling |
| SwRS-MDOKFSTUDIO-BLOCK-193 | S9 | A document switch drops the work of the old document |
| SwRS-MDOKFSTUDIO-BLOCK-193 | S10 | A switch while the host still applies an edit |
| SwRS-MDOKFSTUDIO-BLOCK-205 | S4 | Answers and flags of the flush |
| SwRS-MDOKFSTUDIO-BLOCK-205 | S8 | A save refused during a flush warns that the text was not saved |
| SwRS-MDOKFSTUDIO-BLOCK-216 | S1 | Requests that match the document are accepted |
| SwRS-MDOKFSTUDIO-BLOCK-216 | S2 | The host refuses what no longer fits the document |
| SwRS-MDOKFSTUDIO-BLOCK-216 | S7 | Typing again saves again |
| SwRS-MDOKFSTUDIO-BLOCK-228 | S2 | Table and properties saves carry the pin |
| SwRS-MDOKFSTUDIO-BLOCK-228 | S3 | Out of range |
| SwRS-MDOKFSTUDIO-BLOCK-228 | S4 | The host stores the pin |
| SwRS-MDOKFSTUDIO-BLOCK-228 | S7 | Page at the top |
| SwRS-MDOKFSTUDIO-BLOCK-228 | S9 | Close without a shift |
| SwRS-MDOKFSTUDIO-BLOCK-254 | S3 | Walking a list |
| SwRS-MDOKFSTUDIO-BLOCK-255 | S2 | The editor stays open |
| SwRS-MDOKFSTUDIO-BLOCK-259 | S3 | previewEditOpen: An open with a wrong range, insert point or extra field |
| SwRS-MDOKFSTUDIO-BLOCK-259 | S8 | previewBlocksCopy: Invalid lines |
| SwRS-MDOKFSTUDIO-BLOCK-264 | S1 | A paragraph in the middle |
| SwRS-MDOKFSTUDIO-BLOCK-272 | S2 | boundary |
| SwRS-MDOKFSTUDIO-BLOCK-273 | S2 | boundary |
| SwRS-MDOKFSTUDIO-BLOCK-274 | S2 | boundary |
| SwRS-MDOKFSTUDIO-BLOCK-275 | S2 | boundary |
| SwRS-MDOKFSTUDIO-BLOCK-276 | S2 | boundary |
| SwRS-MDOKFSTUDIO-BLOCK-277 | S2 | boundary |
| SwRS-MDOKFSTUDIO-BLOCK-281 | S1 | setting off |
| SwRS-MDOKFSTUDIO-BLOCK-282 | S1 | setting off |
| SwRS-MDOKFSTUDIO-BLOCK-284 | S2 | both edges in one heading |
| SwRS-MDOKFSTUDIO-BLOCK-285 | S1 | setting off |
| SwRS-MDOKFSTUDIO-BLOCK-285 | S2 | both edges inside one element |
| SwRS-MDOKFSTUDIO-BLOCK-286 | S3 | boundary start after the end |
| SwRS-MDOKFSTUDIO-CODE-001 | S6 | A shorter backtick line does not close the fence |
| SwRS-MDOKFSTUDIO-CODE-001 | S8 | Special characters are shown once |
| SwRS-MDOKFSTUDIO-CODE-001 | S9 | An unknown named reference is kept as written |
| SwRS-MDOKFSTUDIO-CODE-007 | S1 | Fenced blocks share one style |
| SwRS-MDOKFSTUDIO-CODE-007 | S2 | A nested block has the same style |
| SwRS-MDOKFSTUDIO-CODE-008 | S2 | The first character decides the mark |
| SwRS-MDOKFSTUDIO-CODE-008 | S5 | Forced-colours mode uses system colours |
| SwRS-MDOKFSTUDIO-CODE-008 | S6 | Outside forced-colours mode the theme colours apply |
| SwRS-MDOKFSTUDIO-CODE-014 | S2 | No file name option, no file name line |
| SwRS-MDOKFSTUDIO-CODE-014 | S4 | A caption without a label has no reference id |
| SwRS-MDOKFSTUDIO-CODE-017 | S4 | The button stays clear of the sticky band and toolbar |
| SwRS-MDOKFSTUDIO-CODE-017 | S7 | The Copied state is reset by another block |
| SwRS-MDOKFSTUDIO-CODE-019 | S2 | A diff block keeps its markers |
| SwRS-MDOKFSTUDIO-CODE-019 | S4 | The button never claims a copy that did not happen |
| SwRS-MDOKFSTUDIO-CODE-019 | S12 | Every handled request is answered |
| SwRS-MDOKFSTUDIO-CODE-019 | S13 | A stale page or a preview with restricted reads |
| SwRS-MDOKFSTUDIO-CODE-039 | S6 | Invalid directive values fall back |
| SwRS-MDOKFSTUDIO-CODE-040 | S2 | Tokens of a supported language are coloured |
| SwRS-MDOKFSTUDIO-CORE-003 | S3 | Map a one-line block and a directive child |
| SwRS-MDOKFSTUDIO-CORE-003 | S4 | Hide leading frontmatter from the body |
| SwRS-MDOKFSTUDIO-CORE-003 | S7 | Map image-only blocks |
| SwRS-MDOKFSTUDIO-CORE-008 | S2 | A narrow image keeps its natural size |
| SwRS-MDOKFSTUDIO-CORE-008 | S3 | Place inline images on the text line |
| SwRS-MDOKFSTUDIO-CORE-008 | S5 | An existing file loads |
| SwRS-MDOKFSTUDIO-CORE-012 | S3 | Keep unsupported include forms as placeholders |
| SwRS-MDOKFSTUDIO-CORE-012 | S5 | Nested includes carry the outer directive line |
| SwRS-MDOKFSTUDIO-CORE-013 | S1 | Stop include depth |
| SwRS-MDOKFSTUDIO-CORE-022 | S6 | Inert styling |
| SwRS-MDOKFSTUDIO-CORE-028 | S1 | Body text |
| SwRS-MDOKFSTUDIO-CORE-034 | S3 | Identifier as wide as the viewport |
| SwRS-MDOKFSTUDIO-CORE-041 | S3 | Author dir attribute |
| SwRS-MDOKFSTUDIO-CORE-050 | S1 | Soft appearance after the first input |
| SwRS-MDOKFSTUDIO-CORE-069 | S2 | Old address |
| SwRS-MDOKFSTUDIO-CORE-070 | S1 | The parse time does not grow with the directives |
| SwRS-MDOKFSTUDIO-CORE-071 | S3 | The allow-list of tags |
| SwRS-MDOKFSTUDIO-CORE-074 | S2 | Refusals |
| SwRS-MDOKFSTUDIO-CORE-075 | S2 | Drift and dirty manifests |
| SwRS-MDOKFSTUDIO-CORE-077 | S3 | Tables that keep their own look |
| SwRS-MDOKFSTUDIO-CORE-082 | S2 | Exempt behaviour |
| SwRS-MDOKFSTUDIO-CORE-083 | S2 | History off |
| SwRS-MDOKFSTUDIO-CORE-085 | S4 | A long rule |
| SwRS-MDOKFSTUDIO-CORE-085 | S7 | No browser |
| SwRS-MDOKFSTUDIO-CORE-088 | S3 | Render a very long document completely |
| SwRS-MDOKFSTUDIO-CORE-093 | S3 | A long ID on a phone |
| SwRS-MDOKFSTUDIO-DIAG-001 | S6 | Picture width against the content column |
| SwRS-MDOKFSTUDIO-DIAG-005 | S4 | Built-in fallbacks |
| SwRS-MDOKFSTUDIO-DIAG-005 | S5 | Edge labels stay readable |
| SwRS-MDOKFSTUDIO-DIAG-009 | S5 | A late picture for a replaced key is not shown |
| SwRS-MDOKFSTUDIO-DIAG-009 | S7 | The JAR pipeline reuses an earlier render |
| SwRS-MDOKFSTUDIO-DIAG-015 | S4 | Changing reason |
| SwRS-MDOKFSTUDIO-DIAG-017 | S2 | Empty document |
| SwRS-MDOKFSTUDIO-DIAG-023 | S1 | Three forms |
| SwRS-MDOKFSTUDIO-DIAG-023 | S2 | Text kept as written |
| SwRS-MDOKFSTUDIO-DIAG-023 | S5 | SVG with a script |
| SwRS-MDOKFSTUDIO-DIAG-024 | S1 | Default and true |
| SwRS-MDOKFSTUDIO-DIAG-024 | S2 | Value that is not the boolean true |
| SwRS-MDOKFSTUDIO-DIAG-032 | S1 | Library include |
| SwRS-MDOKFSTUDIO-DIAG-032 | S5 | Engine failure shows its reason |
| SwRS-MDOKFSTUDIO-DIAG-032 | S6 | Source of 1 MiB |
| SwRS-MDOKFSTUDIO-DIAG-039 | S1 | Patch and switch back |
| SwRS-MDOKFSTUDIO-DIAG-046 | S2 | The from field of the request |
| SwRS-MDOKFSTUDIO-DIAG-046 | S5 | Malformed include requests are ignored |
| SwRS-MDOKFSTUDIO-DIAG-053 | S2 | Outside the folders |
| SwRS-MDOKFSTUDIO-DIAG-053 | S4 | A changed file tells the page |
| SwRS-MDOKFSTUDIO-DIAG-053 | S5 | Editor open |
| SwRS-MDOKFSTUDIO-DIAG-054 | S1 | Includes resolve next to the including file |
| SwRS-MDOKFSTUDIO-DIAG-054 | S3 | Names that are never read |
| SwRS-MDOKFSTUDIO-DIAG-054 | S4 | Reasons by kind of name |
| SwRS-MDOKFSTUDIO-DIAG-054 | S6 | A missing file or a file the rules reject |
| SwRS-MDOKFSTUDIO-DIAG-061 | S1 | Eighth level |
| SwRS-MDOKFSTUDIO-DIAG-061 | S2 | Limits of one diagram |
| SwRS-MDOKFSTUDIO-DIAG-068 | S2 | Options only |
| SwRS-MDOKFSTUDIO-DIAG-068 | S4 | Files that are not read |
| SwRS-MDOKFSTUDIO-DIAG-068 | S5 | Missing file |
| SwRS-MDOKFSTUDIO-DIAG-084 | S4 | Command missing |
| SwRS-MDOKFSTUDIO-DIAG-084 | S5 | Text on standard input, workspace folder as working directory |
| SwRS-MDOKFSTUDIO-DIAG-084 | S6 | The picture is the SVG span of the output |
| SwRS-MDOKFSTUDIO-DIAG-089 | S1 | An existing JAR file is run |
| SwRS-MDOKFSTUDIO-DIAG-089 | S6 | The process fails or returns no picture |
| SwRS-MDOKFSTUDIO-DIAG-097 | S7 | A process that ignores its input becomes a message |
| SwRS-MDOKFSTUDIO-DIAG-105 | S5 | Results reach the page in place or as a full page |
| SwRS-MDOKFSTUDIO-DIAG-129 | S3 | The Mermaid renderer loads the diagram types it needs |
| SwRS-MDOKFSTUDIO-FMEDIT-001 | S1 | A click or a key opens the editor |
| SwRS-MDOKFSTUDIO-FMEDIT-001 | S4 | Link clicks that still follow the link |
| SwRS-MDOKFSTUDIO-FMEDIT-003 | S5 | Schema limits are left to the check at save time |
| SwRS-MDOKFSTUDIO-FMEDIT-003 | S6 | A boolean field toggles with one click |
| SwRS-MDOKFSTUDIO-FMEDIT-003 | S7 | Boolean cells reached by other inputs |
| SwRS-MDOKFSTUDIO-FMEDIT-003 | S8 | Nullable fields offer Set to null |
| SwRS-MDOKFSTUDIO-FMEDIT-003 | S9 | Set to null on lists and on fields that are not nullable |
| SwRS-MDOKFSTUDIO-FMEDIT-004 | S2 | In a multi-line value Enter adds a line and Cmd or Ctrl+Enter saves |
| SwRS-MDOKFSTUDIO-FMEDIT-004 | S3 | Keys that do not save a text value |
| SwRS-MDOKFSTUDIO-FMEDIT-004 | S4 | Trailing line breaks of the typed value |
| SwRS-MDOKFSTUDIO-FMEDIT-004 | S6 | Fields without a schema type are edited as YAML text |
| SwRS-MDOKFSTUDIO-FMEDIT-004 | S7 | A field just added opens an empty box |
| SwRS-MDOKFSTUDIO-FMEDIT-010 | S1 | A list field shows one input per item |
| SwRS-MDOKFSTUDIO-FMEDIT-010 | S4 | Enter and Backspace on empty items |
| SwRS-MDOKFSTUDIO-FMEDIT-010 | S5 | Items reorder by keyboard |
| SwRS-MDOKFSTUDIO-FMEDIT-010 | S6 | Items reorder by drag |
| SwRS-MDOKFSTUDIO-FMEDIT-016 | S2 | An empty or non-text YAML value |
| SwRS-MDOKFSTUDIO-FMEDIT-016 | S4 | Values that are accepted |
| SwRS-MDOKFSTUDIO-FMEDIT-016 | S7 | A save for a missing field or revision is stale |
| SwRS-MDOKFSTUDIO-FMEDIT-016 | S8 | A frontmatter save that names its editor and field is accepted |
| SwRS-MDOKFSTUDIO-FMEDIT-016 | S10 | Accepted bounds of the optional fields |
| SwRS-MDOKFSTUDIO-FMEDIT-019 | S10 | Undo and redo keys act on the field text |
| SwRS-MDOKFSTUDIO-FMEDIT-028 | S4 | Without schema fields to add, a typed name is added |
| SwRS-MDOKFSTUDIO-FMEDIT-028 | S5 | The Add button waits for a name |
| SwRS-MDOKFSTUDIO-FMEDIT-029 | S3 | Removal leaves a valid block |
| SwRS-MDOKFSTUDIO-FMEDIT-029 | S5 | The host refuses to remove a required field |
| SwRS-MDOKFSTUDIO-FMEDIT-037 | S5 | Reload and later renders |
| SwRS-MDOKFSTUDIO-FMEDIT-037 | S6 | A pending editor that cannot be used is dropped |
| SwRS-MDOKFSTUDIO-FMEDIT-037 | S8 | Text that would not read back as the same string |
| SwRS-MDOKFSTUDIO-FMEDIT-043 | S4 | An added list uses the compact sequence style |
| SwRS-MDOKFSTUDIO-FMEDIT-067 | S2 | What the flush sends for each editor |
| SwRS-MDOKFSTUDIO-FMEDIT-067 | S7 | A normal save carries no flush flag |
| SwRS-MDOKFSTUDIO-FMEDIT-067 | S8 | A refused plain save is saved again as a flush before a navigation |
| SwRS-MDOKFSTUDIO-FMEDIT-067 | S9 | Waiting for a plain save |
| SwRS-MDOKFSTUDIO-FMSCHEMA-001 | S1 | Closing with three dashes or three dots |
| SwRS-MDOKFSTUDIO-FMSCHEMA-004 | S1 | Setting off |
| SwRS-MDOKFSTUDIO-FMSCHEMA-004 | S2 | Setting at its default |
| SwRS-MDOKFSTUDIO-FMSCHEMA-006 | S3 | Lean frame |
| SwRS-MDOKFSTUDIO-FMSCHEMA-006 | S4 | Contrast thresholds |
| SwRS-MDOKFSTUDIO-FMSCHEMA-014 | S6 | Old one-key-per-document choices |
| SwRS-MDOKFSTUDIO-FMSCHEMA-014 | S7 | Malformed stored value |
| SwRS-MDOKFSTUDIO-FMSCHEMA-019 | S1 | Nearest folder wins |
| SwRS-MDOKFSTUDIO-FMSCHEMA-019 | S2 | The file is chosen by the type name |
| SwRS-MDOKFSTUDIO-FMSCHEMA-023 | S3 | Other forms of a relative reference |
| SwRS-MDOKFSTUDIO-FMSCHEMA-023 | S4 | Standard JSON pointer fragment |
| SwRS-MDOKFSTUDIO-FMSCHEMA-023 | S9 | Compile failure in a narrow preview |
| SwRS-MDOKFSTUDIO-FMSCHEMA-027 | S2 | Reverted and deleted |
| SwRS-MDOKFSTUDIO-FMSCHEMA-027 | S4 | Document edited afterwards |
| SwRS-MDOKFSTUDIO-FMSCHEMA-029 | S5 | Row tooltip |
| SwRS-MDOKFSTUDIO-FMSCHEMA-029 | S7 | Names equal to object members |
| SwRS-MDOKFSTUDIO-FMSCHEMA-039 | S4 | Info rows only |
| SwRS-MDOKFSTUDIO-FMSCHEMA-043 | S1 | Typing in the frontmatter |
| SwRS-MDOKFSTUDIO-FMSCHEMA-043 | S2 | Page not ready |
| SwRS-MDOKFSTUDIO-FMSCHEMA-046 | S5 | Accepted annotation values |
| SwRS-MDOKFSTUDIO-FMSCHEMA-046 | S7 | Query and fragment |
| SwRS-MDOKFSTUDIO-FMSCHEMA-050 | S1 | Targets that resolve from their root |
| SwRS-MDOKFSTUDIO-FMSCHEMA-050 | S5 | Bundle or project target leaves its root |
| SwRS-MDOKFSTUDIO-FMSCHEMA-050 | S7 | Configured root |
| SwRS-MDOKFSTUDIO-FMSCHEMA-050 | S8 | Configured root that cannot be used |
| SwRS-MDOKFSTUDIO-FMSCHEMA-063 | S4 | Plain labels of the problems |
| SwRS-MDOKFSTUDIO-FMSCHEMA-063 | S5 | First paint |
| SwRS-MDOKFSTUDIO-FMSCHEMA-063 | S8 | Document changed meanwhile |
| SwRS-MDOKFSTUDIO-FMSCHEMA-067 | S5 | No line label |
| SwRS-MDOKFSTUDIO-FMSCHEMA-067 | S7 | Tooltip opens on hover and focus |
| SwRS-MDOKFSTUDIO-FMSCHEMA-073 | S2 | Follow without a marker line |
| SwRS-MDOKFSTUDIO-FMSCHEMA-073 | S3 | Edit mode |
| SwRS-MDOKFSTUDIO-FMSCHEMA-090 | S2 | The state holds while the document stays open |
| SwRS-MDOKFSTUDIO-FMSCHEMA-090 | S3 | Page load and newly opened document |
| SwRS-MDOKFSTUDIO-FMSCHEMA-090 | S4 | Keyboard and the Description column |
| SwRS-MDOKFSTUDIO-FMSCHEMA-091 | S2 | No schema |
| SwRS-MDOKFSTUDIO-GFM-001 | S2 | Trailing punctuation stays outside the link |
| SwRS-MDOKFSTUDIO-GFM-001 | S5 | Autolinks follow the Markdown link policy |
| SwRS-MDOKFSTUDIO-GFM-001 | S6 | The block editor shows the raw URL |
| SwRS-MDOKFSTUDIO-GFM-008 | S2 | Single tildes and code |
| SwRS-MDOKFSTUDIO-GFM-008 | S5 | Aligned column |
| SwRS-MDOKFSTUDIO-GFM-008 | S6 | Unaligned columns |
| SwRS-MDOKFSTUDIO-GFM-016 | S2 | Line and column counting |
| SwRS-MDOKFSTUDIO-GFM-016 | S4 | Markers stay literal where they have another meaning |
| SwRS-MDOKFSTUDIO-GFM-016 | S5 | Defined reference label |
| SwRS-MDOKFSTUDIO-GFM-016 | S6 | The webview keeps checkbox inputs |
| SwRS-MDOKFSTUDIO-GFM-021 | S3 | Uppercase marker rewritten |
| SwRS-MDOKFSTUDIO-GFM-031 | S2 | Span limits |
| SwRS-MDOKFSTUDIO-GFM-031 | S6 | Unknown tag and comment |
| SwRS-MDOKFSTUDIO-GFM-034 | S3 | Diagnostic for removed declarations |
| SwRS-MDOKFSTUDIO-LAYOUT-001 | S3 | GitHub Flavored Markdown gallery |
| SwRS-MDOKFSTUDIO-LAYOUT-002 | S1 | Default cap in a wide pane |
| SwRS-MDOKFSTUDIO-LAYOUT-007 | S1 | Paragraph first in read mode |
| SwRS-MDOKFSTUDIO-LAYOUT-007 | S3 | Edit mode |
| SwRS-MDOKFSTUDIO-LAYOUT-011 | S3 | First-block editor narrowed |
| SwRS-MDOKFSTUDIO-LAYOUT-011 | S6 | Palette bottom edge of the first-block editor |
| SwRS-MDOKFSTUDIO-LAYOUT-011 | S8 | Toolbar bottom edge for the sticky palette |
| SwRS-MDOKFSTUDIO-LAYOUT-020 | S3 | Scrolled document |
| SwRS-MDOKFSTUDIO-LAYOUT-023 | S2 | Column off the pane centre |
| SwRS-MDOKFSTUDIO-LAYOUT-032 | S2 | Sixteen-column table at 900 px |
| SwRS-MDOKFSTUDIO-LAYOUT-032 | S6 | Short identifiers |
| SwRS-MDOKFSTUDIO-LAYOUT-043 | S3 | Measured in document coordinates and for any toolbar state |
| SwRS-MDOKFSTUDIO-LAYOUT-044 | S4 | Tables without a plain grid and other width modes |
| SwRS-MDOKFSTUDIO-LAYOUT-044 | S5 | Table measured uncapped and rounded up |
| SwRS-MDOKFSTUDIO-LAYOUT-044 | S6 | Table with row handles in edit mode |
| SwRS-MDOKFSTUDIO-LAYOUT-044 | S7 | A cell editor keeps the breakout of its table |
| SwRS-MDOKFSTUDIO-LIFE-001 | S3 | Manifest contract |
| SwRS-MDOKFSTUDIO-LIFE-001 | S5 | What VS Code reads |
| SwRS-MDOKFSTUDIO-LIFE-002 | S2 | A task that succeeds or does not exist logs nothing |
| SwRS-MDOKFSTUDIO-LIFE-003 | S1 | Entry points of the command |
| SwRS-MDOKFSTUDIO-LIFE-003 | S5 | Another document |
| SwRS-MDOKFSTUDIO-LIFE-003 | S6 | No eligible file |
| SwRS-MDOKFSTUDIO-LIFE-003 | S12 | Another custom editor active |
| SwRS-MDOKFSTUDIO-LIFE-003 | S13 | Eligible and ineligible files |
| SwRS-MDOKFSTUDIO-LIFE-003 | S14 | File passed by a menu |
| SwRS-MDOKFSTUDIO-LIFE-003 | S16 | A file that cannot be opened |
| SwRS-MDOKFSTUDIO-LIFE-018 | S1 | Declared editor |
| SwRS-MDOKFSTUDIO-LIFE-018 | S2 | The tab shows its own file |
| SwRS-MDOKFSTUDIO-LIFE-018 | S3 | The editor opens before the render ends |
| SwRS-MDOKFSTUDIO-LIFE-018 | S6 | A failure while opening |
| SwRS-MDOKFSTUDIO-LIFE-024 | S4 | Render finished |
| SwRS-MDOKFSTUDIO-LIFE-026 | S2 | Editor changes that leave the preview as it was |
| SwRS-MDOKFSTUDIO-LIFE-026 | S6 | Quick switching between documents |
| SwRS-MDOKFSTUDIO-LIFE-026 | S9 | A hidden preview that becomes visible |
| SwRS-MDOKFSTUDIO-LIFE-032 | S4 | Other document |
| SwRS-MDOKFSTUDIO-LIFE-032 | S6 | Button pressed |
| SwRS-MDOKFSTUDIO-LIFE-038 | S2 | Same document twice |
| SwRS-MDOKFSTUDIO-LIFE-038 | S4 | One restored panel |
| SwRS-MDOKFSTUDIO-LIFE-044 | S5 | Other setting section |
| SwRS-MDOKFSTUDIO-LIFE-049 | S2 | Good render |
| SwRS-MDOKFSTUDIO-LIFE-049 | S6 | Show and hide |
| SwRS-MDOKFSTUDIO-LIFE-049 | S8 | Longest accepted text |
| SwRS-MDOKFSTUDIO-LIFE-059 | S1 | Status with diagnostics |
| SwRS-MDOKFSTUDIO-LIFE-059 | S2 | Pending notice |
| SwRS-MDOKFSTUDIO-LIFE-059 | S3 | Markup in a message |
| SwRS-MDOKFSTUDIO-LIFE-059 | S4 | Quote in a code |
| SwRS-MDOKFSTUDIO-LIFE-062 | S2 | Restored panel |
| SwRS-MDOKFSTUDIO-LIFE-062 | S3 | Reason of each case |
| SwRS-MDOKFSTUDIO-LIFE-069 | S1 | Typing |
| SwRS-MDOKFSTUDIO-LIFE-071 | S2 | Content bounds |
| SwRS-MDOKFSTUDIO-LIFE-071 | S3 | Status line bounds |
| SwRS-MDOKFSTUDIO-LIFE-071 | S4 | Another document, folders or startup setting |
| SwRS-MDOKFSTUDIO-LIFE-071 | S7 | Page created again by VS Code |
| SwRS-MDOKFSTUDIO-LIFE-094 | S1 | Agent edit |
| SwRS-MDOKFSTUDIO-LIFE-094 | S6 | Skip the glow when it would mislead |
| SwRS-MDOKFSTUDIO-LIFE-100 | S1 | Host records the editor's first visible line |
| SwRS-MDOKFSTUDIO-LIFE-100 | S6 | The pane the reader moved owns the anchor |
| SwRS-MDOKFSTUDIO-LIFE-108 | S1 | Scrolling posts the new top line |
| SwRS-MDOKFSTUDIO-LIFE-108 | S4 | Enter or Space on a focused block |
| SwRS-MDOKFSTUDIO-LIFE-108 | S5 | A text diff shows the file |
| SwRS-MDOKFSTUDIO-LIFE-108 | S7 | A report that names another source file |
| SwRS-MDOKFSTUDIO-LIFE-119 | S2 | A line inside a long paragraph |
| SwRS-MDOKFSTUDIO-LIFE-119 | S5 | Lines added or removed above the anchor |
| SwRS-MDOKFSTUDIO-LIFE-119 | S6 | While a block or field editor is open |
| SwRS-MDOKFSTUDIO-LIFE-125 | S1 | Scroll burst |
| SwRS-MDOKFSTUDIO-LIFE-125 | S2 | Hidden page |
| SwRS-MDOKFSTUDIO-LIFE-127 | S3 | A saved state that cannot be restored |
| SwRS-MDOKFSTUDIO-LIFE-127 | S6 | Identity of a saved state |
| SwRS-MDOKFSTUDIO-LIFE-143 | S4 | Problems entries cleared |
| SwRS-MDOKFSTUDIO-LIFE-143 | S6 | Deactivation |
| SwRS-MDOKFSTUDIO-LIFE-149 | S1 | Both open |
| SwRS-MDOKFSTUDIO-LIFE-149 | S4 | Native diff |
| SwRS-MDOKFSTUDIO-LIFE-151 | S3 | Preview reopened at once |
| SwRS-MDOKFSTUDIO-LIFE-151 | S5 | User lock |
| SwRS-MDOKFSTUDIO-LIFE-156 | S3 | Description limit |
| SwRS-MDOKFSTUDIO-LIFE-156 | S4 | Generated schema |
| SwRS-MDOKFSTUDIO-LIFE-169 | S7 | The host refuses a value outside the table |
| SwRS-MDOKFSTUDIO-LIFE-170 | S1 | Order of sources for each view choice |
| SwRS-MDOKFSTUDIO-LIFE-180 | S1 | Nominal case |
| SwRS-MDOKFSTUDIO-LIFE-187 | S2 | Routing |
| SwRS-MDOKFSTUDIO-LIFE-189 | S2 | Lifetime |
| SwRS-MDOKFSTUDIO-LIFE-190 | S1 | Arrow keys do not mark |
| SwRS-MDOKFSTUDIO-LIFE-193 | S2 | Nested, folded and later cases |
| SwRS-MDOKFSTUDIO-MYST-001 | S2 | Kind outside the named list |
| SwRS-MDOKFSTUDIO-MYST-001 | S7 | Simple and icon-less admonitions |
| SwRS-MDOKFSTUDIO-MYST-006 | S1 | Admonitions nest inside each other |
| SwRS-MDOKFSTUDIO-MYST-013 | S5 | Non-context tags are never grouped |
| SwRS-MDOKFSTUDIO-MYST-013 | S7 | A raw HTML block with tags and Markdown is split |
| SwRS-MDOKFSTUDIO-MYST-017 | S4 | Numbered references stay inert placeholders |
| SwRS-MDOKFSTUDIO-MYST-031 | S2 | Fence form and caption source |
| SwRS-MDOKFSTUDIO-MYST-031 | S4 | A valid width is kept |
| SwRS-MDOKFSTUDIO-MYST-031 | S5 | An invalid width is dropped |
| SwRS-MDOKFSTUDIO-MYST-031 | S6 | The page applies the width, also after updates |
| SwRS-MDOKFSTUDIO-MYST-036 | S3 | The icon is not a mapped block and carries its source line |
| SwRS-MDOKFSTUDIO-MYST-036 | S4 | The labelled block keeps its own mapping |
| SwRS-MDOKFSTUDIO-MYST-038 | S4 | Enter sends the rename or closes |
| SwRS-MDOKFSTUDIO-MYST-038 | S9 | A successful rename reports the remaining uses |
| SwRS-MDOKFSTUDIO-MYST-038 | S10 | Progress, refusal and silence of the host |
| SwRS-MDOKFSTUDIO-MYST-045 | S5 | A valid message is answered with its edit id |
| SwRS-MDOKFSTUDIO-MYST-045 | S6 | Accepted shape of the rename message |
| SwRS-MDOKFSTUDIO-MYST-063 | S1 | A list-table renders like a pipe table |
| SwRS-MDOKFSTUDIO-MYST-063 | S6 | A table directive around a raw HTML table |
| SwRS-MDOKFSTUDIO-MYST-063 | S7 | The csv-table directive renders a table |
| SwRS-MDOKFSTUDIO-MYST-066 | S6 | List literal forms are read completely |
| SwRS-MDOKFSTUDIO-MYST-072 | S2 | The same syntax twice gives one warning |
| SwRS-MDOKFSTUDIO-MYST-072 | S4 | The status list shows the fixed wording |
| SwRS-MDOKFSTUDIO-MYST-078 | S1 | A warning becomes a Problems entry |
| SwRS-MDOKFSTUDIO-MYST-078 | S2 | The line is clamped to the document |
| SwRS-MDOKFSTUDIO-MYST-078 | S4 | Entries are replaced and removed |
| SwRS-MDOKFSTUDIO-MYST-081 | S3 | The banner takes no layout room |
| SwRS-MDOKFSTUDIO-MYST-081 | S5 | A malformed or mismatched previewShowProblems is ignored |
| SwRS-MDOKFSTUDIO-MYST-100 | S4 | Empty cards and unsafe class names |
| SwRS-MDOKFSTUDIO-PALETTE-001 | S4 | The editor opened from an insert point |
| SwRS-MDOKFSTUDIO-PALETTE-001 | S5 | Choosing another mode |
| SwRS-MDOKFSTUDIO-PALETTE-001 | S8 | The cell formatting group follows the mode |
| SwRS-MDOKFSTUDIO-PALETTE-003 | S2 | Listing |
| SwRS-MDOKFSTUDIO-PALETTE-017 | S1 | Platform key |
| SwRS-MDOKFSTUDIO-PALETTE-017 | S3 | Wrong modifier |
| SwRS-MDOKFSTUDIO-PALETTE-017 | S4 | Return to the text box |
| SwRS-MDOKFSTUDIO-PALETTE-017 | S5 | Composition |
| SwRS-MDOKFSTUDIO-PALETTE-021 | S7 | A narrow pane |
| SwRS-MDOKFSTUDIO-PALETTE-031 | S2 | One popover at a time and a toggling button |
| SwRS-MDOKFSTUDIO-PALETTE-031 | S4 | Escape with no popover, second Escape, insertion from the popover |
| SwRS-MDOKFSTUDIO-PALETTE-036 | S5 | Closing the link panel never produces a save |
| SwRS-MDOKFSTUDIO-PALETTE-039 | S6 | A matched shortcut is consumed |
| SwRS-MDOKFSTUDIO-PALETTE-043 | S2 | Menu entries and tooltip |
| SwRS-MDOKFSTUDIO-PALETTE-043 | S3 | Two lines |
| SwRS-MDOKFSTUDIO-PALETTE-043 | S5 | No change or unknown level |
| SwRS-MDOKFSTUDIO-PALETTE-050 | S2 | Empty text |
| SwRS-MDOKFSTUDIO-PALETTE-050 | S3 | Caret position and existing blank lines |
| SwRS-MDOKFSTUDIO-PALETTE-054 | S1 | Real list |
| SwRS-MDOKFSTUDIO-PALETTE-054 | S3 | A chosen language wraps the lines or inserts an empty fence |
| SwRS-MDOKFSTUDIO-PALETTE-054 | S5 | No language or an invalid language name |
| SwRS-MDOKFSTUDIO-PALETTE-058 | S6 | Remove drops the property of the open tab |
| SwRS-MDOKFSTUDIO-PALETTE-058 | S7 | What the sanitizer would strip |
| SwRS-MDOKFSTUDIO-PALETTE-069 | S2 | Where the button shows and hides |
| SwRS-MDOKFSTUDIO-PALETTE-069 | S5 | Caret leaves the code |
| SwRS-MDOKFSTUDIO-PALETTE-069 | S6 | Caret stays in the code |
| SwRS-MDOKFSTUDIO-PALETTE-072 | S2 | The filter matches the words of the English names |
| SwRS-MDOKFSTUDIO-PALETTE-072 | S4 | Enter and arrow keys in the picker |
| SwRS-MDOKFSTUDIO-PALETTE-072 | S6 | Other text |
| SwRS-MDOKFSTUDIO-PALETTE-078 | S3 | Cell click |
| SwRS-MDOKFSTUDIO-PALETTE-078 | S4 | Arrows and Enter |
| SwRS-MDOKFSTUDIO-PALETTE-078 | S5 | Choice without a cell |
| SwRS-MDOKFSTUDIO-PALETTE-078 | S6 | Pointer, range and cell editor |
| SwRS-MDOKFSTUDIO-PALETTE-083 | S2 | Typed letter first |
| SwRS-MDOKFSTUDIO-PALETTE-083 | S3 | Tooltip and accessible name |
| SwRS-MDOKFSTUDIO-PALETTE-083 | S5 | Keys that never match |
| SwRS-MDOKFSTUDIO-PALETTE-089 | S2 | Structure |
| SwRS-MDOKFSTUDIO-PALETTE-089 | S5 | IME composition |
| SwRS-MDOKFSTUDIO-PALETTE-092 | S2 | Empty fields |
| SwRS-MDOKFSTUDIO-PALETTE-092 | S4 | Link around the caret |
| SwRS-MDOKFSTUDIO-PALETTE-092 | S5 | Reference-style link |
| SwRS-MDOKFSTUDIO-PALETTE-109 | S5 | Path refused |
| SwRS-MDOKFSTUDIO-PALETTE-114 | S1 | After a paragraph |
| SwRS-MDOKFSTUDIO-PALETTE-114 | S3 | Author name with control characters |
| SwRS-MDOKFSTUDIO-PALETTE-115 | S2 | Choosing a type |
| SwRS-MDOKFSTUDIO-PALETTE-115 | S4 | Where the list opens |
| SwRS-MDOKFSTUDIO-PALETTE-125 | S2 | Named labels |
| SwRS-MDOKFSTUDIO-PALETTE-127 | S1 | The menu of eleven types |
| SwRS-MDOKFSTUDIO-PALETTE-127 | S2 | Other modes |
| SwRS-MDOKFSTUDIO-PALETTE-127 | S4 | The fence has one colon more than the longest fence inside |
| SwRS-MDOKFSTUDIO-PALETTE-127 | S5 | Unknown or missing type |
| SwRS-MDOKFSTUDIO-PALETTE-132 | S2 | Sample |
| SwRS-MDOKFSTUDIO-PALETTE-133 | S1 | The menu |
| SwRS-MDOKFSTUDIO-PALETTE-133 | S3 | Block |
| SwRS-MDOKFSTUDIO-PALETTE-133 | S4 | Samples with no selection |
| SwRS-MDOKFSTUDIO-PALETTE-133 | S5 | Unknown kind |
| SwRS-MDOKFSTUDIO-PALETTE-136 | S3 | Leading blank lines |
| SwRS-MDOKFSTUDIO-PALETTE-140 | S3 | Keys in the filter and on the entries |
| SwRS-MDOKFSTUDIO-PALETTE-147 | S3 | Labels and selections that give no edit |
| SwRS-MDOKFSTUDIO-PALETTE-148 | S4 | Refused answers |
| SwRS-MDOKFSTUDIO-PALETTE-149 | S2 | Invalid key |
| SwRS-MDOKFSTUDIO-PALETTE-149 | S3 | Keys that give no edit |
| SwRS-MDOKFSTUDIO-PALETTE-150 | S3 | Fence and path |
| SwRS-MDOKFSTUDIO-PALETTE-150 | S4 | Missing path |
| SwRS-MDOKFSTUDIO-PALETTE-150 | S6 | Form opens after the pick |
| SwRS-MDOKFSTUDIO-PALETTE-150 | S8 | Browse refused |
| SwRS-MDOKFSTUDIO-PALETTE-153 | S4 | Fields of the form |
| SwRS-MDOKFSTUDIO-PALETTE-153 | S6 | Lone Markdown image |
| SwRS-MDOKFSTUDIO-PALETTE-153 | S8 | Keys that apply the form |
| SwRS-MDOKFSTUDIO-PALETTE-153 | S9 | Problems under the fields |
| SwRS-MDOKFSTUDIO-PALETTE-160 | S1 | Change |
| SwRS-MDOKFSTUDIO-PALETTE-160 | S2 | Conversion |
| SwRS-MDOKFSTUDIO-PALETTE-160 | S3 | No change |
| SwRS-MDOKFSTUDIO-PALETTE-160 | S6 | Caption, legend and outer fence |
| SwRS-MDOKFSTUDIO-PALETTE-178 | S2 | Fences and bad names |
| SwRS-MDOKFSTUDIO-PALETTE-178 | S5 | Shape of the request and of the answer |
| SwRS-MDOKFSTUDIO-PALETTE-183 | S1 | Nearest first |
| SwRS-MDOKFSTUDIO-PALETTE-183 | S2 | Excluded folder |
| SwRS-MDOKFSTUDIO-PALETTE-183 | S6 | Failed scan, restricted reads and stale preview |
| SwRS-MDOKFSTUDIO-PALETTE-192 | S4 | Shape of the request |
| SwRS-MDOKFSTUDIO-PALETTE-203 | S1 | A screenshot is saved and inserted |
| SwRS-MDOKFSTUDIO-PALETTE-203 | S2 | What the paste hook takes over |
| SwRS-MDOKFSTUDIO-PALETTE-213 | S2 | The host converts without touching a file |
| SwRS-MDOKFSTUDIO-PALETTE-213 | S4 | The conversion fails or the editor is gone |
| SwRS-MDOKFSTUDIO-PALETTE-213 | S5 | The message shape |
| SwRS-MDOKFSTUDIO-PALETTE-217 | S1 | Headings and emphasis, also from styles |
| SwRS-MDOKFSTUDIO-PALETTE-217 | S2 | Links and images |
| SwRS-MDOKFSTUDIO-PALETTE-217 | S3 | Lists with nesting, start number and task boxes |
| SwRS-MDOKFSTUDIO-PALETTE-217 | S4 | Word list paragraphs |
| SwRS-MDOKFSTUDIO-PALETTE-217 | S7 | Tables |
| SwRS-MDOKFSTUDIO-PALETTE-229 | S2 | Only a few attributes are read |
| SwRS-MDOKFSTUDIO-PALETTE-229 | S3 | An unsafe address keeps only the text |
| SwRS-MDOKFSTUDIO-PALETTE-232 | S2 | A slash inside a word, an address or a tag |
| SwRS-MDOKFSTUDIO-PALETTE-232 | S3 | A selection, a paste or an IME composition |
| SwRS-MDOKFSTUDIO-PALETTE-232 | S4 | Code |
| SwRS-MDOKFSTUDIO-PALETTE-238 | S2 | An empty query groups the commands, a query ranks them |
| SwRS-MDOKFSTUDIO-PALETTE-238 | S3 | Variants run an action with a ready-made argument |
| SwRS-MDOKFSTUDIO-PALETTE-238 | S6 | A query that matches nothing |
| SwRS-MDOKFSTUDIO-PALETTE-240 | S2 | Scattered letters and short queries |
| SwRS-MDOKFSTUDIO-PALETTE-240 | S4 | Typing narrows the list and resets the highlight |
| SwRS-MDOKFSTUDIO-PALETTE-242 | S2 | Enter or Tab runs the lit command in one edit |
| SwRS-MDOKFSTUDIO-PALETTE-242 | S3 | A click runs a command and a hover lights it |
| SwRS-MDOKFSTUDIO-PALETTE-242 | S6 | Backspace narrows the query or closes the menu |
| SwRS-MDOKFSTUDIO-PALETTE-242 | S7 | Leaving the query closes the menu and keeps the text |
| SwRS-MDOKFSTUDIO-PALETTE-242 | S8 | Chords, compositions and other keys are not taken by the menu |
| SwRS-MDOKFSTUDIO-PALETTE-252 | S1 | Open menu |
| SwRS-MDOKFSTUDIO-PALETTE-252 | S2 | Closed menu |
| SwRS-MDOKFSTUDIO-PALETTE-252 | S4 | Entry text is never markup |
| SwRS-MDOKFSTUDIO-PALETTE-256 | S1 | Room below |
| SwRS-MDOKFSTUDIO-PALETTE-256 | S2 | No room below |
| SwRS-MDOKFSTUDIO-PALETTE-256 | S4 | Pane edge |
| SwRS-MDOKFSTUDIO-PALETTE-263 | S3 | An alias shared by two commands |
| SwRS-MDOKFSTUDIO-PALETTE-263 | S4 | A command outside its mode or place is not listed |
| SwRS-MDOKFSTUDIO-PALETTE-263 | S5 | A command found by an alias runs as its button |
| SwRS-MDOKFSTUDIO-PALETTE-264 | S4 | The image extension |
| SwRS-MDOKFSTUDIO-PALETTE-266 | S1 | Caret in a line |
| SwRS-MDOKFSTUDIO-PALETTE-266 | S2 | Selection of lines, and unwrap |
| SwRS-MDOKFSTUDIO-PALETTE-266 | S4 | Keys and lines that do nothing |
| SwRS-MDOKFSTUDIO-PALETTE-270 | S2 | Cancel, empty title and line breaks |
| SwRS-MDOKFSTUDIO-PALETTE-276 | S2 | Empty pair |
| SwRS-MDOKFSTUDIO-PALETTE-276 | S3 | Bold and Italic share a run of asterisks |
| SwRS-MDOKFSTUDIO-PALETTE-276 | S8 | A selection that cuts into a marker run, or that a role cannot hold |
| SwRS-MDOKFSTUDIO-PALETTE-276 | S9 | Edges, lines and other markers |
| SwRS-MDOKFSTUDIO-PALETTE-278 | S4 | A mode that does not list the action offers no command |
| SwRS-MDOKFSTUDIO-PALETTE-279 | S2 | After the guard window |
| SwRS-MDOKFSTUDIO-REVIEW-001 | S3 | Unknown fields |
| SwRS-MDOKFSTUDIO-REVIEW-001 | S5 | Stable written form |
| SwRS-MDOKFSTUDIO-REVIEW-002 | S1 | Palette pairs |
| SwRS-MDOKFSTUDIO-REVIEW-003 | S2 | Read mode |
| SwRS-MDOKFSTUDIO-REVIEW-004 | S5 | Same content again |
| SwRS-MDOKFSTUDIO-REVIEW-012 | S2 | Orphan verdict |
| SwRS-MDOKFSTUDIO-REVIEW-012 | S5 | Change of the file outside the Studio |
| SwRS-MDOKFSTUDIO-REVIEW-012 | S6 | The same threads are not posted twice |
| SwRS-MDOKFSTUDIO-REVIEW-012 | S10 | After a write by the host |
| SwRS-MDOKFSTUDIO-REVIEW-012 | S11 | Shape of the threads message the page accepts |
| SwRS-MDOKFSTUDIO-REVIEW-017 | S8 | Resolved style |
| SwRS-MDOKFSTUDIO-REVIEW-017 | S11 | Another word |
| SwRS-MDOKFSTUDIO-REVIEW-021 | S5 | The popover stays inside the pane horizontally |
| SwRS-MDOKFSTUDIO-REVIEW-021 | S6 | Closing the popover |
| SwRS-MDOKFSTUDIO-REVIEW-028 | S3 | Nothing to list |
| SwRS-MDOKFSTUDIO-REVIEW-028 | S6 | The host verdict decides where a thread goes |
| SwRS-MDOKFSTUDIO-REVIEW-038 | S3 | The button is hidden while busy |
| SwRS-MDOKFSTUDIO-REVIEW-038 | S5 | Copy and Shift+click keep working |
| SwRS-MDOKFSTUDIO-REVIEW-038 | S6 | The keyboard shortcut opens the comment box |
| SwRS-MDOKFSTUDIO-REVIEW-044 | S1 | Box content |
| SwRS-MDOKFSTUDIO-REVIEW-044 | S2 | Save or Cmd/Ctrl+Enter sends the comment |
| SwRS-MDOKFSTUDIO-REVIEW-044 | S4 | Escape or Cancel closes the box |
| SwRS-MDOKFSTUDIO-REVIEW-044 | S5 | Keys typed in the box stay in the box |
| SwRS-MDOKFSTUDIO-REVIEW-044 | S6 | A saved comment closes the box |
| SwRS-MDOKFSTUDIO-REVIEW-044 | S8 | No answer from the host after 15 seconds |
| SwRS-MDOKFSTUDIO-REVIEW-044 | S9 | The host answers a blank or invalid comment as empty |
| SwRS-MDOKFSTUDIO-REVIEW-044 | S13 | Reply box: keys typed in the box stay in the box |
| SwRS-MDOKFSTUDIO-REVIEW-044 | S14 | Reply box: length of the reply |
| SwRS-MDOKFSTUDIO-REVIEW-044 | S15 | Reply box: a reply accepted by the host empties the box |
| SwRS-MDOKFSTUDIO-REVIEW-049 | S2 | Normal selection |
| SwRS-MDOKFSTUDIO-REVIEW-054 | S7 | A refusal also shows a warning |
| SwRS-MDOKFSTUDIO-REVIEW-054 | S8 | The change is written once the cause is gone |
| SwRS-MDOKFSTUDIO-REVIEW-054 | S10 | Invalid create messages |
| SwRS-MDOKFSTUDIO-REVIEW-065 | S1 | Setting wins |
| SwRS-MDOKFSTUDIO-REVIEW-065 | S2 | Order of the sources |
| SwRS-MDOKFSTUDIO-REVIEW-065 | S3 | The name is cleaned and cut |
| SwRS-MDOKFSTUDIO-REVIEW-074 | S8 | Invalid reply message |
| SwRS-MDOKFSTUDIO-REVIEW-086 | S4 | One action at a time |
| SwRS-MDOKFSTUDIO-REVIEW-094 | S7 | Typing writes nothing |
| SwRS-MDOKFSTUDIO-REVIEW-094 | S8 | Change of a clean document |
| SwRS-MDOKFSTUDIO-REVIEW-100 | S2 | Unchanged threads are kept |
| SwRS-MDOKFSTUDIO-REVIEW-107 | S6 | Single fuzzy match |
| SwRS-MDOKFSTUDIO-REVIEW-107 | S7 | Large document |
| SwRS-MDOKFSTUDIO-REVIEW-107 | S8 | Budget exhausted |
| SwRS-MDOKFSTUDIO-REVIEW-119 | S2 | Nothing moved |
| SwRS-MDOKFSTUDIO-REVIEW-119 | S6 | Document over 8 MiB |
| SwRS-MDOKFSTUDIO-REVIEW-125 | S1 | Rename |
| SwRS-MDOKFSTUDIO-REVIEW-125 | S2 | Move to another folder |
| SwRS-MDOKFSTUDIO-REVIEW-125 | S5 | Own document |
| SwRS-MDOKFSTUDIO-REVIEW-125 | S6 | Renames that move nothing |
| SwRS-MDOKFSTUDIO-REVIEW-133 | S5 | Several comments and comments next to lists |
| SwRS-MDOKFSTUDIO-REVIEW-139 | S2 | Glued or lower case |
| SwRS-MDOKFSTUDIO-REVIEW-139 | S3 | TODO in code, links and URLs |
| SwRS-MDOKFSTUDIO-REVIEW-139 | S5 | Comment word glued to letters |
| SwRS-MDOKFSTUDIO-REVIEW-143 | S2 | Enter and Space toggle the box |
| SwRS-MDOKFSTUDIO-REVIEW-143 | S3 | Targets and keys that change nothing |
| SwRS-MDOKFSTUDIO-REVIEW-143 | S5 | Open boxes are kept for the panel |
| SwRS-MDOKFSTUDIO-REVIEW-143 | S7 | Opening or closing a box keeps the reading position |
| SwRS-MDOKFSTUDIO-REVIEW-143 | S8 | Square corners |
| SwRS-MDOKFSTUDIO-REVIEW-152 | S4 | The host tells the page the value |
| SwRS-MDOKFSTUDIO-REVIEW-152 | S10 | Current show-comments message |
| SwRS-MDOKFSTUDIO-REVIEW-160 | S1 | Caret in a line |
| SwRS-MDOKFSTUDIO-REVIEW-160 | S2 | Selection of two lines |
| SwRS-MDOKFSTUDIO-REVIEW-160 | S3 | Unwrap when every touched line is wrapped |
| SwRS-MDOKFSTUDIO-REVIEW-160 | S4 | Mixed selection and selection ending at a line start |
| SwRS-MDOKFSTUDIO-REVIEW-160 | S5 | Blank line |
| SwRS-MDOKFSTUDIO-REVIEW-160 | S8 | The slash menu finds the action by three names |
| SwRS-MDOKFSTUDIO-REVIEW-167 | S4 | Indentation and blank lines |
| SwRS-MDOKFSTUDIO-REVIEW-171 | S1 | Controls added once |
| SwRS-MDOKFSTUDIO-REVIEW-171 | S6 | The host refuses the change |
| SwRS-MDOKFSTUDIO-REVIEW-186 | S2 | Line break, indentation and text after the marker |
| SwRS-MDOKFSTUDIO-REVIEW-186 | S3 | Author in the header |
| SwRS-MDOKFSTUDIO-REVIEW-186 | S4 | Closing marker position and marker in the text |
| SwRS-MDOKFSTUDIO-REVIEW-192 | S2 | Position of the thread in the file |
| SwRS-MDOKFSTUDIO-REVIEW-192 | S5 | Invalid delete message |
| SwRS-MDOKFSTUDIO-REVIEW-195 | S2 | When the marks are posted |
| SwRS-MDOKFSTUDIO-REVIEW-195 | S8 | Git available |
| SwRS-MDOKFSTUDIO-REVIEW-207 | S3 | Size of one bar |
| SwRS-MDOKFSTUDIO-REVIEW-207 | S8 | Not a list |
| SwRS-MDOKFSTUDIO-REVIEW-214 | S1 | The label follows the state |
| SwRS-MDOKFSTUDIO-REVIEW-214 | S5 | The setting |
| SwRS-MDOKFSTUDIO-REVIEW-219 | S2 | A quote retyped in a document with unsaved changes |
| SwRS-MDOKFSTUDIO-TABLE-001 | S2 | Edit mode off |
| SwRS-MDOKFSTUDIO-TABLE-001 | S6 | A click opens the cell with the focus in the text box and the caret at the end |
| SwRS-MDOKFSTUDIO-TABLE-001 | S7 | The cell editor region shows no status hint |
| SwRS-MDOKFSTUDIO-TABLE-002 | S9 | One edit, one undo |
| SwRS-MDOKFSTUDIO-TABLE-006 | S2 | Long text wraps and the cell grows |
| SwRS-MDOKFSTUDIO-TABLE-006 | S3 | Unbreakable text |
| SwRS-MDOKFSTUDIO-TABLE-007 | S8 | A table inside a quote or an admonition |
| SwRS-MDOKFSTUDIO-TABLE-007 | S9 | Handle strip at the top of the page |
| SwRS-MDOKFSTUDIO-TABLE-013 | S1 | Typing in one cell |
| SwRS-MDOKFSTUDIO-TABLE-013 | S3 | Switch to a neighbouring cell |
| SwRS-MDOKFSTUDIO-TABLE-013 | S4 | Cell missing from the model |
| SwRS-MDOKFSTUDIO-TABLE-013 | S5 | Switch right after typing |
| SwRS-MDOKFSTUDIO-TABLE-013 | S7 | The cell the editor leaves shows its rendered content again |
| SwRS-MDOKFSTUDIO-TABLE-013 | S8 | Editor closed |
| SwRS-MDOKFSTUDIO-TABLE-018 | S2 | Enter chords and the Done button |
| SwRS-MDOKFSTUDIO-TABLE-018 | S6 | Focus leaving the cell formatting group |
| SwRS-MDOKFSTUDIO-TABLE-018 | S8 | A click outside any editable block or on a link |
| SwRS-MDOKFSTUDIO-TABLE-025 | S11 | Blur after Escape |
| SwRS-MDOKFSTUDIO-TABLE-025 | S15 | Escape during a composition |
| SwRS-MDOKFSTUDIO-TABLE-025 | S16 | Escape after the composition |
| SwRS-MDOKFSTUDIO-TABLE-034 | S4 | Enter after the refusal |
| SwRS-MDOKFSTUDIO-TABLE-048 | S2 | Placement and lifetime |
| SwRS-MDOKFSTUDIO-TABLE-048 | S3 | Seven labelled operation buttons |
| SwRS-MDOKFSTUDIO-TABLE-048 | S7 | Narrow pane |
| SwRS-MDOKFSTUDIO-TABLE-055 | S4 | Disabled buttons and model refusals |
| SwRS-MDOKFSTUDIO-TABLE-055 | S5 | Typed text kept |
| SwRS-MDOKFSTUDIO-TABLE-055 | S6 | Saved by the button itself |
| SwRS-MDOKFSTUDIO-TABLE-055 | S12 | Style kept |
| SwRS-MDOKFSTUDIO-TABLE-064 | S6 | No scroll into view |
| SwRS-MDOKFSTUDIO-TABLE-064 | S8 | A later layout change hides the bar again |
| SwRS-MDOKFSTUDIO-TABLE-085 | S3 | Cmd or Ctrl with B, I or K |
| SwRS-MDOKFSTUDIO-TABLE-085 | S7 | The group leaves with the editor |
| SwRS-MDOKFSTUDIO-TABLE-091 | S1 | Typed pipe |
| SwRS-MDOKFSTUDIO-TABLE-091 | S4 | Escaped pipes and line break pairs in text inserted from the bar |
| SwRS-MDOKFSTUDIO-TABLE-094 | S3 | The edited cell keeps its leading whitespace and its width |
| SwRS-MDOKFSTUDIO-TABLE-094 | S5 | A new row takes the style of a neighbouring body row |
| SwRS-MDOKFSTUDIO-TABLE-094 | S6 | Deleting a row removes exactly one line |
| SwRS-MDOKFSTUDIO-TABLE-094 | S7 | The header row is not deleted |
| SwRS-MDOKFSTUDIO-TABLE-094 | S15 | Text after the closing pipe of a body row |
| SwRS-MDOKFSTUDIO-TABLE-106 | S1 | 3 rows and 4 columns |
| SwRS-MDOKFSTUDIO-TABLE-106 | S2 | Size limits |
| SwRS-MDOKFSTUDIO-TABLE-106 | S3 | In the middle of a paragraph |
| SwRS-MDOKFSTUDIO-TABLE-106 | S5 | After a line break, a blank line or a selection |
| SwRS-MDOKFSTUDIO-TABLE-111 | S1 | Centre a column |
| SwRS-MDOKFSTUDIO-TABLE-111 | S4 | Caret in any row, with or without edge pipes |
| SwRS-MDOKFSTUDIO-TABLE-111 | S6 | Caret in the text after a row's closing pipe |
| SwRS-MDOKFSTUDIO-TABLE-111 | S8 | Strict mode |
| SwRS-MDOKFSTUDIO-TABLE-115 | S3 | Caret in a paragraph |
| SwRS-MDOKFSTUDIO-TABLE-115 | S4 | Caret in another table form |
| SwRS-MDOKFSTUDIO-TABLE-117 | S1 | Caret on header, delimiter or last row |
| SwRS-MDOKFSTUDIO-TABLE-117 | S3 | Alignment, empty cells and unicode |
| SwRS-MDOKFSTUDIO-TABLE-117 | S4 | No body rows |
| SwRS-MDOKFSTUDIO-TABLE-117 | S5 | Caret in a paragraph |
| SwRS-MDOKFSTUDIO-TABLE-117 | S8 | No table tools |
| SwRS-MDOKFSTUDIO-TABLE-120 | S5 | One undo step |
| SwRS-MDOKFSTUDIO-TABLE-122 | S2 | Pipe table action: List-table from any line |
| SwRS-MDOKFSTUDIO-TABLE-122 | S3 | A simple HTML table converts to either form |
| SwRS-MDOKFSTUDIO-TABLE-122 | S5 | Caret elsewhere |
| SwRS-MDOKFSTUDIO-TABLE-122 | S6 | Table bar: Convert after typing |
| SwRS-MDOKFSTUDIO-TABLE-122 | S7 | Table bar: Table in a captioned figure |
| SwRS-MDOKFSTUDIO-TABLE-122 | S11 | Table bar: A table inside a quote or an admonition |
| SwRS-MDOKFSTUDIO-TABLE-122 | S16 | Table already in the target form |
| SwRS-MDOKFSTUDIO-TABLE-122 | S20 | Escaped pipes |
| SwRS-MDOKFSTUDIO-TABLE-122 | S21 | Alignment |
| SwRS-MDOKFSTUDIO-TABLE-122 | S22 | List-table read in every fence style |
| SwRS-MDOKFSTUDIO-TABLE-122 | S24 | Other styles lose their style |
| SwRS-MDOKFSTUDIO-TABLE-123 | S5 | Keys that stay native |
| SwRS-MDOKFSTUDIO-TABLE-124 | S3 | Final save cannot be posted |
| SwRS-MDOKFSTUDIO-TABLE-124 | S4 | A table inside a quote or an admonition |
| SwRS-MDOKFSTUDIO-THEME-001 | S5 | Icon set is well formed |
| SwRS-MDOKFSTUDIO-THEME-016 | S4 | The host tells every open preview |
| SwRS-MDOKFSTUDIO-THEME-016 | S6 | A Markdown document is drawn again |
| SwRS-MDOKFSTUDIO-THEME-016 | S9 | The page reports the theme mode it was given |
| SwRS-MDOKFSTUDIO-THEME-025 | S7 | The same colours on both hosts |
| SwRS-MDOKFSTUDIO-THEME-025 | S8 | The three mode blocks of the stylesheet |
| SwRS-MDOKFSTUDIO-THEME-031 | S1 | Variables of the stylesheet |
| SwRS-MDOKFSTUDIO-THEME-031 | S2 | Rendered pages |
| SwRS-MDOKFSTUDIO-THEME-034 | S2 | Variable not set by the host |
| SwRS-MDOKFSTUDIO-THEME-034 | S3 | Stylesheet without the map |
| SwRS-MDOKFSTUDIO-THEME-034 | S4 | Map first |
| SwRS-MDOKFSTUDIO-THEME-038 | S1 | Zoom in, one step |
| SwRS-MDOKFSTUDIO-THEME-038 | S2 | Zoom in, last step |
| SwRS-MDOKFSTUDIO-THEME-038 | S5 | The zoom a page starts at |
| SwRS-MDOKFSTUDIO-THEME-038 | S6 | The tooltips name the value a click gives |
| SwRS-MDOKFSTUDIO-THEME-038 | S7 | A click at a limit changes nothing |
| SwRS-MDOKFSTUDIO-THEME-043 | S3 | Wide pane |
| SwRS-MDOKFSTUDIO-THEME-043 | S4 | Narrow pane |
| SwRS-MDOKFSTUDIO-TOOLBAR-001 | S2 | Visual order |
| SwRS-MDOKFSTUDIO-TOOLBAR-001 | S6 | Scrolling |
| SwRS-MDOKFSTUDIO-TOOLBAR-001 | S7 | Nothing else makes room |
| SwRS-MDOKFSTUDIO-TOOLBAR-003 | S3 | The chevron is shown when it is useful |
| SwRS-MDOKFSTUDIO-TOOLBAR-007 | S4 | At start and after each press |
| SwRS-MDOKFSTUDIO-TOOLBAR-007 | S5 | The collapsed choice is kept for the workspace |
| SwRS-MDOKFSTUDIO-TOOLBAR-010 | S5 | The three options |
| SwRS-MDOKFSTUDIO-TOOLBAR-018 | S2 | Skipped level |
| SwRS-MDOKFSTUDIO-TOOLBAR-018 | S7 | Comment chips |
| SwRS-MDOKFSTUDIO-TOOLBAR-018 | S8 | Out of range and not a number |
| SwRS-MDOKFSTUDIO-TOOLBAR-025 | S2 | Pointer |
| SwRS-MDOKFSTUDIO-TOOLBAR-025 | S3 | Text aligned with the column |
| SwRS-MDOKFSTUDIO-TOOLBAR-025 | S6 | Table of contents reserve |
| SwRS-MDOKFSTUDIO-TOOLBAR-025 | S8 | Flat, bold style with a rule |
| SwRS-MDOKFSTUDIO-TOOLBAR-025 | S11 | Back to the top |
| SwRS-MDOKFSTUDIO-TOOLBAR-030 | S1 | Deep allowance |
| SwRS-MDOKFSTUDIO-TOOLBAR-030 | S3 | Layout changes with the band |
| SwRS-MDOKFSTUDIO-TOOLBAR-033 | S4 | Each press runs the layout update once |
| SwRS-MDOKFSTUDIO-TOOLBAR-037 | S2 | Wide pane |
| SwRS-MDOKFSTUDIO-TOOLBAR-037 | S3 | Pane width |
| SwRS-MDOKFSTUDIO-TOOLBAR-037 | S5 | Text and tables stay clear in Margin and Full width |
| SwRS-MDOKFSTUDIO-TOOLBAR-037 | S6 | Zoom 200 |
| SwRS-MDOKFSTUDIO-TOOLBAR-040 | S4 | Landmark |
| SwRS-MDOKFSTUDIO-TOOLBAR-040 | S8 | Same text twice |
| SwRS-MDOKFSTUDIO-TOOLBAR-054 | S1 | Start disabled |
| SwRS-MDOKFSTUDIO-TOOLBAR-054 | S4 | Press posts a move |
| SwRS-MDOKFSTUDIO-TOOLBAR-054 | S6 | Document cannot be opened |
| SwRS-MDOKFSTUDIO-TOOLBAR-077 | S6 | With a request |
| SwRS-MDOKFSTUDIO-TOOLBAR-077 | S10 | Request that is not a string |
| SwRS-MDOKFSTUDIO-TOOLBAR-079 | S2 | Same request twice |
| SwRS-MDOKFSTUDIO-TOOLBAR-079 | S8 | No answer for another render |
| SwRS-MDOKFSTUDIO-TOOLBAR-079 | S11 | Requests within the bounds |
| SwRS-MDOKFSTUDIO-TOOLBAR-085 | S1 | Kind and tooltip |
| SwRS-MDOKFSTUDIO-TOOLBAR-094 | S4 | A target that is missing or not a regular file |
| SwRS-MDOKFSTUDIO-TOOLBAR-098 | S1 | One match |
| SwRS-MDOKFSTUDIO-TOOLBAR-098 | S3 | Name with or without an extension, with or without a folder |
| SwRS-MDOKFSTUDIO-TOOLBAR-098 | S4 | Several files match |
| SwRS-MDOKFSTUDIO-TOOLBAR-098 | S5 | No file matches |
| SwRS-MDOKFSTUDIO-TOOLBAR-098 | S6 | A match outside the workspace does not count |
| SwRS-MDOKFSTUDIO-TOOLBAR-117 | S2 | Unknown fragment |
| SwRS-MDOKFSTUDIO-TOOLBAR-120 | S10 | Boolean |
| SwRS-MDOKFSTUDIO-TOOLBAR-120 | S11 | Not a boolean |
| SwRS-MDOKFSTUDIO-TOOLBAR-128 | S5 | A cursor move alone |
| SwRS-MDOKFSTUDIO-TOOLBAR-128 | S6 | Marking and scrolling |
| SwRS-MDOKFSTUDIO-TRUST-001 | S2 | Every editing affordance is present |
| SwRS-MDOKFSTUDIO-TRUST-005 | S6 | Host-side writes follow the trust-free rule |
| SwRS-MDOKFSTUDIO-TRUST-007 | S3 | Writable preview |
| SwRS-MDOKFSTUDIO-TRUST-007 | S4 | Roots the webview may load from |
| SwRS-MDOKFSTUDIO-TRUST-025 | S2 | Reference that is not a safe relative path |
| SwRS-MDOKFSTUDIO-TRUST-025 | S4 | Query and fragment of a reference |
| SwRS-MDOKFSTUDIO-TRUST-036 | S3 | Automatic refresh |
| SwRS-MDOKFSTUDIO-TRUST-036 | S5 | Alternative text of an image |
| SwRS-MDOKFSTUDIO-TRUST-052 | S1 | Registered type with a valid envelope |
| SwRS-MDOKFSTUDIO-TRUST-052 | S3 | Identity fields and size bound of the envelope |
| SwRS-MDOKFSTUDIO-TRUST-052 | S5 | Fields accepted only on the type that owns them |
| SwRS-MDOKFSTUDIO-TRUST-052 | S6 | Block edit and checkbox request names its editor and its lines |
| SwRS-MDOKFSTUDIO-TRUST-065 | S2 | The five gates |
| SwRS-MDOKFSTUDIO-TRUST-065 | S4 | Gates that accept an older revision |
| SwRS-MDOKFSTUDIO-TRUST-074 | S3 | Contract broken |
| SwRS-MDOKFSTUDIO-TRUST-090 | S8 | Closing the editor forgets the pending requests |
| SwRS-MDOKFSTUDIO-TRUST-090 | S10 | A request of an older render is answered |
| SwRS-MDOKFSTUDIO-TRUST-092 | S1 | Bundle folder kept |
| SwRS-MDOKFSTUDIO-TRUST-092 | S2 | Engine bundle and licence |
| SwRS-MDOKFSTUDIO-TRUST-092 | S4 | Contract broken |

## StRS paths with no marker

| StRS | Path | Title |
|---|---|---|
| StRS-MDOKFSTUDIO-BLOCK-001 | S2 | Reopen a document |
| StRS-MDOKFSTUDIO-BLOCK-006 | S1 | Type, then finish |
| StRS-MDOKFSTUDIO-BLOCK-011 | S3 | Write on a blank line |
| StRS-MDOKFSTUDIO-BLOCK-014 | S1 | Move a block with an arrow |
| StRS-MDOKFSTUDIO-BLOCK-014 | S3 | Move a list item |
| StRS-MDOKFSTUDIO-BLOCK-025 | S1 | Edit a block and undo it |
| StRS-MDOKFSTUDIO-BLOCK-027 | S1 | Copy a selection verbatim |
| StRS-MDOKFSTUDIO-BLOCK-027 | S2 | Copy a selection that an edge cuts inside a construct |
| StRS-MDOKFSTUDIO-CODE-001 | S1 | Read highlighted code |
| StRS-MDOKFSTUDIO-CORE-001 | S1 | Edit and see the preview follow |
| StRS-MDOKFSTUDIO-CORE-003 | S1 | A render fails after a good one |
| StRS-MDOKFSTUDIO-CORE-003 | S2 | A construct needs a full build |
| StRS-MDOKFSTUDIO-CORE-006 | S1 | Install the skill and write Markdown |
| StRS-MDOKFSTUDIO-DIAG-001 | S1 | Insert a diagram and read it |
| StRS-MDOKFSTUDIO-DIAG-006 | S2 | Learn why a diagram has no picture |
| StRS-MDOKFSTUDIO-DIAG-007 | S1 | Draw with an own JAR |
| StRS-MDOKFSTUDIO-DIAG-009 | S1 | Include a local file in a diagram |
| StRS-MDOKFSTUDIO-DIAG-009 | S2 | Keep a diagram in a PUML file |
| StRS-MDOKFSTUDIO-DIAG-015 | S1 | Read a chart in the page |
| StRS-MDOKFSTUDIO-FMEDIT-005 | S1 | Rename a key |
| StRS-MDOKFSTUDIO-FMSCHEMA-001 | S1 | Read and fold the properties |
| StRS-MDOKFSTUDIO-FMSCHEMA-001 | S2 | Edit the frontmatter |
| StRS-MDOKFSTUDIO-FMSCHEMA-006 | S2 | No schema is looked up |
| StRS-MDOKFSTUDIO-FMSCHEMA-014 | S2 | Link problems in the badge |
| StRS-MDOKFSTUDIO-GFM-002 | S2 | Alerts and raw HTML tables |
| StRS-MDOKFSTUDIO-LAYOUT-001 | S2 | Long words and URLs |
| StRS-MDOKFSTUDIO-LAYOUT-003 | S1 | Change the width mode |
| StRS-MDOKFSTUDIO-LAYOUT-004 | S2 | The toolbar covers the first control |
| StRS-MDOKFSTUDIO-LIFE-003 | S2 | Refresh on demand |
| StRS-MDOKFSTUDIO-LIFE-005 | S2 | A dependency changes |
| StRS-MDOKFSTUDIO-LIFE-007 | S1 | Wait for a render |
| StRS-MDOKFSTUDIO-LIFE-007 | S2 | The source is gone |
| StRS-MDOKFSTUDIO-LIFE-010 | S2 | The reading line survives an update |
| StRS-MDOKFSTUDIO-LIFE-014 | S2 | A view choice is remembered |
| StRS-MDOKFSTUDIO-LIFE-021 | S1 | Find and set a Studio setting |
| StRS-MDOKFSTUDIO-LIFE-022 | S2 | Remove the folder of a preview |
| StRS-MDOKFSTUDIO-LIFE-023 | S1 | Open Studio at a line |
| StRS-MDOKFSTUDIO-LIFE-023 | S2 | Keep the raw text one command away |
| StRS-MDOKFSTUDIO-LIFE-023 | S3 | Jump while the side preview is open |
| StRS-MDOKFSTUDIO-LIFE-023 | S4 | Get the association back from the old setting |
| StRS-MDOKFSTUDIO-MYST-005 | S1 | A construct only a build resolves |
| StRS-MDOKFSTUDIO-MYST-015 | S1 | An admonition |
| StRS-MDOKFSTUDIO-MYST-015 | S2 | A pasted context tag |
| StRS-MDOKFSTUDIO-MYST-017 | S2 | A table |
| StRS-MDOKFSTUDIO-PALETTE-005 | S2 | See the palette appear softly |
| StRS-MDOKFSTUDIO-PALETTE-007 | S2 | Colour a selection |
| StRS-MDOKFSTUDIO-PALETTE-013 | S1 | Refer to a label of the document |
| StRS-MDOKFSTUDIO-PALETTE-013 | S2 | Fence code in a language |
| StRS-MDOKFSTUDIO-PALETTE-015 | S2 | Find a command by its alternative name |
| StRS-MDOKFSTUDIO-PALETTE-020 | S1 | Insert an alert |
| StRS-MDOKFSTUDIO-PALETTE-021 | S1 | Wrap lines in an admonition |
| StRS-MDOKFSTUDIO-REVIEW-001 | S2 | A thread comes back after an undo |
| StRS-MDOKFSTUDIO-REVIEW-003 | S2 | Reply to a thread and resolve it |
| StRS-MDOKFSTUDIO-REVIEW-008 | S2 | Rename a document |
| StRS-MDOKFSTUDIO-REVIEW-012 | S1 | Open a comment chip |
| StRS-MDOKFSTUDIO-REVIEW-015 | S2 | Delete an inline thread |
| StRS-MDOKFSTUDIO-TABLE-001 | S2 | Edit a cell of a quoted table |
| StRS-MDOKFSTUDIO-TABLE-008 | S2 | Delete a row |
| StRS-MDOKFSTUDIO-TABLE-013 | S2 | Convert the table being edited |
| StRS-MDOKFSTUDIO-THEME-002 | S2 | Switch the theme when the system asks for reduced motion |
| StRS-MDOKFSTUDIO-THEME-004 | S1 | Pick a theme and find it again |
| StRS-MDOKFSTUDIO-TOOLBAR-001 | S1 | Collapse the toolbar and find it collapsed |
| StRS-MDOKFSTUDIO-TOOLBAR-002 | S1 | Fold sections and keep them folded |
| StRS-MDOKFSTUDIO-TOOLBAR-004 | S2 | Change the depth of the band |
| StRS-MDOKFSTUDIO-TOOLBAR-011 | S2 | Follow an anchor |
| StRS-MDOKFSTUDIO-TRUST-009 | S1 | The page asks the host to act |
| StRS-MDOKFSTUDIO-TRUST-009 | S2 | The host answers the page |
