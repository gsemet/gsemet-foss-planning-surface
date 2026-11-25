"""Read-only: host-and-shared home counts of each file given, and the rows whose home class
differs between the first and the last.

Run: python -I homecount.py <inventory> [<inventory> ...]
"""

import collections
import pathlib
import re
import sys

KINDS = (
    "card ",
    "topic ",
    "`topic",
    "host row",
    "inferable",
    "floor",
    "proof file",
    "incidents file",
    "refusal",
    "facts",
)


def homes(path):
    found = {}
    for line in pathlib.Path(path).read_text(encoding="utf-8").split("\n"):
        cells = re.split(r"(?<!\\)\|", line.rstrip("\r"))
        if len(cells) == 10 and re.fullmatch(r"\s*H-\d+\s*", cells[1]):
            found[cells[1].strip()] = (cells[7].strip(), cells[6].strip())
    return found


def klass(home):
    return next((k.strip() for k in KINDS if home.startswith(k)), "?")


def main():
    tables = [homes(path) for path in sys.argv[1:]]
    for path, table in zip(sys.argv[1:], tables):
        counts = collections.Counter(klass(home) for home, _ in table.values())
        print(path, len(table), counts.most_common())
        print("  ?", [(k, v[0]) for k, v in table.items() if klass(v[0]) == "?"][:10])
    first, last = tables[0], tables[-1]
    for key, (home, kind) in last.items():
        if klass(first[key][0]) != klass(home):
            print(key, kind, first[key][0], "->", home)


if __name__ == "__main__":
    main()
