"""usage: oldcode.py <worktree> <scratch dir> <base> <head>

Runs the head's compiled new or changed tests twice in a scratch copy: first with the head's code
(control), then with the base's code under test. Nothing is written in the worktree.
"""
import io, os, re, shutil, subprocess, sys, tarfile

wt, scratch, base, head = sys.argv[1:5]
root = os.path.join(scratch, 'r')
VIEWER = 'test/site/requirementsViewer/'
TESTS = ['build/checkMarkers', 'build/mutationReport'] + [
    'site/requirementsViewer/' + n for n in ('model', 'home', 'pages', 'write', 'mainPaths')]


def git(*args):
    return subprocess.run(['git', '-C', wt, *args], capture_output=True, check=True).stdout


if os.path.exists(scratch):
    sys.exit('scratch exists: ' + scratch)
os.makedirs(root)
tar = git('archive', head, 'scripts', 'package.json', VIEWER.rstrip('/'), 'test/shared')
tarfile.open(fileobj=io.BytesIO(tar)).extractall(root, filter='data')
for part in ('test', 'src'):
    source = os.path.join(wt, 'out', part)
    if os.path.isdir(source):
        shutil.copytree(source, os.path.join(root, 'out', part),
                        ignore=shutil.ignore_patterns('*.map', '*.png', 'integration'))
# the marker script is an ES module: NODE_PATH does not reach its yaml import
shutil.copytree(os.path.join(wt, 'node_modules', 'yaml'), os.path.join(root, 'node_modules', 'yaml'))
env = dict(os.environ, NODE_PATH=os.path.join(wt, 'node_modules'))


def run(label):
    for name in TESTS:
        r = subprocess.run(['node', '--test', '--test-reporter=tap', 'out/test/' + name + '.test.js'],
                           cwd=root, env=env, capture_output=True, text=True, encoding='utf-8')
        out = r.stdout
        counts = {k: re.findall(r'^# %s (\d+)' % k, out, re.M) for k in ('tests', 'pass', 'fail')}
        print(label, name, 'exit', r.returncode, {k: (v[-1] if v else None) for k, v in counts.items()})
        for line in re.findall(r'^not ok \d+ - (.*)$', out, re.M):
            print('    not ok:', line)


run('HEAD-CODE')

changed = git('diff', '--name-only', base, head, '--', VIEWER, 'scripts').decode().split()
replaced = [f for f in changed if not f.endswith('.test.ts') and f != VIEWER + 'fixture.ts']
print('code under test taken from the base:', replaced)
esbuild = os.path.join(wt, 'node_modules', 'esbuild')
for f in replaced:
    exists = subprocess.run(['git', '-C', wt, 'cat-file', '-e', base + ':' + f], capture_output=True).returncode == 0
    if not exists:
        print('    not on the base (kept):', f)
        continue
    data = git('show', base + ':' + f)
    with open(os.path.join(root, f), 'wb') as fh:
        fh.write(data)
    if f.endswith('.ts'):
        js = subprocess.run(
            ['node', '-e', 'const e=require(process.argv[1]);let s="";process.stdin.setEncoding("utf8");'
             'process.stdin.on("data",d=>s+=d).on("end",()=>process.stdout.write('
             'e.transformSync(s,{loader:"ts",format:"cjs",target:"es2022"}).code))', esbuild],
            input=data, capture_output=True, check=True).stdout
        with open(os.path.join(root, 'out', f[:-3] + '.js'), 'wb') as fh:
            fh.write(js)

run('BASE-CODE')

print('--- test titles on added lines of the diff')
for name in TESTS:
    diff = git('diff', '-U0', base, head, '--', 'test/' + name + '.test.ts').decode('utf-8')
    added = [l[1:] for l in diff.split('\n') if l.startswith('+') and not l.startswith('+++')]
    code = [l for l in added if l.strip() and not l.strip().startswith('//')]
    titles = [m.group(1) for l in code for m in [re.match(r'\s*(?:test|it)\(\s*["\'`](.*?)["\'`],', l)] if m]
    print(name, 'added non-comment lines', len(code), 'new or retitled tests', titles)
