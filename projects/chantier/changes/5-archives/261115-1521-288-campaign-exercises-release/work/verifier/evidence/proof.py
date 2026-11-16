import sys, re
from pathlib import Path
sys.path.insert(0, "scripts")
import release_notes as rn
folder = Path("docs/release-notes/2026-11-13-v0.9.0")
base = (folder / "release-notes.md").read_text(encoding="utf-8")
print("0.9.0 notes has For contributors:", "For contributors" in base)
t = base.replace("0.9", "0.10", 1) if "0.9" in base.splitlines()[0] else base
print("title:", t.splitlines()[0])
# strip any existing bullet
nb = re.sub(r"^- \*\*Not exercised by an eval\.\*\*.*\n", "", t, flags=re.M)
def add(text, bullet):
    i = text.index("For contributors")
    j = text.index("</summary>", i) + len("</summary>")
    return text[:j] + "\n\n" + bullet + "\n" + text[j:]
cases = {
 "A no bullet, 0.10.0": (nb, "0.10.0"),
 "B claims bullet, 0.10.0": (add(nb, "- **Not exercised by an eval.** A pipeline job as long gate."), "0.10.0"),
 "C None form, 0.10.0": (add(nb, "- **Not exercised by an eval.** None: every change of this release came up in an eval run."), "0.10.0"),
 "D no bullet, 0.9.0": (nb, "0.9.0"),
 "E real 0.9.0 notes unchanged, 0.9.0": (base, "0.9.0"),
}
for k,(txt,v) in cases.items():
    try:
        rn.validate_notes(txt, folder, v); print(k, "-> accepted")
    except ValueError as e:
        print(k, "-> refused:", e)
