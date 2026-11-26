# usage: python -I percommit.py <worktree> <scratch dir> <base> <old base> <commit>...
# Extracts each commit into a scratch git repository, runs that commit's own marker check,
# and tells for each failing line which commit wrote it (before or after the old base).
import sys, os, re, io, subprocess, tarfile, shutil, stat, collections

W, S, base, old = sys.argv[1:5]
commits = sys.argv[5:]


def git(*args, binary=False):
    r = subprocess.run(['git', '-C', W, *args], capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode('utf-8', 'replace')


def is_ancestor(a, b):
    return subprocess.run(['git', '-C', W, 'merge-base', '--is-ancestor', a, b]).returncode == 0


def remove(path):
    def force(fn, p, _):
        os.chmod(p, stat.S_IWRITE)
        fn(p)
    if os.path.exists(path):
        shutil.rmtree(path, onerror=force)


seen = {}
sets = {}
for c in commits:
    d = S + '/c'
    remove(d)
    os.makedirs(d)
    subprocess.run(['git', 'init', '-q', d], check=True)
    data = git('archive', c, 'requirements', 'src', 'sphinx', 'skills', 'scripts', 'test', 'package.json', 'esbuild.mjs', binary=True)
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        t.extractall(d)
    shutil.copytree(W + '/node_modules/yaml', d + '/node_modules/yaml')
    r = subprocess.run(['node', d + '/scripts/check-marker-companions.mjs', '--root', d], capture_output=True)
    out = (r.stdout + r.stderr).decode('utf-8', 'replace')
    fails = re.findall(r'^\s*(\S+?):(\d+): ([a-z-]+): (@\w+) (\S+)', out, re.M)
    rules = collections.Counter(f[2] for f in fails)
    print('==', c, 'check exit', r.returncode, 'failing lines', len(fails), dict(rules))
    if not fails:
        print('   last output:', out.strip().splitlines()[-1][:200] if out.strip() else '(none)')
    sets[c] = collections.Counter((f[0].replace(chr(92), '/').split('/vg/c/')[-1], f[4]) for f in fails)
    print('   files', len({k[0] for k in sets[c]}), 'requirements', sorted({k[1][-10:] for k in sets[c]}))
    for path, line, rule, marker, req in fails:
        rel = path.replace('\\', '/')
        if rel.startswith(d + '/'):
            rel = rel[len(d) + 1:]
        key = (rel, line, req)
        if key not in seen:
            b = git('blame', '-l', '-s', '-L', line + ',' + line, c, '--', rel)
            sha = b.split()[0].lstrip('^')
            origin = 'before old base' if is_ancestor(sha, old) else ('from main after old base' if is_ancestor(sha, base) else 'branch commit')
            seen[key] = (sha[:8], origin, b.split(')', 1)[1].strip() if ')' in b else '')
    remove(d)

print('== origin of the failing lines', dict(collections.Counter(v[1] for v in seen.values())))
print('distinct failing lines', len(seen))
failing = [s for s in sets.values() if s]
print('failing commits', len(failing), 'identical sets', all(s == failing[0] for s in failing))
per_file = collections.defaultdict(list)
for (rel, line, req), v in seen.items():
    per_file[rel].append((int(line), req.replace('SwRS-MDOKFSTUDIO-', ''), v[0], v[1]))
for rel, items in sorted(per_file.items()):
    items.sort()
    print(rel, len(items), sorted({i[1] for i in items}), sorted({(i[2], i[3]) for i in items}))
