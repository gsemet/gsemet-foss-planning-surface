p='scenario/run_scenario.py'
s=open(p,encoding='utf-8',newline='').read()
a=s.index("def surface_server(w: World)")
b=s.index("def remote_board(w: World)")
f=s[a:b]
def rep(old,new):
    global f
    old=old.replace(chr(10),chr(13)+chr(10)); new=new.replace(chr(10),chr(13)+chr(10))
    assert f.count(old)==1,(old,f.count(old))
    f=f.replace(old,new)
rep('''    def journal() -> list[dict]:
        path = sw.state / "forge-journal.jsonl"
        return ([json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]
                if path.is_file() else [])
''','''    def journal(raw: bool = False) -> list[dict]:
        """The journal's lines, but the setup's `arrived@1` lines unless `raw`."""
        path = sw.state / "forge-journal.jsonl"
        found = ([json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]
                 if path.is_file() else [])
        return found if raw else [e for e in found if e["type"] != "arrived@1"]
''')
rep('''    sw.chantier("seat", "take", "sess-a")  # A's seat is this session's
    board_port(sw)
    try:''','''    sw.chantier("seat", "take", "sess-a")  # A's seat is this session's; tells the setup's arrivals
    base = len(journal(raw=True))  # the journal's length past the setup's `arrived@1` lines
    board_port(sw)
    try:''')
rep('start.startswith("watch: demo from cursor 0")','start.startswith(f"watch: demo from cursor {base}")')
rep('wa = watcher("--after", 1)','wa = watcher("--after", base + 1)')
rep('''start.startswith("watch: demo from "
                                                                                  "cursor 1")''','''start.startswith(
            f"watch: demo from cursor {base + 1}")''')
rep('`--after 1` subscribes','`--after` subscribes') if False else None
rep('[e["seq"] for e in journal()] == [1, 2]','[e["seq"] for e in journal()] == [base + 1, base + 2]')
rep('wi = watcher("--after", 2, env=short)','wi = watcher("--after", base + 2, env=short)')
rep('watch=f"{cli_form} watch --after 2")','watch=f"{cli_form} watch --after {base + 2}")')
s=s[:a]+f+s[b:]
open(p,'w',encoding='utf-8',newline='').write(s)
