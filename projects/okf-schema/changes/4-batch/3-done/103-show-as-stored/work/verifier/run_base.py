"""Run the head tests against the base sources (the base worktree), in-process and child."""

import os
import subprocess
import sys
from pathlib import Path

head = Path(sys.argv[1]).resolve()
base = Path(__file__).resolve().parent / "b"
for name in ("test_api.py", "test_cli_remaining.py"):
    (base / "tests" / name).write_bytes((head / "tests" / name).read_bytes())

env = dict(os.environ, PYTHONPATH=str(base / "src"), PYTHONDONTWRITEBYTECODE="1")
subprocess.run(
    [sys.executable, "-c", "import okf_schema; print('package under test:', okf_schema.__file__)"],
    cwd=base,
    env=env,
    check=True,
)
done = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_api.py", "tests/test_cli_remaining.py"]
    + ["--no-cov", "-p", "no:cacheprovider", "-o", "addopts=", "-q", "-rf", "--tb=no"],
    cwd=base,
    env=env,
)
print("pytest exit code:", done.returncode)
