import sys, importlib.util, socket
from pathlib import Path
src = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-30-CR-456\scenario\run_scenario.py")
sys.path.insert(0, str(src.parent))
spec = importlib.util.spec_from_file_location("rs", src)
rs = importlib.util.module_from_spec(spec); sys.modules["rs"] = rs
spec.loader.exec_module(rs)
import argparse
rs.ARGS = argparse.Namespace(forge="github", verbose=True, keep=False, unit=None, jobs=1)
with socket.socket() as s:
    s.bind(("127.0.0.1", 0)); F = s.getsockname()[1]
import chantier.board.address as a
a.DEFAULT_PORT = F
orig = rs.SurfaceWorld.build
def build(self):
    orig(self)
    (self.surface / "chantier.yaml").write_text(f"board:\n  port: {F}\n", encoding="utf-8")
rs.SurfaceWorld.build = build
rs.UNITS["one"] = (300, ["github"], ["serve_and_webui"])
out = Path(sys.argv[1]); out.mkdir(exist_ok=True)
print("rc", rs.run_unit("one", "github", out))
