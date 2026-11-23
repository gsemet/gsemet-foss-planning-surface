p='scenario/run_scenario.py'
s=open(p,encoding='utf-8',newline='').read()
old='''        if not link.ok:
            note(f"    the default port {DEFAULT_PORT} is held by another program here: "
                 "the second-surface step is skipped")
'''.replace(chr(10),chr(13)+chr(10))
new='''        if not link.ok:
            note(f"    the default port {DEFAULT_PORT} is held by another program here: "
                 "the second-surface step is skipped; the first server takes a free port")
            first.stop()
            first = BoardProc(sw, "--project", "demo", "serve", "--host", "127.0.0.1", "--port",
                              free_port(), cwd=sw.surface)
            procs.append(first)
            link = Link(first.line())
'''.replace(chr(10),chr(13)+chr(10))
assert s.count(old)==1
s=s.replace(old,new)
open(p,'w',encoding='utf-8',newline='').write(s)
