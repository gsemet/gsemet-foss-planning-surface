import sys
sys.path.insert(0, sys.argv[1])
from gard import *

# ---------- FMEDIT-001
edit_strs("FMEDIT-001", rationale="""
- Only one editor is open at a time; a field editor does not open while a block editor is open.
- Plain clicks on a link inside a field value open the editor in edit mode; Cmd/Ctrl+click still follows the link.
- Field and key editors have no edition palette or slash menu.
- The control fits the field type: a choice list for enums, a text box, number, date and time inputs, a checkbox, an item list or a YAML text box; the schema is not applied to the controls, so out-of-range values are caught only at save time.
- Only a changed value is saved; Escape cancels unless a save is in flight; turning edit mode off closes the editor without saving.
- A refusal keeps the editor open with the host message shown and the controls enabled again.
- Each save is one edit of the document, so one Undo reverts it; undo keys typed in a field editor act on the field text only.
""", diagram="""
sequenceDiagram
    actor Writer
    participant Page as Preview (properties table)
    participant Editor as Field editor
    participant Host
    participant Doc as VS Code document
    Writer->>Page: click a name or value cell in edit mode
    Page->>Editor: open the editor of the field type in that cell
    Writer->>Editor: type a value and press Enter
    Editor->>Host: save the field
    Host->>Host: plan the edit and check YAML, type and schema
    alt the value is accepted
        Host->>Doc: change only the lines of the field
        Doc-->>Page: the table is re-rendered in place
    else the value is refused
        Host-->>Editor: the reason is shown and the editor stays open
    end
""", main_sub=[("   - Option SwRS-MDOKFSTUDIO-BLOCK-041 (nominal): other actions that would compete with the editor are refused with a reason\n", "")])

# ---------- FMEDIT-005
edit_strs("FMEDIT-005", diagram="""
sequenceDiagram
    actor Writer
    participant Menu as Field action menu
    participant Host
    participant Doc as VS Code document
    Writer->>Menu: open a field editor and choose Add field
    Menu-->>Writer: the missing schema fields, or a custom key
    Writer->>Menu: pick a schema field or type a custom key
    Menu->>Host: add the field
    Host->>Doc: insert one line where the row appears
    Doc-->>Writer: the table is re-rendered and the editor of the new field opens
    opt Remove field
        Writer->>Menu: choose Remove field
        Note over Menu: disabled when the schema requires the field
        Menu->>Host: remove the field
        Host->>Doc: delete exactly the lines of the field
    end
""")

# ---------- FMEDIT-008
edit_strs("FMEDIT-008", rationale="""
- Quoting style, folded or literal headers, comments, fences, the body and line endings are preserved; anchored or aliased values fall back to a whole-block rewrite.
- Every edit is re-parsed and refused when it would lose, duplicate or corrupt a key; a refusal explains itself and never leaves the document half-edited.
- Trust does not refuse a metadata edit: it works in Restricted Mode and for a file outside every workspace folder as in a trusted workspace. A file that VS Code holds read-only is refused with the reason "This file is read-only in VS Code.", as is every other write.
- The schema check covers type, enum, null and conditional rules; link problems do not block a save.
- When a writer navigates away or the preview needs to flush an open field editor, the typed text is saved as is, without the type and schema check, instead of being dropped, and a warning shows if it is refused.
- A plain save refused by the host is saved again as a flush when a navigation waits for it; a save that gets no result still lets the navigation go after a bounded wait.
- While a field editor is open, the page does not replace the properties table under it.
""", diagram="""
stateDiagram-v2
    [*] --> Open: the writer opens a field editor
    Open --> Saving: the writer saves the value
    Saving --> Saved: only the lines of the field change
    Saving --> Refused: the reason is shown and the typed text is kept
    Refused --> Open: the writer corrects the value
    Open --> Flushed: the writer navigates away and the text is written as typed
    Saved --> [*]
    Flushed --> [*]
""", main="""### Main paths

#### Path 1: Save a value without side effects

1. A field editor is open
   - SwRS-MDOKFSTUDIO-FMEDIT-043: the save changes only the lines of its field and keeps comments, quoting, spacing and line endings
   - Option SwRS-MDOKFSTUDIO-FMEDIT-043 (refusal): an edit that loses or corrupts a key is refused
   - Option SwRS-MDOKFSTUDIO-FMEDIT-016 (refusal): a value that breaks the YAML, the field type or the schema is refused and nothing changes
   - Option SwRS-MDOKFSTUDIO-FMEDIT-067 (nominal): a navigation saves the typed text as a flush
2. The value is saved on the lines of its field and the diff holds only the edited field
""")

