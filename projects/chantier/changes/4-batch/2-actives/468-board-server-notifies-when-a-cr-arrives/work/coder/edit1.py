p='scenario/run_scenario.py'
s=open(p,encoding='utf-8',newline='').read()
a=s.index("def forge_hub(w: World)")
b=s.index("def two_keys(")
f=s[a:b]
def rep(old,new,count=1):
    global f
    old=old.replace(chr(10),chr(13)+chr(10)); new=new.replace(chr(10),chr(13)+chr(10))
    assert f.count(old)==count,(old,f.count(old))
    f=f.replace(old,new)
rep('''    def journal(project: str = "demo") -> list[dict]:
        path''','''    def journal(project: str = "demo", raw: bool = False) -> list[dict]:
        """The project's journal lines, but the `arrived@1` lines of the setup unless `raw`."""
        path''')
rep('''                whole.append(json.loads(x))
        return whole''','''                whole.append(json.loads(x))
        return whole if raw else [e for e in whole if e.get("type") != "arrived@1"]''')
rep('''    board_port(sw)
    before =''','''    board_port(sw)
    sw.chantier("status", expect=None)  # tells the setup's arrivals: the told mark moves
    base = len(journal(raw=True))  # the journal's length past the setup's `arrived@1` lines
    base_b = len(journal("other", raw=True))
    before =''')
rep('out[-1] == no_watcher(0)','out[-1] == no_watcher(base)')
rep('sw.chantier("watch", "--after", 5, expect=1)','sw.chantier("watch", "--after", base + 5, expect=1)')
rep('start.startswith("watch: demo from cursor 0 for project")','start.startswith(f"watch: demo from cursor {base} for project")')
rep('start_b.startswith("watch: other from cursor 0")','start_b.startswith(f"watch: other from cursor {base_b}")')
rep('x.endswith(" watch --once --after 0")','x.endswith(f" watch --once --after {base}")')
rep('got == [says(a[0], 910, "2026-11-16T10:00:00Z"), cursor(1)]','got == [says(a[0], 910, "2026-11-16T10:00:00Z"), cursor(base + 1)]')
rep('== [(2, 1, "hub", ["project"], "merged@1", a[0])]','== [(2, base + 1, "hub", ["project"], "merged@1", a[0])]')
rep('out[-1] == no_watcher(1)','out[-1] == no_watcher(base + 1)')
rep('wa = watcher("demo", "--after", 1)\n        wg = watcher("demo", "--after", 1, "--for", "role:griller")','wa = watcher("demo", "--after", base + 1)\n        wg = watcher("demo", "--after", base + 1, "--for", "role:griller")')
rep('start_g.startswith("watch: demo from cursor 1 for project")','start_g.startswith(f"watch: demo from cursor {base + 1} for project")')
rep('start.startswith("watch: demo from cursor 1")','start.startswith(f"watch: demo from cursor {base + 1}")')
rep('                      cursor(3)], str(got))','                      cursor(base + 3)], str(got))')
rep('wa = watcher("demo", "--after", 3)','wa = watcher("demo", "--after", base + 3)')
rep('got == [red, cursor(4)]','got == [red, cursor(base + 4)]')
rep('[(5, "board", a[4])]','[(base + 5, "board", a[4])]')
rep('wa = watcher("demo", "--after", 4)','wa = watcher("demo", "--after", base + 4)')
rep('cursor(5)], str(got))','cursor(base + 5)], str(got))')
rep('wa = watcher("demo", "--after", 5)','wa = watcher("demo", "--after", base + 5)')
rep('got[1] == cursor(6)','got[1] == cursor(base + 6)')
rep('sw.chantier("watch", "--once", "--after", 5)','sw.chantier("watch", "--once", "--after", base + 5)')
rep('''("watch: cursor 6; next, at the user's next message: "
                             f"{cli_form} watch --once --after 6")''','''(f"watch: cursor {base + 6}; next, at the user's next message: "
                             f"{cli_form} watch --once --after {base + 6}")''')
rep('wa = watcher("demo", "--after", 6)','wa = watcher("demo", "--after", base + 6)')
rep("watch=f\"{cli_of('other')} watch --after 1\")","watch=f\"{cli_of('other')} watch --after {base_b + 1}\")")
s=s[:a]+f+s[b:]
open(p,'w',encoding='utf-8',newline='').write(s)
