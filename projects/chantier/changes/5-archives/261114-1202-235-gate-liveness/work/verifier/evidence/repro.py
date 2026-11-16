import os, subprocess, sys, time, tempfile, pathlib, types
sys.path.insert(0, "skills/chantier/scripts/cli/src")
from chantier import procs
from chantier.commands import gate_lock as gl
p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
now = time.time()
print("live proc, file written after it started:", procs.alive_since(p.pid, now, False))
print("live proc, file written 10s before it started (reused pid):", procs.alive_since(p.pid, now-10, False))
q = subprocess.Popen([sys.executable, "-c", "pass"]); q.wait()
print("dead pid:", procs.alive_since(q.pid, now, False))
d = pathlib.Path(tempfile.mkdtemp()); (d/".long-gate.queue").mkdir()
repo = types.SimpleNamespace(changes=d)
def tk(name, cr, pid, back=0):
    f=d/".long-gate.queue"/name; f.write_text(f"{cr} pid {pid}")
    if back: t=time.time()-back; os.utime(f,(t,t))
(d/".long-gate.lock").write_text(f"\0CR-3 pid {q.pid} pg{p.pid}"); t=time.time()-10; os.utime(d/".long-gate.lock",(t,t))
tk("1-a","CR-2",os.getpid()); tk("2-b","CR-4",os.getpid(), back=0)
print("lock names dead pid + reused pg: CR-3 ->", gl.gate_state(repo,"CR-3"))
print("CR-2 ->", gl.gate_state(repo,"CR-2"))
(d/".long-gate.lock").write_text(f"\0CR-3 pid {os.getpid()}")
print("live holder: CR-3 ->", gl.gate_state(repo,"CR-3"), "| CR-2 ->", gl.gate_state(repo,"CR-2"), "| CR-4 ->", gl.gate_state(repo,"CR-4"))
(d/".long-gate.lock").write_text("")
print("empty lock: CR-2 ->", gl.gate_state(repo,"CR-2"), "| CR-4 ->", gl.gate_state(repo,"CR-4"))
tk("3-c","CR-5",q.pid); print("dead ticket: CR-5 ->", gl.gate_state(repo,"CR-5"), "ticket kept:", (d/".long-gate.queue"/"3-c").exists())
p.kill()

