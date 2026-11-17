# Heavy CI: real-input integration fails at the typing and undo scenario

Heavy integration (real VS Code) stops with "Timed out waiting for the block editor to close before
the undo" since the block-open change (a click on another block opens it after the save). The
scenario clicks the heading after typing in a paragraph; the heading's editor now opens.
