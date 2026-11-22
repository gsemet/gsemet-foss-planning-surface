No before/after pair captured: the change is protocol behaviour, proved by the commands in ../../verify.md at
53a134e6e2804387be6ae43ae24b06bab5c836c6. The before (base main) has no `read_key`, no `read-only:` line.
Reproduce: init a scratch git repo, `chantier serve --port 8799 --host 127.0.0.1`, then POST
/api/v1/call/<op> with header x-chantier-board-key set to `read_key` from .git/chantier/server.json.
