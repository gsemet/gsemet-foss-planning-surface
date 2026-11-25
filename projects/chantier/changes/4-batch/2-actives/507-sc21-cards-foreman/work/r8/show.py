import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "r7"))
from inv import NAMES, rows
want = set(sys.argv[1].split(","))
for name in NAMES:
    for i, d in rows(name):
        if d["id"] in want:
            print(f'{d["id"]}:{i} [{d.get("kind")}] home={d.get("new home")} | chk={d.get("check")}\n  B: {d.get("behaviour","")[:260]}')
