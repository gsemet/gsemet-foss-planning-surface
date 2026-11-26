"""Every `topic <name>`, `topics <a>, <b>` and `help <name>` of the inventories and of
cards-next names a topic of `topics.json`, not a reading file. With `--apply`, a reading file
named as a topic in an inventory is replaced by the topic that holds it."""

import json
import re
import sys
from pathlib import Path

CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
EV = Path(__file__).resolve().parents[2] / "evidence"
INDEX = json.loads((CN / "topics.json").read_text(encoding="utf-8"))["topics"]
NAME = r"[a-z][a-z0-9]*(?:-[a-z0-9]+)+|[a-z]{4,}"


def files_of(readings) -> list[str]:
    out = []
    for reading in readings:
        out.extend(reading.values() if isinstance(reading, dict) else [reading])
    return out


HOLDERS: dict[str, list[str]] = {}
for topic, data in INDEX.items():
    for path in files_of(data["readings"]):
        stem = re.sub(r"(-p\d+)?\.md$", "", path.removeprefix("topics/"))
        HOLDERS.setdefault(stem, []).append(topic)


def main() -> None:
    apply = "--apply" in sys.argv
    unknown: dict[str, int] = {}
    pattern = re.compile(rf"(?<![\w-])(topics? |help )({NAME})(?![\w-])")
    for path in sorted(EV.glob("cards-inventory-*.md")):
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")
        count = 0

        def swap(match: re.Match) -> str:
            nonlocal count
            lead, name = match.groups()
            if name in INDEX or name not in HOLDERS:
                if name not in INDEX and "-" in name:
                    unknown[f"{path.name}: {lead}{name}"] = unknown.get(f"{path.name}: {lead}{name}", 0) + 1
                return match.group(0)
            top = min(HOLDERS[name], key=len)
            count += 1
            print(f"{path.name}: {lead}{name} -> {lead}{top} (held by {HOLDERS[name]})")
            return lead + top

        result = pattern.sub(swap, text)
        if apply and count:
            bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
            path.write_bytes(bom + result.encode("utf-8"))
        print(path.name, count, "replaced" if apply else "to replace")
    for path in sorted(CN.rglob("*.md")):
        for match in re.finditer(r"help ([a-z][a-z0-9]*(?:-[a-z0-9]+)+)", path.read_text(encoding="utf-8")):
            if match.group(1) not in INDEX:
                key = f"{path.relative_to(CN).as_posix()}: help {match.group(1)}"
                unknown[key] = unknown.get(key, 0) + 1
    print("unknown names:")
    for key, value in sorted(unknown.items()):
        print(" ", key, value)


main()
