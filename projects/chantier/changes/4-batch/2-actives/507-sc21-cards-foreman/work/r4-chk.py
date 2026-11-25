import re, sys
base = 'C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/'
def rows(p):
    t = open(p, encoding='utf-8', newline='').read()
    i = t.index("### A Driver's prompt")
    out = []
    for l in t[i:].split('\n')[1:]:
        if l.startswith('#'):
            break
        if l.startswith('|'):
            out.append(l)
    return out
a = rows(base + 'references/concepts.md')
b = rows(base + 'cards-next/concepts.md')
print([x.rstrip() for x in a] == b, len(a), len(b))
t = open(base + 'cards-next/concepts.md', encoding='utf-8').read()
for n in ('Words', 'Escalation'):
    m = re.search(r'^## ' + n + r'\n(.*?)(?=^#{1,2} )', t + '\n# x\n', re.S | re.M)
    print(n, len(m.group(1).encode()))
print(len(t.encode()))
