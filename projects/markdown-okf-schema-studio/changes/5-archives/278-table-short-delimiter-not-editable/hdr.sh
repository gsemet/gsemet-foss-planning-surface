#!/bin/sh
# usage: hdr.sh status step round head pr run next question
P=/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/3-requests/278-table-short-delimiter-not-editable
printf 'driver: driver-278 · updated: %s\nstatus: %s · step: %s · round: %s\nhead: %s · PR: %s · run: %s\nnext: %s · question: %s\n' "$(date +%H:%M)" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" > $P/STATUS.md
