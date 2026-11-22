# order after: add one predecessor without restating the list

Priority P1, next batch (the user, 2026-11-22: "On traitera les problèmes du CLI sur le prochain batch, mets-les en P1"). Seen in batch-30.

`order after CR-x --note <list>` replaces the CR's whole list of predecessors and takes CR ids only. Adding one predecessor (CR-460 after CR-447) means retyping every earlier one, and a slug or a ready path is refused. Intent: a way to add one predecessor without restating the list (an append form, or a clear `--replace`), and the refusal names the accepted forms.
