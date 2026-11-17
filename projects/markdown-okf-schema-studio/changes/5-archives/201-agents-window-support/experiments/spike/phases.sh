#!/usr/bin/env bash
R=$1; PORT=$2
EXPR='({edit:[...doc.querySelectorAll("button")].filter(x=>/edit mode/i.test(x.getAttribute("aria-label")||"")).map(x=>x.getAttribute("aria-disabled")+" | "+x.title)[0], head:(doc.querySelector("h1")||{}).textContent})'
phases=(phase-1-opened-no-folder phase-2-folder-mounted phase-3-opened-after-mount phase-4-folder-unmounted)
for n in 1 2 3 4; do
  f="$R/${phases[$((n-1))]}.json"
  for i in $(seq 1 60); do [ -f "$f" ] && break; sleep 1; done
  echo "== ${phases[$((n-1))]}"
  [ -f "$f" ] || { echo "timeout"; cat "$R/error.json" 2>/dev/null; exit 1; }
  node -e 'const p=require(process.argv[1]);console.log(JSON.stringify({folders:p.folders,tabs:p.tabs.map(t=>t.label+":"+(t.viewType?"studio":t.kind))}))' "$f"
  node inspect.mjs "$PORT" "$EXPR"
  [ $n -lt 4 ] && touch "$R/go-$n"
done
