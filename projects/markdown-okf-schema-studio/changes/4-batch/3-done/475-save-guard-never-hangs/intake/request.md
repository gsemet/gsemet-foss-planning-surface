# No edit stays on Saving Markdown for good

Part B of the split of blank-run-edit-stuck-saving (issue 485): a general save guard. Every final save ends in success or a shown error after a 10 s limit; frontmatter saves bounded until close or error; neutral timeout message; Cancel always closes the editor, the save goes on.