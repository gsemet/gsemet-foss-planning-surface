## Summary

Pasting a web address into a block editor now does what people expect: over selected text it makes
a link, on its own it makes an autolink, and an image address inserts an image. Rich-text paste and
image-file paste are unchanged.

## Deliverables

| Paste (plain text) | Result in the source |
| --- | --- |
| URL over selected text | `[text](url)` |
| URL alone | `<url>` |
| Image URL (`.png .jpg .jpeg .gif .svg .webp`) | `![](url)` (`![text](url)` over a selection) |
| Cmd/Ctrl+Shift+V | the address as it is |

Only `http:`, `https:` and `mailto:` are handled; inside code, inside a link target and for any
other scheme the paste stays plain text. Only the pasted span of the source changes.

Before / after, cream theme:

| Before | After |
| --- | --- |
| ![before link](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5a555cfccc0e4778d4c95c14ae1676f7b14d0d19/before-cream-1-link.png) | ![after link](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5a555cfccc0e4778d4c95c14ae1676f7b14d0d19/after-cream-1-link.png) |
| ![before image](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5a555cfccc0e4778d4c95c14ae1676f7b14d0d19/before-cream-2-image.png) | ![after image](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5a555cfccc0e4778d4c95c14ae1676f7b14d0d19/after-cream-2-image.png) |
| ![before autolink](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5a555cfccc0e4778d4c95c14ae1676f7b14d0d19/before-cream-3-autolink.png) | ![after autolink](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5a555cfccc0e4778d4c95c14ae1676f7b14d0d19/after-cream-3-autolink.png) |

Dark theme:

| Before | After |
| --- | --- |
| ![before link](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5a555cfccc0e4778d4c95c14ae1676f7b14d0d19/before-dark-1-link.png) | ![after link](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5a555cfccc0e4778d4c95c14ae1676f7b14d0d19/after-dark-1-link.png) |
| ![before image](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5a555cfccc0e4778d4c95c14ae1676f7b14d0d19/before-dark-2-image.png) | ![after image](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5a555cfccc0e4778d4c95c14ae1676f7b14d0d19/after-dark-2-image.png) |
| ![before autolink](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5a555cfccc0e4778d4c95c14ae1676f7b14d0d19/before-dark-3-autolink.png) | ![after autolink](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/5a555cfccc0e4778d4c95c14ae1676f7b14d0d19/after-dark-3-autolink.png) |

## Autonomous decisions

- A lone URL pasted without a selection becomes `<url>` (autolink form).
- An image URL over a selection keeps the selection as alt text: `![text](url)`.
- Scheme limit (http, https, mailto) follows the existing link-scheme rule.
- Cmd/Ctrl+Shift+V raw paste is covered by a unit test only; it could not be driven in a real window.

## Internal references

CR 145 (paste-url-as-link); requirement PALETTE-003.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
