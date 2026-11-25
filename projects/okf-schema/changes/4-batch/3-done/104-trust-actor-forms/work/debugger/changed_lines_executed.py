"""Report which changed lines of validator.py the symlink tests executed.

Usage: python changed_lines_executed.py <coverage.json of a run limited to those tests>
"""

import json
import sys

# New-side line numbers of the base..head diff of src/okf_schema/validator.py.
CHANGED = {
    "module level (_ACTOR_RE)": range(64, 68),
    "_derive_trust_tier body": range(373, 399),
    "_validate_okf2_verified W10 block": range(627, 640),
}


def main() -> None:
    """Print executed lines per changed region and the executed test files."""
    with open(sys.argv[1], encoding="utf-8") as handle:
        files = json.load(handle)["files"]
    for name, data in files.items():
        if name.replace("\\", "/").endswith("okf_schema/validator.py"):
            executed = set(data["executed_lines"])
            for label, lines in CHANGED.items():
                hit = sorted(executed.intersection(lines))
                print(f"{label}: executed lines {hit or 'none'}")
            return
    print("validator.py not in the coverage report")


if __name__ == "__main__":
    main()
