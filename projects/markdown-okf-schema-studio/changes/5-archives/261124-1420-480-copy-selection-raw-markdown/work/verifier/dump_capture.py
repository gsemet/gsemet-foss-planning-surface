"""Runs the raw copy capture check and dumps each copy it made (taken, plain, html) as JSON."""
import json, sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "test", "visual"))
import capture_raw_copy as m
import capture
out = sys.argv[1]
rec = []
orig = m._copy
def wrapped(page, source, start, end):
    r = orig(page, source, start, end)
    rec.append({"start": start, "end": end, "browserSelectionText": page.evaluate("window.getSelection().toString()"), "defaultPrevented": r["taken"], "text/plain": r["plain"], "text/html": r["html"]})
    return r
m._copy = wrapped
sys.argv = ["capture.py", "--scenario", "block-editing/v55-raw-copy-light-900"]
try:
    code = capture.main()
finally:
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
sys.exit(code)
