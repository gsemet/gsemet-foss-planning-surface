# Intent: order after, add one predecessor without restating the list

Seen in batch-30. `order after <cr> --note <list>` replaces the CR's whole list of predecessors
and takes CR ids only. To add one predecessor (CR-460 after CR-447), the Chief of Staff has to
retype every earlier one, and a slug or a ready path is refused.

The Chief of Staff gets a way to add or remove one predecessor without restating the list,
`--note` keeps its replace meaning, a CR of the batch can be named by its slug or its path as
well as its id, and a refusal lists the forms the command accepts.
