"""Round 10: print the rows whose quoted rule matches a pattern.

Run: python -I find.py <regex> [<home regex>]
"""

import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from inv import rows  # noqa: E402


def main():
    pattern = re.compile(sys.argv[1])
    home = re.compile(sys.argv[2]) if len(sys.argv) > 2 else None
    for _, _, row in rows():
        if pattern.search(row["behaviour"]) and (home is None or home.search(row["new home"])):
            print(f"{row['id']} [{row['kind']}] -> {row['new home']} :: {row['behaviour'][:170]}")


if __name__ == "__main__":
    main()
