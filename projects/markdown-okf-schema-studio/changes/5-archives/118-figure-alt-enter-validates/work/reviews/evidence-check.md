before-shot matches user evidence: yes

- The user's evidence (image.png) shows the inline source editor with `![alt](path)` and the alt text selected; the complaint is that Enter replaces that selection with a newline.
- before-enter-dark.png and before-enter-cream.png show the result of that Enter: the alt is gone and the source reads `![` / newline / `](image-1.png)`, with the footer hint "Enter: new line", so the symptom reproduces.
- Caveats: the shots show the state after Enter, not the selected-alt state before it; the evidence uses a light editor background while the shots use the dark and cream themes. The symptom does not depend on the theme.
