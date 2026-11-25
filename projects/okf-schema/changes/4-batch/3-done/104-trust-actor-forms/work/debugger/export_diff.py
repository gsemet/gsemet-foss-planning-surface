"""List files of an exported copy that differ from the archive it came from.

Usage: python export_diff.py <archive.tar> <extracted folder>
"""

import os
import sys
import tarfile

SKIP_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "htmlcov",
    "_build",
}
SKIP_FILES = {".coverage", "coverage.xml", "coverage.json"}


def main() -> None:
    """Print changed, line-end-only, removed and new files."""
    archive_path, root = sys.argv[1], sys.argv[2]
    with tarfile.open(archive_path) as archive:
        original = {
            member.name: archive.extractfile(member).read()
            for member in archive.getmembers()
            if member.isfile()
        }
    for name, before in sorted(original.items()):
        path = os.path.join(root, name)
        if not os.path.isfile(path):
            print("removed      ", name)
            continue
        with open(path, "rb") as handle:
            after = handle.read()
        if after != before:
            eol_only = after.replace(b"\r\n", b"\n") == before.replace(b"\r\n", b"\n")
            print("line-end only" if eol_only else "changed      ", name)
    for folder, dirs, files in os.walk(root):
        dirs[:] = [item for item in dirs if item not in SKIP_DIRS]
        for item in files:
            name = os.path.relpath(os.path.join(folder, item), root).replace("\\", "/")
            if name not in original and item not in SKIP_FILES:
                print("new          ", name)
    pointers = sorted(
        name
        for name, data in original.items()
        if data.startswith(b"version https://git-lfs.github.com/spec/")
    )
    print(f"files in archive: {len(original)}; unresolved LFS pointers: {pointers or 'none'}")


if __name__ == "__main__":
    main()
