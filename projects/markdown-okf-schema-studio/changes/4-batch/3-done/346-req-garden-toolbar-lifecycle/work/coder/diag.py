from st import *
D={}
D["LIFE-001"]='''flowchart LR
    W([Writer]) -->|Open Preview to Side: command, Explorer, title button, key| P[Preview panel]
    W -->|Open With: Markdown OKF Schema Studio tab| P
    R([Reader]) -->|opens several previews, one per file| P
    B[VS Code built-in preview] -.->|keeps working beside it| P
    P -->|file refused: message, no panel| W'''
D["LIFE-003"]='''sequenceDiagram
    actor Writer
    participant VS as VS Code
    participant Ext as Extension
    participant Pre as Preview
    Writer->>VS: switches the active editor
    VS->>Ext: active editor changed
    Ext->>Ext: is the file eligible
    Ext->>Pre: newest following preview goes pending
    Ext->>Pre: renders the new file, sets the title
    Writer->>Pre: presses Refresh
    Ext->>Pre: renders again from the editor buffer
    Pre-->>Writer: reading place kept'''
D["LIFE-005"]='''sequenceDiagram
    actor Writer
    participant VS as VS Code
    participant Ext as Extension
    participant Wk as Render worker
    participant Pre as Preview
    Writer->>VS: edits, or the file changes outside
    VS->>Ext: change event
    Ext->>Ext: waits for the debounce
    Ext->>Wk: render the document
    Wk-->>Ext: result, or stopped if a newer edit supersedes it
    Ext->>Pre: patch in place with a glow, or a new page
    Pre-->>Writer: ready
    Note over Ext,Pre: after the timeout the full document is rendered'''
D["LIFE-007"]='''stateDiagram-v2
    [*] --> Pending
    Pending --> Ready: render done
    Ready --> PendingNotice: new edit, notice shown
    PendingNotice --> Ready: render done
    PendingNotice --> Failed: render fails, last good page kept
    Failed --> Recovered: next render succeeds
    Recovered --> Ready
    Ready --> SourceMissing: file deleted or moved
    Failed --> SourceMissing: file deleted or moved
    SourceMissing --> [*]'''
D["LIFE-010"]='''sequenceDiagram
    actor Writer
    participant Ed as Text editor
    participant Ext as Extension
    participant Pre as Preview
    Writer->>Ed: scrolls
    Ed->>Ext: first visible line
    Ext->>Pre: page scrolls to that line
    Pre-->>Ext: echo of the scroll, ignored
    Writer->>Pre: scrolls or clicks
    Pre->>Ext: top line of the preview
    Ext->>Ed: editor reveals the line
    Ext->>Pre: anchor restored after a patch'''
D["LIFE-014"]='''stateDiagram-v2
    [*] --> Open
    Open --> Serialized: window reload
    Serialized --> Restored: source file found, same place
    Serialized --> SourceMissing: source file gone
    Restored --> Open
    Open --> Open: view choices stored
    Restored --> Restored: view choices read back'''
D["LIFE-022"]='''stateDiagram-v2
    [*] --> Open
    Open --> Closed: preview closed, render stopped, watchers and Problems entries removed
    Closed --> [*]
    Open --> FolderRemoved: workspace folder removed, reads restricted
    FolderRemoved --> Open: folder added back'''
D["LIFE-021"]='''sequenceDiagram
    actor Reader
    participant VS as VS Code
    participant Ext as Extension manifest
    Reader->>VS: opens Settings
    VS->>Ext: reads the contributed settings
    Ext-->>VS: groups in order, with defaults and descriptions
    VS-->>Reader: lists the groups'''
D["TOOLBAR-001"]='''stateDiagram-v2
    [*] --> Expanded: initial state is the panel choice, else the workspace choice, else collapsed
    Expanded --> Collapsed: collapse
    Collapsed --> Expanded: expand
    Collapsed --> Collapsed: load hint shown once
    Expanded --> Expanded: choice stored for the workspace'''
D["TOOLBAR-002"]='''stateDiagram-v2
    [*] --> Open
    Open --> Folded: fold a section, or Fold all
    Folded --> Open: unfold, or Unfold all
    Folded --> Open: find or navigation targets inside
    Open --> Open: kept across a patch and a reload
    Folded --> Folded: kept across a patch and a reload'''
D["TOOLBAR-003"]='''sequenceDiagram
    actor Writer
    participant Pre as Preview
    participant Host as Extension host
    participant Src as Source file
    Writer->>Pre: Cmd or Ctrl+F
    Pre-->>Writer: find bar, matches and count
    Writer->>Pre: Enter walks the matches
    Writer->>Pre: Replace all
    Pre->>Host: dry run, skipped count shown
    Host->>Src: edits the source spans in one undo step
    Note over Pre,Host: refused while a block editor is open
    Host-->>Pre: new counts'''
D["TOOLBAR-004"]='''sequenceDiagram
    actor Reader
    participant Pre as Preview
    participant Ext as Extension
    Reader->>Pre: scrolls
    Pre->>Pre: heading path up to the depth setting
    Pre-->>Reader: band with one line per heading, shadow under it
    Reader->>Ext: changes the sticky headings setting
    Ext->>Pre: new page'''
D["TOOLBAR-006"]='''stateDiagram-v2
    [*] --> Closed
    Closed --> Column: open, wide pane
    Closed --> Rail: open, pane under 760 px
    Column --> Closed: close
    Rail --> Closed: close
    Column --> Column: current entry follows, click an entry, twisty
    Rail --> Rail: current entry follows, click an entry
    Column --> Column: state stored'''
D["TOOLBAR-009"]='''sequenceDiagram
    actor Writer
    participant Pre as Preview
    participant Ext as Extension
    participant Src as Source file
    Writer->>Pre: types in a block editor
    Writer->>Pre: clicks a link
    Pre->>Ext: save flushed first
    Ext->>Src: change written
    Pre->>Ext: place recorded
    Ext->>Pre: target opened, history state pushed
    Writer->>Pre: Back or Next
    Pre-->>Writer: previous or next place'''
D["TOOLBAR-011"]='''sequenceDiagram
    actor Reader
    participant Pre as Preview
    participant Host as Extension host
    Pre->>Host: links in view, batches of up to 64
    Host->>Host: classifies and resolves each link
    Host-->>Pre: tooltip, or warning icon
    Reader->>Pre: clicks a link
    Pre->>Host: click
    Host-->>Reader: opens it, hands it to the OS, or warns'''
D["TOOLBAR-013"]='''sequenceDiagram
    actor Writer
    participant Ed as Text editor
    participant Ext as Extension
    participant Pre as Preview
    Writer->>Pre: pairs the preview with the editor
    Writer->>Pre: presses Anchor
    Pre->>Ext: mode stored
    Ext->>Pre: preview aligned
    Writer->>Ed: scrolls
    Ed->>Ext: cursor line, with the setting on
    Ext->>Pre: block outlined'''
D["TOOLBAR-014"]='''sequenceDiagram
    actor Writer
    participant Pre as Preview
    participant Host as Extension host
    participant File as HTML file
    Writer->>Pre: Export
    Pre->>Pre: diagrams awaited, snapshot taken
    Host-->>Writer: link warning, cancel stops here
    Host-->>Writer: save dialog, cancel stops here
    Host->>Host: styles, theme, images and math embedded, no script
    Host->>File: one file written'''
for k,v in D.items():
    a=("StRS-"+k)
    add_diagram(a,v)
    print(k,"ok")
print(len(D))
