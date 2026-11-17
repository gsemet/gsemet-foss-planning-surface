# Host-side guard on block ranges sent by the page (defense in depth)

From the alert line-shift hotfix (PR #185): the host trusts the page's line numbers for edit open,
Done, cut, copy and move, so any future mapping bug becomes a wrong-line overwrite. Candidate: in
`handleEditOpen`, `handleBlockMove`, `handleBlocksCopyCut`, refuse a range past the end of the
document or starting on a blank line, with a diagnostic. A text-sample comparison (page sends a
snippet) was judged costly (math, tables, diagrams differ from source). Own CR and SwRS (proposed).
