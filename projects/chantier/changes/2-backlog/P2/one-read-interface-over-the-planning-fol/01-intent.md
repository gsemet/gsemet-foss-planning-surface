# Intent

Split, 2026-11-18, by the Chief of Staff from `surface-server-one-elected-process-for-t` on its
spec critic's advice (that CR's answer 13). The user, the same day: the surface server "lit les
fichiers mais on va bientot lui donner une persistance pour etre plus rapide (dolt?)"; "poser des
bases solides pour permettre ca plus tard".

One module, `store`, is the only way the board, the hub and `status` read the planning folder:
records, backlog, configuration, journal, directly or through `commands/cost`,
`autosync/reading`, `core/surface_batches`, `status/` and `Repo`. Today it reads the files on
each call and keeps no cache. An index (SQLite, Dolt) can come later behind it, rebuilt from the
files; the files stay the truth, in Markdown and JSON browsable on the forge (`planning-server`'s
answers). A structure test follows those modules.

Not built: the index. No behaviour or output changes. Waits for the CRs that edit the same files
(CR-375, CR-383, CR-384, the addressed events CR, the surface server CR).
