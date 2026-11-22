import sys, importlib.util, socket, time, argparse, os, tempfile
from pathlib import Path
src = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-30-CR-456\scenario\run_scenario.py")
sys.path.insert(0, str(src.parent))
spec = importlib.util.spec_from_file_location("rs", src)
rs = importlib.util.module_from_spec(spec); sys.modules["rs"] = rs
spec.loader.exec_module(rs)
rs.ARGS = argparse.Namespace(forge="github", verbose=False, keep=False, unit=None, jobs=1)
with socket.socket() as s:
    s.bind(("127.0.0.1", 0)); F = s.getsockname()[1]
tmp = Path(tempfile.mkdtemp(prefix="dbg-"))
cfg = tmp/"gitconfig"; cfg.write_text("[user]\n\tname = s\n\temail = s@e.com\n")
os.environ["GIT_CONFIG_GLOBAL"] = str(cfg)
a = rs.SurfaceWorld(tmp/"a"); a.root.mkdir(); a.build(); a.chantier("init")
t0=time.monotonic()
extra = sys.argv[1:]
first = rs.BoardProc(a,"--project","demo","serve","--host","127.0.0.1","--port",F,*extra,cwd=a.surface)
print("first", first.line(), first.line())
for i in range(12):
    time.sleep(1)
    if first.p.poll() is not None:
        print("exited", first.p.poll(), "after", round(time.monotonic()-t0,1)); print(first.p.stderr.read()); break
else: print("alive at 12s")
first.stop()
