# Before / after

Before SHA: 5717626d (detached worktree, removed). After SHA: f1792cd79ce23802e6b7213eb7fbc8477bdf5f87.

- Pair 1: node-before.log / node-after.log. Shows renderMarkdown output on six inputs; the front matter list disappears for plain, BOM and CRLF inputs. Reproduce: `uvx --from nodejs-wheel==24.19.0 node ../probe.mjs <path to markdown.js>`.
- Pair 2 (board panel screenshot, captioned f1792cd): not captured. Serving the board needs a background process, which the Verifier card forbids. Both captures are missing, no image kept.
