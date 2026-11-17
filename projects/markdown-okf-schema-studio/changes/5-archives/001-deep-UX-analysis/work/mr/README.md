# MR package: deep UX fixes for Markdown OKF-Schema Studio

Everything needed to open the merge request once you are back on the internal network. Nothing
here has been pushed or created.

| File | What it is |
| --- | --- |
| `MR.md` | The MR title (first line) and description, with before/after images |
| `images/` | 12 screenshots that `MR.md` references by relative path |
| `SQUASH-COMMIT.txt` | The message of the squashed commit (already used) |
| `COST-REPORT.md` | The full cost report; `MR.md` has its summary |
| `cost2.py`, `cost_tables.py`, `assemble_cost.py` | Scripts that produced the cost report from the local transcripts |

## State of the branch

- `dev/gsemet-deep-ux-analysis` is **one commit**, `7d560d1`, on top of `1a5f8d8`. It squashes the
  43 commits from `aeb9c03` to `7a21a2b`. The tree is identical to `7a21a2b`.
- The 43 original commits are kept on the local branch
  `backup/dev-gsemet-deep-ux-analysis-pre-squash`. Delete it once the MR is merged:
  `git branch -D backup/dev-gsemet-deep-ux-analysis-pre-squash`.
- The branch has never been pushed and has no upstream.
- Your uncommitted changes to `.agents/skills/markdown-studio-exploratory-qa-claude/` and
  `.agents/thinking/` are untouched and **not** in the commit.

## Open the MR

GitLab does not render the local `images/…` paths, so upload the images first and rewrite the
links.

```bash
cd .agents/changes/requests/deep-UX-analysis/mr

# 1. Push the branch.
git push -u origin dev/gsemet-deep-ux-analysis

# 2. Upload the images and build a description with GitLab links.
HOST=gitlabee.dt.renault.com
PROJECT=swlabs%2Fnestor%2Fagentic%2Fagentic-coding-white-paper
cp MR.md MR.gitlab.md
for f in images/*; do
  md=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" --form "file=@$f" \
    "https://$HOST/api/v4/projects/$PROJECT/uploads" | python3 -c 'import json,sys; print(json.load(sys.stdin)["url"])')
  python3 - "$f" "$md" <<'EOF'
import sys
old, new = sys.argv[1], sys.argv[2]
text = open("MR.gitlab.md").read().replace(f"]({old})", f"]({new})")
open("MR.gitlab.md", "w").write(text)
EOF
done

# 3. Create the MR (title = first heading of MR.md, description = the rest).
glab mr create \
  --source-branch dev/gsemet-deep-ux-analysis --target-branch master \
  --title "$(head -1 MR.gitlab.md | sed 's/^# //')" \
  --description "$(tail -n +3 MR.gitlab.md)"
```

`MR.md` points to `COST-REPORT.md` "next to this description". After creating the MR, attach
`COST-REPORT.md` as a comment, or upload it like the images and link it.
