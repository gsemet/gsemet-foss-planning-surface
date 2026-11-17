#!/bin/sh
# usage: hdr.sh status step round head pr run next question
C=/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/3-requests/293-table-keyboard-row-add-discoverable
printf 'driver: stack-driver · updated: %s\nstatus: %s · step: %s · round: %s\nhead: %s · PR: %s · run: %s\nnext: %s · question: %s\n' "$(date +%H:%M)" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" > $C/STATUS.md
