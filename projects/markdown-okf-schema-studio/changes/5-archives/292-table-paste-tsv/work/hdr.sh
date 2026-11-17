#!/bin/sh
# usage: hdr.sh status step round head pr run next question
F=/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/3-requests/292-table-paste-tsv
T=$(date +%H:%M)
{
printf 'driver: stack-driver · updated: %s\n' "$T"
printf 'status: %s · step: %s · round: %s/3\n' "$1" "$2" "$3"
printf 'head: %s · PR: %s · run: %s\n' "$4" "$5" "$6"
printf 'next: %s · question: %s\n' "$7" "$8"
sed -n '5,$p' "$F/STATUS.md"
} > "$F/STATUS.md.new" && mv "$F/STATUS.md.new" "$F/STATUS.md"
