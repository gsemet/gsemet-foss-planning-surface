# Before / after, CR-341

After head: ade7512bc413e5278f2042207142f9b8be230e5e. No before captured (no detached worktree of the base):
the brief asked for the after screenshots only. Reproduce: `uv run --with playwright python -I work/scratch/shoot.py <worktree> <evidence folder>` (the script builds its own scratch surface, which is no longer kept).

- ../../evidence/home-open-prs-row-hovered.png: Home "Open PRs", row CR-143 (GitLab MR) hovered; the address bar is a drawn overlay of the row's real href (a headless browser has no status bar).
- ../../evidence/side-panel-facts-and-links.png: side panel of CR-142, facts row with `#14`, 04-links.md fixture drawn with its links.
Paths are made up (`/home/demo/...`); the images were opened and show no username or home folder.
