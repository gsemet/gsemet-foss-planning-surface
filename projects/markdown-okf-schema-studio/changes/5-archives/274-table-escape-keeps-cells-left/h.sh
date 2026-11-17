#!/bin/sh
P=/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/3-requests/274-table-escape-keeps-cells-left
sh $P/hdr.sh "$@" >/dev/null
sed -i '' '1s/cr-driver-274/driver-274-r/' $P/STATUS.md
