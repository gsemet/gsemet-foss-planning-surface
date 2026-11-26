"""Round 10: of the given rows, which are not word for word in their home files.

Run: python -I verbatim.py <home file> <id> [<id> ...]
Prints each row whose quoted rule is not a substring of the home file, and each clause of it
that is not; a row printed is read by hand.
"""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from audit import flat, home_text  # noqa: E402
from inv import rows  # noqa: E402


def plain(text):
    return re.sub(r"[`*]", "", flat(text)).replace("\\|", "|").lower()


def main():
    home = plain(home_text([sys.argv[1]]))
    wanted = sys.argv[2:]
    by_id = {r["id"]: r for _, _, r in rows()}
    same = 0
    for i in wanted:
        text = plain(by_id[i]["behaviour"]).rstrip(" .;:,")
        if text.rstrip(" …") in home:
            same += 1
            continue
        parts = [p.strip(" .;:,…") for p in re.split(r"(?<=[.;:])\s+|[()]|, ", text)]
        lost = [p for p in parts if len(p) > 3 and p not in home]
        print(f"{i} -> {by_id[i]['new home']}")
        for p in lost:
            print("    -", p)
    print(f"word for word: {same} of {len(wanted)}")


if __name__ == "__main__":
    main()
