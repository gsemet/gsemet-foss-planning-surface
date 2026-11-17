# Before and after: the picker's surface item

Before: base 33a23059dc9bcb9e0416500d82001b92f20a7481 (detached worktree, removed). After: head 18d82a0e26550d7eda4028fac290702ef76ea440.

Reproduce: `uv run --no-project --with playwright python -I work/verifier/check.py <head worktree> <code root> <label> <out>` on the demo planning surface copy (docs/demo, 3 projects), real Chromium, surface path rewritten to a made-up one.

- `before-picker-pc.png`, `before-picker-phone.png`: the open menu on a project's Kanban page at base: caption "PLANNING SURFACE · 3 PROJECTS", the surface as a plain first row.
- `after-picker-pc.png`, `after-picker-phone.png`: same at head: header (grid icon, name, grey "overview · 3 projects"), separator, indented projects with regular names.

Kanban page used so no local path shows behind the menu. No username or home folder shows in the four images (looked at each).
