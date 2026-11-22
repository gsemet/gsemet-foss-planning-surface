# The board's open handle on a CR folder blocks triage on Windows

On Windows, triage failed with WinError 32 (file in use) when it moved a CR folder out of 1-inbox while the surface server (chantier board) was running: the board held a handle open on the folder or one of its files. The workaround was to stop the board, triage, and start it again; triage also refuses while the board is stopped, so the order matters. Seen 2026-11-21 in the chantier project. Expected: triage moves the folder while the board runs (the board closes its handles, retries, or does the move itself), with no stop and restart of the board.

Note (2026-11-21, the Chief of Staff): a second WinError 32 on triage of board-batch-compact cleared once the Chief of Staff's own shell left the CR folder (its working directory was inside it), the board still running. The holder may be any process whose working directory is inside the folder, not the board.
