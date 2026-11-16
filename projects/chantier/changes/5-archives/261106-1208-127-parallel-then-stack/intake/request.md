# In a stack, CRs run in parallel on main; only the stack driver stacks them

The user, after PR 57 landed on CR-123's branch and on reading "each CR on the one under it":
"ca va pas du tout, en mode stack, les CR sont fait en paralleles contre la tete du projet (main)
puis stacker par le stack driver une , sauf si le foreman juge qu'il sera plus efficace de les
mettre a la chaine quand meme, avec une justification debrayable par l'utilisateur. mais en
parallel, elle ne peuvent pas se referencer l'une sur l'autre. Revoie les impacts sur le design,
fait moi revoir et met ca dans le batch en cours"

Found while reviewing the impacts:

- PR 56 (CR-122, e640710) already starts a CR on the default branch, in a stack too. Batch-06 did
  not get it: the plugin reads the main checkout, which stood at a75972e, four commits behind
  origin/main, so its Drivers ran the old rule and CR-123, 124, 125 and 126 stood on each other.
- `batch.json` holds no `after` on a live CR and no `depends.json` exists: nothing needed that chain.
- `ship` still records `_stack_base`, the place in the stack, before any stack exists: the record
  says another CR's branch while the forge says main.
