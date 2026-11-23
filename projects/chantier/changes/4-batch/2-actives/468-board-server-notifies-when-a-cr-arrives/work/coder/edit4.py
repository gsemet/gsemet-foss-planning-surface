p='scenario/run_scenario.py'
s=open(p,encoding='utf-8',newline='').read()
def rep(old,new):
    global s
    old=old.replace(chr(10),chr(13)+chr(10)); new=new.replace(chr(10),chr(13)+chr(10))
    assert s.count(old)==1,(old,s.count(old))
    s=s.replace(old,new)
rep('''    try:
        link = Link(bp.line())
        code, _, view = op(link.port, link, "config.get", {"project": "demo"})''','''    w.chantier("status", expect=None)  # tells the filings' arrivals: the told mark moves
    journal_file = w.project / "changes" / "forge-journal.jsonl"
    base = len(journal_file.read_text(encoding="utf-8").splitlines()) if journal_file.is_file() else 0
    try:
        link = Link(bp.line())
        code, _, view = op(link.port, link, "config.get", {"project": "demo"})''')
rep('''        lines = [json.loads(x) for x in (w.project / "changes" / "forge-journal.jsonl")
                 .read_text(encoding="utf-8").splitlines()]''','''        lines = [e for e in (json.loads(x) for x in journal_file.read_text(encoding="utf-8").splitlines())
                 if e["type"] != "arrived@1"]''')
rep('== [(1, "board", "config@1", "hosts.claude.roles.coder.model")]','== [(base + 1, "board", "config@1", "hosts.claude.roles.coder.model")]')
rep('got == [told, cursor(2)]','got == [told, cursor(base + 2)]')
rep('"watch", "--after", 2, cwd=w.surface, env=quick)','"watch", "--after", base + 2, cwd=w.surface, env=quick)')
rep('specifying.parallel 4 -> 1", cursor(3)]','specifying.parallel 4 -> 1", cursor(base + 3)]')
open(p,'w',encoding='utf-8',newline='').write(s)
