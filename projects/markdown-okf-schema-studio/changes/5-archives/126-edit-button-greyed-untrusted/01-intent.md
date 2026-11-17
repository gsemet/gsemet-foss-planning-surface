# Edit-mode button: say why it is unavailable outside a trusted workspace

Found during the demo tour (2026-10-27): a Markdown file opened from outside the trusted
workspace (a temporary folder) shows no way to enter edit mode, and nothing tells the user why.
They had to guess that workspace trust was the reason.

Expected: the edit-mode (pencil) button stays visible but greyed out (disabled), with a tooltip
such as "Editing is unavailable: this file is not in a trusted workspace". The same rule applies
to any other button that needs trust: show it disabled with the reason, never hide it silently.
Cover with a visual scenario (untrusted file) and update the SwRS.
