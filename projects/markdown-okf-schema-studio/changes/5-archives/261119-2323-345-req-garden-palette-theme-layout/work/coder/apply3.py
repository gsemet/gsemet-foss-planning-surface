import sys, datetime
B = r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/345-req-garden-palette-theme-layout/work/coder"
sys.path.insert(0, B)
from fm import *

NOW = datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def edit(short, reps=(), drops=(), diagram=None, caption="", approve=False, title=None, need=None):
    sid = full(short)
    body = getbody(sid)
    for old, new in reps:
        assert old in body, (short, old[:50])
        body = body.replace(old, new)
    for pre in drops:
        lines = body.split("\n")
        n = [l for l in lines if l.startswith(pre)]
        assert len(n) == 1, (short, pre, len(n))
        body = "\n".join(l for l in lines if not l.startswith(pre))
    if diagram:
        assert "### Use case diagram" not in body
        sec = "### Use case diagram\n\n```mermaid\n" + diagram.strip("\n") + "\n```\n\n" + (caption + "\n\n" if caption else "")
        assert body.count("### Main paths") == 1
        body = body.replace("### Main paths", sec + "### Main paths")
    setbody(sid, body)
    if title:
        setfield(sid, "title", title)
    if need:
        setfield(sid, "user_need", need)
    if approve:
        setfield(sid, "approved_by", "gaetan@xeberon.net")
        setfield(sid, "approved_at", "'" + NOW + "'")


D = {}
D["P002"] = """stateDiagram-v2
    direction LR
    state "Full: Strict, GFM, MyST buttons and charts and diagrams" as Full
    state "MyST: Strict and GFM buttons and MyST constructs" as MyST
    state "GFM: Strict buttons and GFM constructs" as GFM
    state "Strict: Markdown buttons" as Strict
    [*] --> GFM: no choice yet and no setting
    Strict --> GFM: the next set adds buttons
    GFM --> MyST: the next set adds buttons
    MyST --> Full: the next set adds buttons
    Full --> MyST: the writer picks a smaller set
    MyST --> GFM: the writer picks a smaller set
    GFM --> Strict: the writer picks a smaller set"""
D["P005"] = """stateDiagram-v2
    [*] --> Closed
    Closed --> Editing: the writer opens a block editor
    Editing --> Editing: a palette button is pressed, the editor stays open
    Editing --> Editing: the native file dialog opens and closes, the editor stays open
    Editing --> Popover: a picker or the slash menu opens
    Popover --> Editing: Escape closes the popover only
    Editing --> Committed: Done, Cmd or Ctrl and Enter, or leaving the editor
    Editing --> Closed: Escape cancels the editor
    Committed --> Closed"""
D["P007"] = """sequenceDiagram
    actor Writer
    participant Page as Preview page
    participant Host as Host
    participant Dialog as Native dialog
    participant Box as Text box
    Writer->>Page: press the Image button
    Page->>Host: ask for an image file
    Host->>Dialog: open the file dialog, the editor stays open
    alt the writer picks a file
        Dialog-->>Host: the file path
        Host-->>Page: the path relative to the document
        Page->>Box: insert or replace the image reference, one undo step
    else the writer cancels
        Dialog-->>Host: nothing
        Host-->>Page: no path
        Page-->>Writer: the text is unchanged
    end"""
D["P013"] = """sequenceDiagram
    actor Writer
    participant Page as Preview page
    participant Host as Host
    participant Box as Text box
    Writer->>Page: press the Reference button
    Page-->>Writer: the list shows Loading
    Page->>Host: ask for the targets
    Host->>Host: list the labelled targets, or scan at most 20 bibliography files of at most 2 MiB each
    alt the list has entries
        Host-->>Page: the entries, possibly cut, with a note
        Page-->>Writer: the list of targets
        Writer->>Page: pick one
        Page->>Box: write the reference or the citation
    else the list is empty or the host fails
        Host-->>Page: an empty list or an error
        Page-->>Writer: a message and no edit
    end"""
D["P015"] = """stateDiagram-v2
    [*] --> Closed
    Closed --> Open: a slash at the start of a line or after a space
    Closed --> Closed: a slash inside a word
    Open --> Filtered: the writer types, matched by alias or label
    Filtered --> Open: the writer erases the filter
    Open --> Closed: Enter, Tab or a click runs the command in one edit
    Filtered --> Closed: Enter, Tab or a click runs the command in one edit
    Open --> Closed: Escape or the caret leaves, the text is kept
    Filtered --> Closed: Escape or the caret leaves, the text is kept"""
