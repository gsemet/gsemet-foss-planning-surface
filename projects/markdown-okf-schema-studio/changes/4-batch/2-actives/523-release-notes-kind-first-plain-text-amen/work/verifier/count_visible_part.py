import re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
t = subprocess.run(["git","show","HEAD:docs/releases-notes/2026-11-24-v1.12.1/release-notes.md"],capture_output=True,check=True).stdout.decode("utf-8")
vis = t[:t.index("<details")]
vis = re.sub(r"<a [^>]*>.*?</a>","",vis,flags=re.S)   # links not counted
vis = re.sub(r"<[^>]+>","",vis)                        # HTML tags not counted
tok = [x for x in vis.split() if x not in ("##","-","---")]
w = [x for x in tok if re.search(r"\w",x)]
print("words holding a letter or digit:", len(w))
print("every whitespace token (markup markers excluded):", len(tok), [x for x in tok if not re.search(r"\w",x)])
