import json
from chantier.board import key as keys, routes
from chantier.board.context import Context, Request
from chantier.board.projects import Projects
from chantier.board.seats import Seats
from chantier.core.repo import Repo
repo_ = Repo.find(readonly=True)
projects = Projects(repo_, repo_.surface, [])
PROJ = projects.home_id
secret = keys.load_or_create(repo_)
ctx = Context(projects, keys.KeyFile(keys.key_path(repo_)), Seats(projects), "t", lambda: None)
def call(method, route, body):
    head = {keys.HEADER: secret, "content-type": "application/json", "host": "board"}
    r = routes.handle(ctx, Request(method, f"/api/projects/{PROJ}/{route}", {}, head, json.dumps(body).encode()))
    return r.status
for r,b in [("backlog/new",{"text":"board idea"}),("backlog/move",{"items":["board-idea"],"to":"P2"}),
            ("backlog/move",{"items":["nonexistent-x"],"to":"P1"}),
            ("backlog/labels",{"items":["board-idea"],"add":"x"})]:
    print(r, b, "-> HTTP", call("POST", r, b))
