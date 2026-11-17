#!/bin/zsh
# commit.sh <Txx> <msgfile>: stage task files explicitly (never -A); README.md and CHANGELOG.md
# are staged hunk by hunk, leaving out the user's own uncommitted edits.
set -e
cd /Users/az02065/Projects/DevTools/markdown-okf-schema-studio
S=/private/tmp/claude-502/-Users-az02065-Projects-Nestor-agentic-coding-white-paper/dd375646-4450-4e52-a643-89ff1d9e405a/scratchpad
filtered=(README.md CHANGELOG.md)
files=(${(f)"$(git diff --name-only | grep -v -x -e README.md -e CHANGELOG.md || true)"})
untracked=(${(f)"$(git ls-files --others --exclude-standard | grep -v '^\.agents/' || true)"})
echo "tracked: ${files[*]}"; echo "untracked: ${untracked[*]}"
[[ ${#files[@]} -gt 0 && -n "${files[1]}" ]] && git add -- "${files[@]}"
[[ ${#untracked[@]} -gt 0 && -n "${untracked[1]}" ]] && git add -- "${untracked[@]}"
for f in $filtered; do
  git diff --quiet -- $f && continue
  rtk proxy git diff -U0 -- $f >| $S/hunks-full.patch
  python3 - "$S" "$f" <<'PY'
import sys,re
S,f=sys.argv[1],sys.argv[2]; t=open(S+'/hunks-full.patch').read()
head,*hunks=re.split(r'(?m)^(?=@@ )',t)
user=('Linked-File Annotations','TODO: add frontmatter example','<!-- TODO: read back);','OKF-Schema supports `x-okf-link`')
keep=[h for h in hunks if not any(u in h for u in user)]
print(f, 'hunks', len(hunks), 'task hunks', len(keep))
open(S+'/hunks-task.patch','w').write(head+''.join(keep) if keep else '')
PY
  [[ -s $S/hunks-task.patch ]] && git apply --cached --unidiff-zero $S/hunks-task.patch
done
git diff --cached --stat | tail -3
git commit -q -F "$2"
git rev-parse --short HEAD
git status --short
