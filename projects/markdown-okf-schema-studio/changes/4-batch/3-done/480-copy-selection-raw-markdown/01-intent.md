# Copy a selection as the exact raw Markdown under it

Owner, 2026-11-23: "quand je sélectionne du texte ça copie pas exactement le texte dessous (par exemple les triple tirets ou des tables etc). Le but c'est que du point de départ au point en dessous le texte brut y compris le formatage est conservé."

Intent: a native mouse or keyboard selection in Studio copies, as plain text, the raw Markdown source from the source position under the selection's start to the one under its end, formatting included (thematic breaks, tables, emphasis, directives). Today the page has no copy handler: the browser copies the rendered text. Only the edit mode's block selection (Shift+click, whole blocks) already copies source lines through the host.
