"""Make work/r9/records.py from work/r8/records.py (round 9's wording). Round 9 changed no role
card, no quiz case and no `roles.yaml` line, so the brief log stays round 8's and the quiz plan
round 7's."""

from pathlib import Path

R9 = Path(__file__).parent
src = (R9.parent / "r8/records.py").read_text(encoding="utf-8")


def swap(old: str, new: str, count: int = 1) -> None:
    global src
    assert src.count(old) == count, (old, src.count(old))
    src = src.replace(old, new)


swap('(HERE / "briefs8.log")', '(HERE.parent / "r8/briefs8.log")')
swap("plus the uncommitted changes of rounds 7 and 8 unless",
     "plus the uncommitted changes of rounds 7 to 9 unless")
swap("LF bytes of the brief file:",
     "LF bytes of the brief file (round 8's run: round 9 changed no role card, and `brief` reads no topic):")
swap("`just check` on round 8's working tree", "`just check` on round 9's working tree")
(R9 / "records.py").write_text(src, encoding="utf-8", newline="\n")
print("written")
