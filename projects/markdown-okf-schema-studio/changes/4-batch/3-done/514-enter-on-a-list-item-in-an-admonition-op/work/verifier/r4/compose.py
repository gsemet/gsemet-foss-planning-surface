# Writes <work>/verify.md: the claims judged in this pass, then the claims of the first verdict at
# the same head, carried with their commands and outputs. Usage: python -I compose.py <work folder>
import pathlib
import re
import sys

work = pathlib.Path(sys.argv[1])
first = (work / "verify-f9dc2c6-first.md").read_text(encoding="utf-8")
judged = (work / "verifier/r4/judged.md").read_text(encoding="utf-8")


def between(start, end):
    return first[first.index(start):first.index(end)]


claims = between("## Claims that hold", "## Files that may be attached")
claims = claims[claims.index("### "):]
REASON = "carried from f9dc2c6: same head, and none of the description text it judges changed (claim D0)."
SPECIAL = {
    "### The other Known gaps": "carried from f9dc2c6: same head; every bullet but the three of D1 to D3 is "
    "unchanged (claim D0). The observation at its end is replaced by D3.",
    "### PR description form": "carried from f9dc2c6: same head; the template, diagram and name checks stand "
    "(claim D0: only three bullets changed). The posted body and its length are judged again in D4.",
}


def mark(match):
    title = match.group(0)
    reason = next((text for key, text in SPECIAL.items() if title.startswith(key)), REASON)
    return f"{title}\n\n_{reason}_"


claims = re.sub(r"^### .*$", mark, claims, flags=re.MULTILINE)
claims = claims.replace("VERIFIED apart from C", "VERIFIED (the sentence failed as C is judged in D1)")
files = between("## Files that may be attached", "## Limits")
limits = between("## Limits", "\nNOT VERIFIED")
extra = (
    "- This pass: the three bullets were judged through the real renderer, page helpers, cursor model and\n"
    "  `PreviewManager` at the head; the base side of \"as before this change\" is carried from the base logs\n"
    "  of the first verdict (no base build of mine in this pass).\n"
)
out = judged.rstrip() + "\n\n## Carried claims\n\n" + claims + files + limits.rstrip() + "\n" + extra + "\nVERIFIED\n"
(work / "verify.md").write_text(out, encoding="utf-8", newline="\n")
print(len(out.splitlines()), "lines")
