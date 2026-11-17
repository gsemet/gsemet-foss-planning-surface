# The board's Configuration page writes the project file with LF

Found 2026-11-17 by CR-301's Verifier and Driver (PR 256, merged as 7ae5958): CR-301's
specification says the Configuration page writes the project folder's existing file (else creates
`chantier.yaml`) "UTF-8, LF", but `edit_text.py` keeps CRLF when the existing file is mostly CRLF.
A new file is LF. Filed by the Chief of Staff under the user's leave of 2026-11-17 to fix a few
CRs on its own during the night.
