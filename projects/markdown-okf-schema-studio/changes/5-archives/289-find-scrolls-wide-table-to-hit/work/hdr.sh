#!/bin/sh
# usage: hdr.sh status step round head pr run next question  (driver fixed)
F=/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/3-requests/289-find-scrolls-wide-table-to-hit/STATUS.md
{ printf 'driver: stack-driver · updated: %s\n' "$(date +%H:%M)"
  printf 'status: %s · step: %s · round: %s\n' "$1" "$2" "$3"
  printf 'head: %s · PR: %s · run: %s\n' "$4" "$5" "$6"
  printf 'next: %s · question: %s\n' "$7" "$8"; } > "$F.new" && mv "$F.new" "$F"
