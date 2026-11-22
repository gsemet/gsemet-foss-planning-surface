# chantier scenario, unit one on github: 1/3 checks passed

- Run: 2026-11-22 15:18:16, 48.9 s
- Workspace: `C:\Users\gaeta\AppData\Local\Temp\cs-one-xcxbao3_` (removed)


## 16d1. `chantier serve` and `chantier webui`; two surfaces' servers on one machine
    $ chantier --project demo init  → exit 0
      created projects/demo/changes/1-inbox
      created projects/demo/changes/2-backlog
      created projects/demo/changes/3-ready
      created projects/demo/changes/4-batch/1-pending
      created projects/demo/changes/4-batch/2-actives
      created projects/demo/changes/4-batch/3-done
      created projects/demo/changes/5-archives
      created projects/demo/changes/6-trash
    $ chantier --project demo init  → exit 0
      created projects/demo/changes/1-inbox
      created projects/demo/changes/2-backlog
      created projects/demo/changes/3-ready
      created projects/demo/changes/4-batch/1-pending
      created projects/demo/changes/4-batch/2-actives
      created projects/demo/changes/4-batch/3-done
      created projects/demo/changes/5-archives
      created projects/demo/changes/6-trash
- [ ] a second surface's server, with the default port held by the first, prints the `board: port ... takes port <n>` line, then its start line on another port — None None
- [ ] serve_and_webui ran to the end — ConnectionRefusedError: [WinError 10061] Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée
Traceback (most recent call last):
  File "C:\Users\gaeta\Projets\chantier.worktrees\batch-30-CR-456\scenario\run_scenario.py", line 11386, in run_unit
    CASES[name](w)
    ~~~~~~~~~~~^^^
  File "C:\Users\gaeta\Projets\chantier.worktrees\batch-30-CR-456\scenario\run_scenario.py", line 2726, in serve_and_webui
    got1 = fetch(link.port, "/api/board", headers=link.cookie)
  File "C:\Users\gaeta\Projets\chantier.worktrees\batch-30-CR-456\scenario\run_scenario.py", line 1688, in fetch
    conn.request(method, path, body, headers or {})
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\gaeta\scoop\persist\uv\python\versions\cpython-3.15-windows-x86_64-none\Lib\http\client.py", line 1398, in request
    self._send_request(method, url, body, headers, encode_chunked)
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\gaeta\scoop\persist\uv\python\versions\cpython-3.15-windows-x86_64-none\Lib\http\client.py", line 1444, in _send_request
    self.endheaders(body, encode_chunked=encode_chunked)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\gaeta\scoop\persist\uv\python\versions\cpython-3.15-windows-x86_64-none\Lib\http\client.py", line 1393, in endheaders
    self._send_output(message_body, encode_chunked=encode_chunked)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\gaeta\scoop\persist\uv\python\versions\cpython-3.15-windows-x86_64-none\Lib\http\client.py", line 1153, in _send_output
    self.send(msg)
    ~~~~~~~~~^^^^^
  File "C:\Users\gaeta\scoop\persist\uv\python\versions\cpython-3.15-windows-x86_64-none\Lib\http\client.py", line 1097, in send
    self.connect()
    ~~~~~~~~~~~~^^
  File "C:\Users\gaeta\scoop\persist\uv\python\versions\cpython-3.15-windows-x86_64-none\Lib\http\client.py", line 1063, in connect
    self.sock = self._create_connection(
                ~~~~~~~~~~~~~~~~~~~~~~~^
        (self.host,self.port), self.timeout, self.source_address)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\gaeta\scoop\persist\uv\python\versions\cpython-3.15-windows-x86_64-none\Lib\socket.py", line 883, in create_connection
    raise exceptions[0]
  File "C:\Users\gaeta\scoop\persist\uv\python\versions\cpython-3.15-windows-x86_64-none\Lib\socket.py", line 868, in create_connection
    sock.connect(sa)
    ~~~~~~~~~~~~^^^^
ConnectionRefusedError: [WinError 10061] Aucune connexion n’a pu être établie car l’ordinateur cible l’a expressément refusée

- [x] chantier wrote nothing outside the planning folder (`git status` shows only .agents/changes/)

## Timing

| case or section | seconds | commands |
| --- | ---: | ---: |
| build | 0.5 | 8 |
| serve_and_webui | 48.2 | 40 |
| total of the rows | 48.7 | 48 |
| whole unit | 48.9 | 50 |
