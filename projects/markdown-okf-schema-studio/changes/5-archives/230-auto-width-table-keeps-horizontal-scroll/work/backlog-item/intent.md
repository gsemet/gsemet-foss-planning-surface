# Wide table does not scroll sideways in Auto width
In Auto width a table wider than the pane is clipped at the pane edge (soft shadow on the right) and its
scrollbar shows, but `scrollLeft` of the `<table>` snaps back to 0 about 50 ms after it is set, and horizontal
wheel events do nothing, so columns past the edge cannot be reached. In Margin and Full width the same table
scrolls sideways normally. Repro: `demo-video/s1-v2/workspace/perf-analysis.md`, Width = Auto, zoom 130 %,
source pane at 40 % (preview pane about 670 CSS px); 8-column table at the end.
