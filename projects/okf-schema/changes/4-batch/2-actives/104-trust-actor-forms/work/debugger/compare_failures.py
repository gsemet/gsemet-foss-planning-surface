"""Compare the failure signature of each failed test between two pytest logs.

Usage: python compare_failures.py <head log> <base log>

A signature is the test file line that raised plus the final exception line, with the
per-run temporary folder numbers removed.
"""

import re
import sys

HEADER = re.compile(r"^_{3,} (test_\w+) _{3,}$")
LOCATION = re.compile(r"^(tests\\\S+\.py:\d+): ?(\w*)")


def signatures(path: str) -> dict[str, tuple[str, int, str]]:
    """Return test name -> (raising test line, 1314 flag, exception text)."""
    with open(path, "rb") as handle:
        raw = handle.read()
    found: dict[str, tuple[str, int, str]] = {}
    name = None
    location = ""
    errors: list[str] = []
    for line in raw.decode("utf-8", errors="replace").splitlines() + ["____ test_end ____"]:
        header = HEADER.match(line)
        if header or line.startswith(("====", "---- ")):
            if name:
                text = " ".join(errors)
                text = re.sub(r"pytest-\d+", "pytest-N", text)
                text = re.sub(r"popen-gw\d+", "popen-gwX", text)
                # The localized Windows message depends on the log's encoding.
                text = re.sub(r"\[WinError 1314\] [^:]+:", "[WinError 1314]:", text)
                found[name] = (location, int("WinError 1314" in text), text)
            name = header.group(1) if header else None
            location, errors = "", []
            continue
        match = LOCATION.match(line)
        if match:
            location = match.group(1)
        if line.startswith("E "):
            errors.append(line[1:].strip())
    return found


def main() -> None:
    """Print one comparison row per failed test and a verdict."""
    head, base = signatures(sys.argv[1]), signatures(sys.argv[2])
    print(f"failed: head {len(head)}, base {len(base)}, same names: {set(head) == set(base)}")
    identical = 0
    for name in sorted(set(head) | set(base)):
        left, right = head.get(name), base.get(name)
        same = left == right
        identical += same
        shown = left or right
        print(f"{'same' if same else 'DIFF'} | {shown[0]} | 1314={shown[1]} | {name}")
    print(f"identical signatures: {identical}/{len(set(head) | set(base))}")


if __name__ == "__main__":
    main()
