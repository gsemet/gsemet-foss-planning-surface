# Side preview scroll follows only the real-file side of a diff

Known limits left by CR-455 (side-preview-diff-gaps): only the real file side of a diff scrolls the side preview; the inline diff layout is untested; a staged or timeline diff has no scroll following (its real-window test T6 was dropped as the owner's fallback 'Livrer le reste'). Evidence in CR-455's folder and PR #466.