p='scenario/run_scenario.py'
s=open(p,encoding='utf-8',newline='').read()
def rep(old,new):
    global s
    old=old.replace(chr(10),chr(13)+chr(10)); new=new.replace(chr(10),chr(13)+chr(10))
    assert s.count(old)==1,(old,s.count(old))
    s=s.replace(old,new)
rep('''    def forge_lines() -> list[dict]:
        path = w.state / "forge-journal.jsonl"
        return ([json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]
                if path.is_file() else [])

    slug = "board-inbox-item"
''','''    def forge_lines(raw: bool = False) -> list[dict]:
        """The journal's lines, but the `arrived@1` lines of the filings unless `raw`."""
        path = w.state / "forge-journal.jsonl"
        lines = ([json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]
                 if path.is_file() else [])
        return lines if raw else [e for e in lines if e["type"] != "arrived@1"]

    prior = len(forge_lines(raw=True))  # the filings' `arrived@1` lines come first
    slug = "board-inbox-item"
''')
rep('''and [e["seq"] for e in seen] == [1, 2, 3]''','''and [e["seq"] for e in seen] == [prior + 1, prior + 2, prior + 3]''')
open(p,'w',encoding='utf-8',newline='').write(s)
