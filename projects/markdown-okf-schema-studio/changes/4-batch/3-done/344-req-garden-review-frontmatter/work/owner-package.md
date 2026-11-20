# CR-344 owner package: edits to the approved StRS REVIEW-001, 003, 012, 015

These four StRS are approved, so the Coder did not edit their authored text. The generated fields
(`derived_by`, Links) of the four changed only because titles of the merged SwRS changed and
because SwRS REVIEW-017/100/054/074/186/152/192 and TRUST-065 were merged or reparented; that is
information only. Apply the edits below on agreement, in the worktree
`requirements/tiers/strs/review-annotations/`, then run `just requirements-update`.

## REVIEW-001 (comments file shown in the page)

Add before `### Main paths` (no SwRS ID in the diagram):

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

## REVIEW-003 (create, reply, resolve, reopen, delete)

Add before `### Main paths`:

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

Main path 2, step 1: replace the citation `SwRS-MDOKFSTUDIO-REVIEW-081` by
`SwRS-MDOKFSTUDIO-REVIEW-044` (**applied on agreement**, see below: it needs the 081 to 044 fold,
which the Coder did not do).

## REVIEW-012 (gray and green chips, TODO action)

- Normative text: replace "from the palette, the slash menu or a shortcut" by "from the edition
  palette or the slash menu". Rationale line: "The TODO action has no shortcut; Ctrl+/ toggles a
  plain comment".
- Main paths:
  - Path 1 gains `Option SwRS-MDOKFSTUDIO-REVIEW-152 (nominal)`: the Comments button hides the
    gray and thread chips.
  - Path 2 "Mark a line as TODO" cites SwRS-MDOKFSTUDIO-REVIEW-160, with options for the unwrap
    and for a line that already holds `-->`.
  - The step citing SwRS-MDOKFSTUDIO-LIFE-170 is removed.
- Diagram:

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

## REVIEW-015 (thread chip, reply, delete)

- Diagram:

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

- Path 2: remove the line
  `Option SwRS-MDOKFSTUDIO-BLOCK-058 (nominal): the edit is one undo step`
  (the Coder already removed REVIEW-015 from SwRS BLOCK-058 `derives_from` in the round, see the
  list below).

## Applied on agreement (not done by the Coder)

1. REVIEW-081 is not folded into REVIEW-044 (REVIEW-003 Main path 2 waits for it).
2. SwRS BLOCK-058 still derives from StRS REVIEW-015: kept until REVIEW-015 loses its
   BLOCK-058 option. Same for SwRS LIFE-170 and StRS REVIEW-012, and SwRS TRUST-001 and
   StRS REVIEW-001, each kept in `derives_from` until the owner agrees.
