"""Run named scenario cases in one unit (a Coder's targeted run): python run_cases.py <out> <case>..."""

import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-476")
spec = importlib.util.spec_from_file_location("run_scenario", ROOT / "scenario" / "run_scenario.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["run_scenario"] = mod
spec.loader.exec_module(mod)
mod.ARGS = argparse.Namespace(forge="github", keep=False, verbose=True, jobs=1, unit=None, child=None,
                              out=None)
mod.UNITS["coder"] = (600, ["github"], sys.argv[2:])
sys.exit(mod.run_unit("coder", "github", Path(sys.argv[1])))
