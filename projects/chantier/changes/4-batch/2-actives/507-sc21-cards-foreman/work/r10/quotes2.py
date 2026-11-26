"""The host-and-shared end table `| id | source | new home | the home line |`: is the quoted
home line still a line of a named home, and is it the home its main row names? With `--apply`,
a quote that no longer stands is replaced by the current line of the home that shares most words."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import inv  # noqa: E402

CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
EV = Path(__file__).resolve().parents[2] / "evidence"
PATH = EV / "cards-inventory-host-and-shared.md"
HEAD = "| id | source | new home | the home line |"
SPLIT = re.compile(r"(?<!\\)\|")


def norm(text: str) -> str:
    return " ".join(text.replace("\\|", "|").split())


def home_lines(home: str) -> list[tuple[str, str]]:
    out = []
    for card, line in re.findall(r"card ([\w./-]+\.md):(\d+)", home):
        path = CN / card
        if path.exists():
            lines = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
            out.extend((card, text) for text in lines)
    for part in re.findall(r"topics? ([\w ,-]+)", home):
        for name in re.findall(r"[\w-]+", part):
            for path in sorted((CN / "topics").glob(f"{name}*.md")):
                if re.fullmatch(rf"{re.escape(name)}(-p\d+)?\.md", path.name):
                    lines = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
                    out.extend((path.name, text) for text in lines)
    for card in re.findall(r"(?<!card )\b([\w-]+\.md):\d+", home):
        path = CN / card
        if path.exists():
            lines = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
            out.extend((card, text) for text in lines)
    if "floor" in home:
        lines = (CN / "floor.md").read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
        out.extend(("floor.md", text) for text in lines)
    return out


def words(text: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[A-Za-z<>-]{4,}", text)}


def main() -> None:
    apply = "--apply" in sys.argv
    raw = PATH.read_bytes()
    lines = raw.decode("utf-8-sig").split("\n")
    main_homes = {}
    for line in lines[: next(i for i, t in enumerate(lines) if t.strip() == HEAD)]:
        parts = [p.strip() for p in SPLIT.split(line)]
        if len(parts) >= 9 and re.fullmatch(r"[A-Z]+-B?\d+", parts[1]):
            main_homes[parts[1]] = parts[7]
    inside, seen, stale, moved = False, 0, 0, 0
    for i, line in enumerate(lines):
        if line.strip() == HEAD:
            inside = True
            continue
        if inside and not line.startswith("|"):
            inside = False
        if not inside or line.startswith("|--") or line.startswith("| --"):
            continue
        parts = [p.strip() for p in SPLIT.split(line)]
        ident, home, quote = parts[1], parts[3], "|".join(parts[4:-1]).strip()
        if not ident or ident.startswith("-"):
            continue
        seen += 1
        want = main_homes.get(ident, home)
        if want != home:
            moved += 1
        pool = home_lines(want)
        bare = norm(quote.removesuffix("...").removesuffix("…").strip())
        pieces = [p.strip() for p in bare.split(" / ") if p.strip()]
        ok = bool(pieces) and all(any(p in norm(text) for _, text in pool) for p in pieces)
        if ok and want == home:
            continue
        if ok:
            new = quote
        else:
            stale += 1
            if not pool:
                print(f"{ident} line {i + 1}: no readable home: {want} | {quote[:80]}")
                continue
            target = words(quote)
            card, best = max(pool, key=lambda p: len(words(p[1]) & target) / (len(words(p[1]) | target) or 1))
            best = best.strip()
            cut = best if len(best) <= 200 else best[:200].rsplit(" ", 1)[0] + " ..."
            new = cut.replace("\\|", "|").replace("|", "\\|")
            print(f"{ident} line {i + 1} [{want}]\n  was: {quote[:150]}\n  now ({card}): {new[:150]}")
        lines[i] = f"| {ident} | {parts[2]} | {want} | {new} |"
    print(f"{seen} rows, {stale} quotes not in their home, {moved} homes differ from the main table")
    if apply:
        bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
        PATH.write_bytes(bom + "\n".join(lines).encode("utf-8"))


main()
