import argparse, sys
from pathlib import Path
sys.path.insert(0, "scenario")
import run_scenario as rs
rs.UNITS["surface-board"] = (710, ["github"], ["remote_cli"])
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
rs.ARGS = argparse.Namespace(unit=None, forge="github", jobs=1, keep=False, verbose=False, child="surface-board", out=str(out))
sys.exit(rs.main())
