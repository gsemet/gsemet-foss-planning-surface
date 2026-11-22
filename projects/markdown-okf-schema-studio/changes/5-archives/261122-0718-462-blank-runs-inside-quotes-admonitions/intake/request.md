# Blank-line runs inside quotes and admonitions

Split off from blank-runs-inside-lists (2026-11-21, owner: 'Lists, then others if free'): CR-444's blank-lines block does not serve quotes and admonitions. Empty lines inside a quote or a GitHub alert start with '>', so they are not blank lines and blankRuns never finds them; a MyST admonition is a directive, which needs a rule per directive kind. Owner's goal (2026-11-20): blank lines beyond the one separator are always reachable in edit mode.

Also in scope (from the blank-runs-inside-lists spec critic, 2026-11-21): runs inside a definition list (`dl`/`dd`) and inside a footnote definition body; neither is a list, a quote nor an admonition, so blank-runs-inside-lists shows nothing for them.
