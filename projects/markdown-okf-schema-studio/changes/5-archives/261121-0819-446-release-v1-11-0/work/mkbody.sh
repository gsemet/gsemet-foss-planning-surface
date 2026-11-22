set -e
cd C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-07-CR-446
W=C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/446-release-v1-11-0/work
dir=docs/releases-notes/2026-11-21-v1.11.0
base="https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/$(git rev-parse HEAD)/$dir"
rewrite() { sed -E -e "s#(\]\(|src=\")([^/\":)]+\.(png|jpe?g|gif))#\1$base/\2#g" -e "s#^Image: ([^ /]+\.(png|jpe?g|gif))\$#Image: ![\1]($base/\1)#" "$1"; }
{ cat $W/body-sections.md
  printf '\n---\n\n# 📰 Release notes (rendered)\n\n'; rewrite "$dir/release-notes.md"
  printf '\n---\n\n# 🐦 Announcement thread (rendered, a draft the owner posts themselves)\n\n'; rewrite "$dir/tweet.md"
  printf '\n---\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n'
} > $W/pr-body.md
