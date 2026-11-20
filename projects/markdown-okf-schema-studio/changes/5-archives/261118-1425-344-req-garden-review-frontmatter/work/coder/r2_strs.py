import re, pathlib, sys
NOW = sys.argv[1]
D = {}
D["001"] = """### Use case diagram

```mermaid
sequenceDiagram
    actor Reviewer
    participant Host
    participant File as Comments file
    participant Page as Preview
    Host->>File: read the comments file
    alt the file is valid
        Host->>Page: the threads
        Page->>Page: highlight each quote and list the orphans
        Page-->>Reviewer: highlights and orphan list
    else the file is not valid
        Host-->>Reviewer: one warning, the file stays untouched
    end
    Reviewer->>Page: click a highlight
    Page-->>Reviewer: the thread popover
```

"""
D["003"] = """### Use case diagram

```mermaid
sequenceDiagram
    actor Reviewer
    participant Page as Preview
    participant Host
    participant File as Comments file
    Reviewer->>Page: select text and press Comment
    Page-->>Reviewer: the comment box opens
    Reviewer->>Page: Save
    Page->>Host: create the thread
    Host->>File: append one change after another under the author name
    alt accepted
        Host->>Page: post the threads again
    else refused
        Host-->>Page: the reason
        Page-->>Reviewer: the typed text stays
    end
    Reviewer->>Page: reply, resolve, reopen or delete (confirmed)
    Page->>Host: the change for that thread
```

"""
D["012"] = """### Use case diagram

```mermaid
sequenceDiagram
    actor Writer
    participant Page as Preview
    participant Editor
    Page-->>Writer: gray chips for comments, green chips for threads
    Writer->>Page: click a chip
    Page-->>Writer: the comment box opens
    Writer->>Page: press the Comments button
    Page-->>Writer: gray and thread chips are hidden
    Writer->>Editor: the TODO action from the palette or slash menu
    Editor-->>Writer: the line is wrapped, or unwrapped when it already is
```

"""
D["015"] = """### Use case diagram

```mermaid
sequenceDiagram
    actor Writer
    participant Page as Preview
    participant Host
    participant Doc as Document
    Writer->>Page: click the thread chip
    Page-->>Writer: the thread opens
    Writer->>Page: Reply or Delete
    Page->>Host: the change
    alt an edit is open
        Host-->>Writer: save or cancel the edit first
    else
        Host->>Doc: change only the thread lines
    end
```

"""
P2_012 = """#### Path 2: Mark a line as TODO

1. A block editor is open on a line
   - SwRS-MDOKFSTUDIO-REVIEW-160: the writer runs the TODO action from the edition palette or the slash menu and each touched line is wrapped in a TODO comment
   - Option SwRS-MDOKFSTUDIO-REVIEW-160 (nominal): lines that are all wrapped are unwrapped by the same action
   - Option SwRS-MDOKFSTUDIO-REVIEW-160 (refusal): a line that already holds a comment end is never wrapped
2. The touched lines are wrapped in a TODO comment, or unwrapped

"""
for n, dia in D.items():
    p = pathlib.Path(f"StRS-MDOKFSTUDIO-REVIEW-{n}.md")
    t = p.read_text(encoding="utf8")
    assert "\r" not in t
    assert "### Use case diagram" not in t
    t = t.replace("### Main paths\n", dia + "### Main paths\n", 1)
    t = re.sub(r"(approved_at: )'[^']*'", r"\g<1>'" + NOW + "'", t, 1)
    t = re.sub(r"(verified:\n  by: [^\n]*\n  at: )'[^']*'", r"\g<1>'" + NOW + "'", t, 1)
    if n == "012":
        t, k = re.subn(r"from the keyboard in a block\s+editor", "from the edition palette or the slash menu in a block editor", t)
        assert k == 2, k
        a = "- The TODO shortcut action is also offered by the edition palette and the slash menu.\n"
        assert a in t
        t = t.replace(a, "- The TODO action has no shortcut; Ctrl+/ toggles a plain comment.\n")
        a = "   - Option SwRS-MDOKFSTUDIO-REVIEW-003 (nominal): in edit mode the opened block is titled with the literal tag\n"
        assert a in t
        t = t.replace(a, a + "   - Option SwRS-MDOKFSTUDIO-REVIEW-152 (nominal): the Comments button hides the gray and thread chips\n")
        i = t.index("#### Path 2: Hide the gray chips")
        j = t.index("<!-- okf:links:start -->")
        t = t[:i] + P2_012 + t[j:]
    if n == "015":
        a = "   - Option SwRS-MDOKFSTUDIO-BLOCK-058 (nominal): the edit is one undo step\n"
        assert a in t
        t = t.replace(a, "")
    p.write_text(t, encoding="utf8", newline="")
