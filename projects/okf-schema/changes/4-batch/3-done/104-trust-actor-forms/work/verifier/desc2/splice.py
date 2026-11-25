"""Compose verify.md: this pass's header, then the first pass's claims from "State and gates" on."""

from pathlib import Path

here = Path(__file__).parent
target = here.parents[1] / "verify.md"
old = target.read_text(encoding="utf-8")
(here / "verify-pass1.md").write_text(old, encoding="utf-8", newline="\n")
carried = old[old.index("## State and gates") :]
header = (here / "header.md").read_text(encoding="utf-8")
note = (
    "---\n\n# Carried from the first pass (carried from 7a33d92: no move of the head or the base)\n\n"
    "Its full text, failed claims D1 and D2 included, is `verifier/desc2/verify-pass1.md`.\n\n"
)
target.write_text(header + note + carried, encoding="utf-8", newline="\n")
print(target.read_text(encoding="utf-8").splitlines()[0])
