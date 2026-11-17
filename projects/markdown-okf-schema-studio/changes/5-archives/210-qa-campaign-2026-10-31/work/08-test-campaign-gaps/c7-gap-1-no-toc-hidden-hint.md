# c7-gap-1 — TOC toggle active but column hidden on narrow panes, untested

Short note. Severity Low. At 438 px `html[data-sphinx-preview-toc=open]` is set and the toolbar button
shows active, but the nav is `display:none` (CSS hides it on narrow panes). The existing
`toc_column` machine check uses fixed sizes; add a test that asserts either the nav is visible or
the button shows a disabled/hint state below the breakpoint. Replay: manual (narrow pane, click
"Show table of contents").
