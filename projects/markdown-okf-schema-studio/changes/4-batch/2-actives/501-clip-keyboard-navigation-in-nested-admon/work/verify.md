Head: 3ea161ce58f3b53cfc4121a4cd0581f3082561e6

Description-only pass on PR 522 (posted text read with `gh pr view 522`).

- Clean render: sections, lists, inline GIF and links well formed; judged at 3ea161c. OK.
- Consistent with the diff: `gh pr diff 522 --name-only` lists the clip folder, docs/user/editing.md, kit tests (check, storyboard), test/site/siteClips.test.ts; no src/. Matches Changes. Judged at 3ea161c.
- Media pinned at 66b8478: `git diff --name-only 66b8478 3ea161c` prints only clip.md, so the media are unchanged (carried from 66b8478: only clip.md changed). GIF at 66b8478 resolves, size 1675368 bytes (1.60 MB as claimed).
- CI box: `gh pr checks 522`: checks, report, static, static-windows, viewer-graph, visual pass; others skipping. OK at 3ea161c.
- Known gaps present; Deviation and Autonomous decisions disclosed; Review box unticked (draft, owner approval pending), no STALE mark. Internal references only in the last section.
- Not checked: images' username/home look (not an evidence capture pass; frames not opened in this short pass).

VERIFIED