# ---------- FMSCHEMA-001
edit_strs("FMSCHEMA-001", head_sub=[
 ("""  that follows the frontmatter settings and that refreshes in place shortly
  after the last edit.""", """  that follows the frontmatter settings and that refreshes in place shortly
  after the last edit, and, when the frontmatter is invalid, explains why while
  the body still renders."""),
 ("""that follows the frontmatter settings and that refreshes in place shortly after the last edit.
""", """that follows the frontmatter settings and that refreshes in place shortly after the last edit, and, when the frontmatter is invalid, explains why while the body still renders.
"""),
], rationale="""
- A block needs a first-line fence and a closing fence alone on its line; a document without a closing fence has no frontmatter. CRLF fences are accepted.
- Invalid YAML shows one row "Invalid frontmatter YAML: {parser message}" and an error badge of 1; a list, a scalar or an empty block shows "Invalid frontmatter YAML: Frontmatter is not a mapping."; the body of the document still renders.
- Frontmatter without a string type, or whose type has no schema, shows a generic two-column table in source key order.
- Values read like YAML in a lean table that fits the preview width and never pushes the page sideways.
- A toggle in the column headers collapses and restores the Description column; the choice survives a refresh and a narrow preview starts collapsed.
- The frontmatter table setting is a boolean, on by default; off, the body still renders and neither the table nor the raw YAML is shown.
- The frontmatter is re-analysed 300 ms after the last change; while a field editor is open the new table waits.
""", diagram="""
sequenceDiagram
    actor Writer
    participant Doc as VS Code document
    participant Host as Host (analyse)
    participant Page as Preview
    Writer->>Doc: open a document that starts with frontmatter
    Doc->>Host: the document text
    Host->>Host: extract the block between the fences and parse the YAML
    alt the block is a valid YAML mapping
        Host->>Page: the properties table and the body
    else the YAML is invalid
        Host->>Page: one error row with the parser message and the body
    end
    Writer->>Doc: edit the text
    Doc->>Host: re-analyse 300 ms after the last change
    Host->>Page: patch the table in place, held while a field editor is open
""", main_sub=[("""   - Option SwRS-MDOKFSTUDIO-FMSCHEMA-001 (refusal): invalid YAML gives one error row and the body still renders
""", """   - Option SwRS-MDOKFSTUDIO-FMSCHEMA-001 (refusal): YAML that does not parse shows one error row "Invalid frontmatter YAML" with the parser message, and the body still renders
   - Option SwRS-MDOKFSTUDIO-FMSCHEMA-001 (refusal): an opening fence without a closing fence
""")])

# ---------- FMSCHEMA-006
edit_strs("FMSCHEMA-006", rationale="""
- The schema folder is the first _schema (preferred) or _schemas folder found walking up from the folder of the document to the workspace folder root; the schema file is {type}.schema.yaml, .yml, .json or .json5 whose stem equals the type, case-insensitively.
- A missing schema file shows an info row and an info badge; no schema folder gives the generic table with no info row; the info row appears only when the frontmatter has a string type.
- In Restricted Mode, and for a standalone file outside the workspace, no schema is looked up and an info row says that schema validation requires a trusted workspace.
- A relative reference that is a whole node is inlined from the schema folder; JSON5 support is minimal (comments only).
- A schema that cannot be parsed gives the generic table with a warning row, an empty schema file leaves the type without schema with an informational row, and a schema that cannot be compiled shows a red row counted as one error while the fields stay listed.
- A schema edit is used at the next analysis (a document change, refresh, re-render or settings change); open previews are not refreshed by it.
""", diagram="""
stateDiagram-v2
    [*] --> Typed: the frontmatter has a string type
    Typed --> Untrusted: Restricted Mode or a standalone file
    Typed --> Searching: walk up to the nearest schema folder
    Searching --> NoFolder: no schema folder
    Searching --> NoFile: no file named by the type
    Searching --> Parsing: the schema file is found
    Parsing --> ParseError: the file cannot be parsed
    Parsing --> Compiling: relative references inlined
    Compiling --> CompileError: the schema cannot be compiled
    Compiling --> Applied: the schema applies to the frontmatter
    Untrusted --> [*]: info row
    NoFolder --> [*]: generic table
    NoFile --> [*]: info row
    ParseError --> [*]: warning row
    CompileError --> [*]: red row
    Applied --> [*]: fields follow the schema
""")

