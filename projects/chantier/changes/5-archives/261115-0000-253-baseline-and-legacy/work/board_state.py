"""Print project_state of one project, time fields removed. argv: id, cwd-or-project, surface(0/1)."""
import json, sys
from pathlib import Path
from chantier.core.repo import Repo
from chantier.board.state import project_state

pid, where, surface = sys.argv[1], sys.argv[2], sys.argv[3] == "1"
if surface:
    repo = Repo.find(Path(where).parent.parent, project=where)
else:
    repo = Repo.find(Path(where))
st = project_state(pid, repo, surface, None)
TIME = {"now", "read_at", "read", "at_read"}


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in TIME}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


print(json.dumps(strip(st), indent=1, sort_keys=True, default=str))