D["P018"] = """sequenceDiagram
    actor Writer
    participant Page as Page paste handler
    participant Host as Host
    participant Box as Text box
    Writer->>Page: paste, or drop files from the Explorer
    alt the clipboard holds text
        Page->>Box: ordinary text paste
    else an image only
        Page->>Host: save the image
        Host-->>Page: the file image-N with its extension
        Page->>Box: a reference as a paragraph of its own
    else rich text
        Page->>Host: convert to the safe subset
        Host-->>Page: Markdown
        Page->>Box: replace the selection
    else a URL
        Page->>Box: a link, an autolink or an image
    else files dropped from the Explorer
        Page->>Box: links or images at the drop point
    end
    Note over Page,Box: one undoable edit saved with the other text"""
D["L001"] = """stateDiagram-v2
    [*] --> Rendered
    Rendered --> Measured: each block is measured
    Measured --> Scrolling: a table wider than the box
    Measured --> AsIs: a table that fits
    Measured --> Wrapped: a long word or a long URL
    Scrolling: Scrolls in its own box with shaded edges
    AsIs: Left as it is
    Wrapped: The text wraps
    Scrolling --> NoOverflow
    AsIs --> NoOverflow
    Wrapped --> NoOverflow
    NoOverflow: No sideways scroll of the page, within 1 px
    NoOverflow --> [*]"""
D["L003"] = """stateDiagram-v2
    [*] --> Margin: nothing stored
    Margin --> Auto: the Width button
    Auto --> Full: the Width button
    Full --> Margin: the Width button
    Margin: Blocks stay in the text column
    Auto: Wide blocks break out of the column
    Full: No column limit and a small gutter
    Margin --> Margin: the maxContentWidth setting changed
    Auto --> Auto: the maxContentWidth setting changed
    Full --> Full: the maxContentWidth setting changed
    note right of Margin: reopening the preview starts from the stored mode"""
D["L004"] = """sequenceDiagram
    participant Page as Page runtime
    participant Measure as Clearance measure
    participant CSS as Page style
    Page->>Measure: the page opens, or a resize, a font load, a toolbar collapse or a width mode change
    loop until the layout is quiet
        Measure->>Measure: read the rectangles of the toolbar, the column and the first control
        Measure->>Page: publish the first clearance, the first inset and the toolbar bottom
    end
    Page->>CSS: the published values
    CSS->>CSS: move the first control down or narrow it out of the toolbar's way"""
D["T002"] = """stateDiagram-v2
    [*] --> Cream: no theme chosen yet
    Current --> Dark: the Theme button
    Dark --> White: the Theme button
    White --> Cream: the Theme button
    Cream --> Current: the Theme button
    Current: Follows the VS Code theme
    Dark: Paints the page, toolbar, heading band and notes
    White: Paints the page, toolbar, heading band and notes
    Cream: Paints the page, toolbar, heading band and notes
    note right of Current: the redraw waits while a block editor is open"""
D["T004"] = """sequenceDiagram
    actor Reader
    participant Page as Preview page
    participant Host as Host
    participant Store as Workspace state
    Reader->>Page: press the Theme button
    Page->>Host: the chosen mode
    alt a known mode
        Host->>Store: store the mode
    else an unknown mode
        Host-->>Page: dropped, the stored mode stays
    end
    Reader->>Page: reopen the preview
    Page->>Host: ready
    Host-->>Page: the stored workspace mode, else the saved panel mode, else Cream"""
D["T011"] = """stateDiagram-v2
    [*] --> Zoom100: no zoom saved
    Zoom100: 100 percent
    Zoom70: 70 percent, Zoom out disabled
    Zoom200: 200 percent, Zoom in disabled
    Zoom100 --> Zoom70: Zoom out, steps of 10 points
    Zoom100 --> Zoom200: Zoom in, steps of 10 points
    Zoom70 --> Zoom100: Zoom in, steps of 10 points
    Zoom200 --> Zoom100: Zoom out, steps of 10 points
    note right of Zoom100: reopening starts from the panel zoom, else the workspace zoom, else 100"""

# ---- PALETTE-002
edit("StRS-PALETTE-002",
     reps=[("let the writer choose between a strict Markdown, a GitHub Flavored Markdown and a MyST set of palette buttons",
            "let the writer choose between four sets of palette buttons, Strict, GFM, MyST and Full, each set containing the one before"),
           ("- The sets add up: the GitHub set holds the strict buttons, and the MyST set holds the GitHub buttons.",
            "- The four sets are nested: GFM holds the Strict buttons, MyST holds the GFM buttons and Full holds the MyST buttons and adds charts and diagrams."),
           ("SwRS-MDOKFSTUDIO-PALETTE-010 (refusal)", "SwRS-MDOKFSTUDIO-LIFE-169 (refusal)")],
     diagram=D["P002"],
     caption="The sets are nested, and a writer moves between them with the mode select or from the keyboard; the choice is kept for the workspace.")