# ---------- FMSCHEMA-010
edit_strs("FMSCHEMA-010", diagram="""
sequenceDiagram
    participant Host
    participant Validator
    participant Page as Preview
    actor Writer
    Host->>Validator: the frontmatter and the schema of its type
    Validator-->>Host: the issues (JSON Schema 2020-12)
    Host->>Page: fields in schema order with their issues on their rows
    Host->>Page: the badge and the line of missing required fields
    Writer->>Page: press the badge
    Page-->>Writer: scroll to the first row with an issue and focus its value cell
""")

# ---------- FMSCHEMA-014
edit_strs("FMSCHEMA-014", rationale="""
- A field is a link field when its schema annotates it with x-okf-link; its values are plain or wikilink targets, and a #fragment or ?query is kept for navigation.
- A target is resolved document-relative, bundle-relative, project-relative or by filename stem (exactly one match required); the bundle root and project root settings and the outside-workspace links setting choose the roots.
- Absolute paths and a target that leaves its root, also through a symlink, are refused; a missing file is reported as not resolving to a file.
- A resolving link shows as a link; otherwise the text shows with an error or warning mark and a plain label that says why, counted in the badge; link problems never block saving other fields.
- Link inspection is deferred: the first paint shows the values as pending and about 150 ms later the table is replaced in place.
- A tooltip shows the target path and the fields found in the target frontmatter.
- Click or Enter in read mode, Cmd/Ctrl+click in edit mode, follows a resolving link; an unusable link is not followed and VS Code shows the reason.
""", diagram="""
sequenceDiagram
    actor Writer
    participant Page as Preview
    participant Host
    participant Files as File system and stem index
    participant Editor as VS Code editor
    Page->>Writer: first paint with the link values pending
    Page->>Host: resolve the links about 150 ms after the render
    Host->>Files: resolve each target from its root
    Files-->>Host: found, missing, ambiguous or outside the root
    Host->>Page: the table with the status of each link
    Writer->>Page: hover or focus a link and read its tooltip
    Writer->>Page: click, or press Enter on, a link
    Page->>Host: follow the link
    alt the link resolves
        Host->>Editor: open the target at the marker line
    else the link is unusable
        Host-->>Writer: a warning with the reason
    end
""", main_sub=[("   - Option SwRS-MDOKFSTUDIO-FMSCHEMA-060 (refusal): a configured root that cannot be used", "   - Option SwRS-MDOKFSTUDIO-FMSCHEMA-050 (refusal): a configured root that cannot be used")])

# ---------- REVIEW-008
edit_strs("REVIEW-008", diagram="""
stateDiagram-v2
    [*] --> Anchored: the thread sits on its quote
    Anchored --> Shifted: edits above move its lines in memory
    Shifted --> SavedLines: the document is saved
    SavedLines --> Anchored
    Anchored --> Moved: the quote is found at another place
    Moved --> SavedLines
    Anchored --> Orphaned: the quote is gone and the lines are kept
    Orphaned --> Anchored: the quote comes back
    Anchored --> Renamed: the document is renamed or moved
    Renamed --> Anchored: the comments file follows unless the new name is taken
""", main_sub=[("""   - Option SwRS-MDOKFSTUDIO-REVIEW-101 (nominal): a deleted quote orphans the thread
""", """   - Option SwRS-MDOKFSTUDIO-REVIEW-100 (refusal): a deleted quote orphans the thread and it keeps its lines
""")])

# ---------- REVIEW-017
edit_strs("REVIEW-017", diagram="""
sequenceDiagram
    actor Writer
    participant Doc as VS Code document
    participant Git as Git extension
    participant Host as Host (incoming changes)
    participant Page as Preview
    Writer->>Doc: edit the document
    Host->>Git: read the file at the last commit (at most 1 MiB)
    Git-->>Host: the text at the last commit
    Host->>Host: compare the lines with the shown text
    Host->>Page: the changed line ranges
    Page->>Page: mark the innermost changed blocks with a green change bar
    Writer->>Page: press the Diff button
    Page-->>Writer: the change bars are hidden
""", main_sub=[("   - Option SwRS-MDOKFSTUDIO-REVIEW-208 (refusal): a malformed range is ignored", "   - Option SwRS-MDOKFSTUDIO-REVIEW-207 (refusal): a malformed range is ignored")])
