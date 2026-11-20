Before (base 82c11a47): the requirements-lint recipe has no diagram parse; with Box in PALETTE-007 its four lines exit 0.
After (c749c3b5): same edit, `just requirements-lint` exits 1 naming the StRS file:79, the StRS id and "got 'box'". Output in ../verify.md claim 1.
Reproduce: replace Field by Box on lines 72 and 79 of StRS-MDOKFSTUDIO-PALETTE-007.md, run `just requirements-lint`, then git checkout the file. No images.