# ---- PALETTE-005
edit("StRS-PALETTE-005",
     reps=[("## The palette stays in reach, appears softly and never closes the editor by accident",
            "## While a writer edits a block, the palette stays in reach, appears softly and keeps the editor open"),
           ("the Studio SHALL keep the edition palette visible next to the text box, also for a very tall text box and in a narrow pane, show it and its menus",
            "the Studio SHALL keep the edition palette in reach next to the text box, also for a very tall text box and in a narrow pane, show it and its menus")],
     title="While a writer edits a block, the palette stays in reach, appears softly and keeps the editor open",
     diagram=D["P005"],
     caption="Pressing a palette button or using the file dialog never commits the edit; only Done, the shortcut or leaving the editor does.")

edit("StRS-PALETTE-007", diagram=D["P007"], caption="The editor stays open while the native dialog is shown.")
edit("StRS-PALETTE-013", diagram=D["P013"], caption="The list is bounded and says when it was cut.")
edit("StRS-PALETTE-015", diagram=D["P015"], caption="A command is one edit, and Escape leaves the text as it is.", approve=True)

edit("StRS-PALETTE-018",
     reps=[("When a writer pastes an image or rich text into a block text box, the Studio SHALL save an image as a file next to the document with a reference as a paragraph of its own, or replace the selection with the rich text converted to Markdown without scripts, styles, hidden content or unsafe addresses, in one undoable step",
            "When a writer pastes an image, rich text or a URL into a block text box, or drops files from the Explorer on it, the Studio SHALL save an image as a file next to the document with a reference as a paragraph of its own, replace the selection with the rich text converted to Markdown without scripts, styles, hidden content or unsafe addresses, turn a pasted URL into a link, an autolink or an image, and link or embed the dropped files at the drop point, each in one undoable step")],
     drops=["- The conversion rules and the image file handling belong"],
     diagram=D["P018"], caption="Text on the clipboard always wins; every other branch ends in one undoable edit.")

# ---- LAYOUT-001 (approved)
edit("StRS-LAYOUT-001",
     reps=[(" As a maintainer, I can run machine layout checks on any preview and trust that they flag real layout defects and stay quiet on pages where they do not apply.", "")],
     drops=["- The layout checks are tooling", "- Each layout check is not applicable", "- Known issue: this is a page-wide promise", "- Known issue: the layout-check behaviour"],
     diagram=D["L001"], caption="Every branch ends with a page that does not scroll sideways.",
     approve=True,
     need="As a reader, I never have to scroll the whole page sideways to read a document, whatever its content, theme or the size of the pane; I reach every column of a wide table without the page moving, I can tell there is more to scroll to, and short identifiers stay readable.")

# ---- LAYOUT-003 (approved): trim the rationale
sid = full("StRS-LAYOUT-003")
body = getbody(sid)
a = body.index("### Rationale and constraints")
b = body.index("### Main paths")
new_rat = """### Rationale and constraints

- The setting maxContentWidth limits and centres the column, 0 lifts the limit, an invalid value falls back to the default, and open previews follow a change without reloading the editor.
- The Width button goes Margin, Auto, Full width, then Margin again, and its icon, label and tooltip say which mode is active.
- The choice is kept for the workspace; at start the saved page state wins over the stored workspace preference, which wins over Margin.
- Margin keeps tables, code blocks and figures inside the text column; they scroll or wrap instead of leaving it.
- In Auto, a table, figure, image, code block or Mermaid diagram wider than the column uses the available width, centred and clear of the pane edges; elements that are not wider are left alone, and an element being edited keeps the column width.
- Full width removes the column limit and keeps a small gutter on each side.
- In every mode, content narrower than the column is centred at its own width and the page stays readable beside the open table of contents.

"""
body = body[:a] + new_rat + body[b:]
setbody(sid, body)
edit("StRS-LAYOUT-003", diagram=D["L003"], caption="The Width button cycles the three modes, and the setting applies in each of them.", approve=True)

# ---- LAYOUT-004
edit("StRS-LAYOUT-004",
     reps=[("SwRS-MDOKFSTUDIO-LAYOUT-018", "SwRS-MDOKFSTUDIO-LAYOUT-011")],
     drops=["- Earlier values (56 px", "- Known issue: CHANGELOG entry 0.2.1"],
     diagram=D["L004"], caption="The clearance is measured again until the layout is quiet.")

# ---- THEME
edit("StRS-THEME-002",
     reps=[("; this scope records the reduced-motion preference on the page.", ".")],
     diagram=D["T002"], caption="Each theme paints the whole page; Current follows the host.")
edit("StRS-THEME-004", reps=[("SwRS-MDOKFSTUDIO-THEME-013 (refusal)", "SwRS-MDOKFSTUDIO-LIFE-169 (refusal)")],
     diagram=D["T004"], caption="An unknown mode is dropped and the stored mode stays.")
edit("StRS-THEME-011", diagram=D["T011"], caption="Zoom moves in steps of 10 points between the two limits.")
