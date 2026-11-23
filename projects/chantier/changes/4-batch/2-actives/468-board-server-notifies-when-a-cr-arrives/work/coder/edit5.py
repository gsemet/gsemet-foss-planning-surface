p='scenario/run_scenario.py'
s=open(p,encoding='utf-8',newline='').read()
def rep(old,new):
    global s
    old=old.replace(chr(10),chr(13)+chr(10)); new=new.replace(chr(10),chr(13)+chr(10))
    assert s.count(old)==1,(old,s.count(old))
    s=s.replace(old,new)
rep('''        folders_text = ", ".join(by)
        written = f"journal: seq 1 issue@1''','''        folders_text = ", ".join(by)
        base = len(journal.read_text(encoding="utf-8").splitlines())  # the filings' `arrived@1` lines
        written = f"journal: seq {base + 1} issue@1''')
rep('out == ["journal: already there (seq 1)"]','out == [f"journal: already there (seq {base + 1})"]')
rep('''        code, remote = sw.chantier("status", "--batch", batch)
        _, local''','''        sw.chantier("status", "--batch", batch)  # tells the arrivals once: `status` moves the told mark
        code, remote = sw.chantier("status", "--batch", batch)
        _, local''')
open(p,'w',encoding='utf-8',newline='').write(s)
