"""Apply exact old/new replacements to cards-next files; each old must occur exactly once.

Run: python -I replace.py <cards-next folder> <pairs.json>
The JSON is a list of [file, old, new]. Line endings of the file are kept.
"""

import json
import pathlib
import sys


def main():
    root = pathlib.Path(sys.argv[1])
    pairs = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
    failed = 0
    touched = {}
    for name, old, new in pairs:
        path = root / name
        text = touched.get(path)
        if text is None:
            text = path.read_bytes().decode("utf-8")
        if "\r\n" in text:
            old = old.replace("\n", "\r\n")
            new = new.replace("\n", "\r\n")
        count = text.count(old)
        if count != 1:
            print("NOT APPLIED", name, count, old[:60])
            failed += 1
            continue
        touched[path] = text.replace(old, new)
    for path, text in touched.items():
        path.write_bytes(text.encode("utf-8"))
        size = len(text.replace("\r\n", "\n").encode("utf-8"))
        print(f"{path.relative_to(root).as_posix()}: {size} B")
    print("failed", failed)


if __name__ == "__main__":
    main()
