import sys, collections, pathlib, os
sys.path.insert(0, sys.argv[1])
from chantier.costs.sessions import transcript_state
home = pathlib.Path.home() / '.claude' / 'projects'
for pat in ('*/*/subagents/agent-*.jsonl', '*/*.jsonl'):
    c = collections.Counter(); ex = {}
    for f in home.glob(pat):
        st, why = transcript_state(f)
        key = (st, why[:70] if st != 'ended' else '')
        c[key] += 1; ex.setdefault(key, f)
    print(pat)
    for k, v in c.most_common():
        print('  ', v, k, ex[k] if k[0] != 'ended' else '')
