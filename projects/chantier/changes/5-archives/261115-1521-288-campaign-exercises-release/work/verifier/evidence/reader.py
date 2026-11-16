import sys; sys.path.insert(0,"evals/kit")
import audit
rows = audit.scorecard_rows()
print("rows:", len(rows))
for r in rows:
    if r["id"] in ("C21","J27","J28","C6"): print(r["id"], "|", r["how"], "|", r["where"], "| cells ok")
ids=[r["id"] for r in rows]; print("dup ids:", len(ids)-len(set(ids)))
