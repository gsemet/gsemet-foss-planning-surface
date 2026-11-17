#!/bin/sh
# usage: hdr.sh status step round head pr run next question
S=/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/3-requests/288-export-single-html/STATUS.md
rest=$(tail -n +5 "$S" 2>/dev/null)
{
  printf 'driver: stack-driver · updated: %s\n' "$(date +%H:%M)"
  printf 'status: %s · step: %s · round: %s/3\n' "$1" "$2" "$3"
  printf 'head: %s · PR: %s · run: %s\n' "$4" "$5" "$6"
  printf 'next: %s · question: %s\n' "$7" "$8"
  if [ -n "$rest" ]; then printf '%s\n' "$rest"; fi
} > "$S.new"
cat "$S.new" > "$S"
rm -f "$S.new" "$S.tmp"
