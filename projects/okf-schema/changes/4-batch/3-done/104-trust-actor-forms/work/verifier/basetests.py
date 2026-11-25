"""Run the head's changed test files against the base source tree (argv[1])."""

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])

import pytest  # noqa: E402

import okf_schema  # noqa: E402

where = Path(okf_schema.__file__).as_posix()
if "/scratch/ver/b/src/" not in where:
    raise SystemExit("unexpected module location: " + where)
print("module under test: base src (2f09cef)")
head = Path("C:/Users/gaeta/Projets/okf-schema.worktrees/batch-01-CR-104")
names = ["test_okf2_compliance.py", "test_api.py", "test_cli_remaining.py", "test_kb_scaffold.py"]
code = pytest.main(
    ["-q", "--no-header", "--tb=no", "-rf", "-o", "addopts=", "-p", "no:cacheprovider",
     "--rootdir", str(head), "-c", str(head / "pyproject.toml")]
    + [str(head / "tests" / name) for name in names]
)
print("pytest exit:", int(code))
