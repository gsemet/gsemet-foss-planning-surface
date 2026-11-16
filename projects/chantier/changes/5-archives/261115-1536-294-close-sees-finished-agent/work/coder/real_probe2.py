import sys, pathlib, time, json
sys.path.insert(0, sys.argv[1])
from chantier.costs.sessions import transcript_state
home = pathlib.Path.home() / '.claude' / 'projects'
bad = 0
for f in home.glob('*/*/subagents/agent-*.jsonl'):
    st, why = transcript_state(f)
    txt = f.read_text(encoding='utf-8', errors='replace')
    used = '"name":"SubagentHandback"' in txt
    if st != 'ended':
        age = (time.time() - f.stat().st_mtime) / 3600
        print(st, 'handback-used' if used else 'no-handback', f'{age:.1f}h', why[:50], f.parent.parent.name[:8], f.stem)
        bad += used
print('running but used the hand-back tool:', bad)
