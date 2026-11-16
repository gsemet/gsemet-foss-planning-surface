"""Run named functions of scenario/run_scenario.py on a fresh World (a subset, not the full gate).
Usage: python subset_runner.py <repo root> <github|gitlab> <function>..."""
import argparse
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

root = Path(sys.argv[1])
forge = sys.argv[2]
names = sys.argv[3:]
spec = importlib.util.spec_from_file_location("rs", root / "scenario" / "run_scenario.py")
rs = importlib.util.module_from_spec(spec)
sys.modules["rs"] = rs
spec.loader.exec_module(rs)
rs.ARGS = argparse.Namespace(forge=forge, external_only=False, keep=False, verbose=False)
tmp = Path(tempfile.mkdtemp(prefix="chantier-subset-"))
w = rs.World(tmp)
try:
    w.build()
    for n in names:
        w.env.pop("CHANTIER_BATCH", None)
        getattr(rs, n)(w)
except Exception:
    traceback.print_exc()
finally:
    subprocess.run(["git", "worktree", "prune"], cwd=w.work, capture_output=True)
    shutil.rmtree(tmp, ignore_errors=True)
print(rs.CHECKS)

