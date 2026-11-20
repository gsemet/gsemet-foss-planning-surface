Short name: `list-reorder`

# Answers (owner, 2026-11-20, Chief of Staff grill)

- Owner's words at filing: 'il faut mettre des ancre de reordonnement de la liste sur la gauche comme les ligne d une table'. Cmd/Ctrl+Alt+Up/Down in a list item editor keeps moving the whole list (CR-424).
- Nesting: an item moves with its sub-items and blocks, only among its siblings of the same list. (owner chose: 'Il emporte ses enfants')
- Where: owner's words: 'toutes les listes en mode edition' (bullet, ordered, task lists, every level; an ordered list keeps its numbering in order).
- Keyboard: the handle has a menu with move up / move down, like table rows. (owner chose: 'Oui, via le menu')
- Visibility: on hover, in edit mode only, like table row handles. (owner chose: 'Au survol en édition')
- Depends on CR-424 (PR 404, item-level list editing) being in its base.

## Second series (2026-11-20, spec open questions)

- Style, owner's words: 'je veux le meme comportement pour les listes et les poignee, mais ce menu c est quoi'. The list item handles behave exactly like the table row handles: same visibility (as the table handles, always shown in edit mode), no menu (the menu answer of the first series is replaced; the CoS explained the menu was only a proposed keyboard path, which Alt+Up/Down on the handle already gives). Table handles unchanged.
- Keyboard: Alt+Up/Down on a focused list item handle moves the item, as on a table row handle (SwRS-TABLE-002). (owner chose: 'Oui, comme les tables')
- Lists inside a GitHub alert or a MyST admonition (any nesting depth): handles too. Owner's words: 'alors on met partout, tu peux decaler les poignee en dehors de l admonition ou des n niveaux d admonition'. The handles may sit outside the admonition box, shifted left past the n nested admonition levels. (The CoS told the owner it is a rule of the extension, from CR-424, not a VS Code limit.)
