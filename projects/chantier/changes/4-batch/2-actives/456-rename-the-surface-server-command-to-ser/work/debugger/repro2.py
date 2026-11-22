import sys, importlib.util, socket, time, argparse
from pathlib import Path
src = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-30-CR-456\scenario\run_scenario.py")
sys.path.insert(0, str(src.parent))
spec = importlib.util.spec_from_file_location("rs", src)
rs = importlib.util.module_from_spec(spec); sys.modules["rs"] = rs
spec.loader.exec_module(rs)
rs.ARGS = argparse.Namespace(forge="github", verbose=True, keep=False, unit=None, jobs=1)
import tempfile
with socket.socket() as s:
    s.bind(("127.0.0.1", 0)); F = s.getsockname()[1]
tmp = Path(tempfile.mkdtemp(prefix="dbg-"))
import os
cfg = tmp/"gitconfig"; cfg.write_text("[user]\n\tname = s\n\temail = s@e.com\n")
os.environ["GIT_CONFIG_GLOBAL"] = str(cfg)
w = rs.World(tmp)
sws = []
for n in ("a","b"):
    sw = rs.SurfaceWorld(tmp/n); sw.root.mkdir(); sw.build(); sw.chantier("init")
    (sw.surface/"chantier.yaml").write_text(f"board:\n  port: {F}\n"); sws.append(sw)
a,b = sws
first = rs.BoardProc(a,"--project","demo","serve","--host","127.0.0.1","--port",F,"--seat","sess-1",cwd=a.surface)
print("first", first.line()); print("first2", first.line())
time.sleep(2); print("first poll", first.p.poll())
second = rs.BoardProc(b,"--project","demo","serve","--host","127.0.0.1","--seat","sess-2",cwd=b.surface)
print("second", second.line(), second.line())
time.sleep(2)
print("polls", first.p.poll(), second.p.poll())
for n,p in (("first",first),("second",second)):
    if p.p.poll() is not None: print(n,"stderr:", p.p.stderr.read())
first.stop(); second.stop()
