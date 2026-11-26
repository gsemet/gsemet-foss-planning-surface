"""usage: changedtests.py <worktree> <base> <head> : head test cases with a changed non-comment line."""
import re, subprocess, sys

wt, base, head = sys.argv[1:4]
VIEWER = 'test/site/requirementsViewer/'
FILES = ['test/build/checkMarkers.test.ts', 'test/build/mutationReport.test.ts'] + [
    VIEWER + n + '.test.ts' for n in ('model', 'home', 'pages', 'write', 'mainPaths')]


def git(*args):
    return subprocess.run(['git', '-C', wt, *args], capture_output=True, check=True).stdout.decode('utf-8')


for f in FILES:
    lines = git('show', head + ':' + f).split('\n')
    touched = set()
    for m in re.finditer(r'^@@ -\S+ \+(\d+)(?:,(\d+))? @@', git('diff', '-U0', base, head, '--', f), re.M):
        start, count = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
        touched.update(range(start, start + count))
    spans, current = [], None
    for number, line in enumerate(lines, 1):
        if re.match(r'(test|it)\(', line):
            title = re.match(r'(?:test|it)\(\s*(["\'`])(.*?)\1', line)
            current = [title.group(2) if title else '(line %d)' % number, number, None]
            if re.search(r'\}\);\s*$', line):
                current[2] = number
                spans.append(current)
                current = None
        elif current and re.match(r'\}\);', line):
            current[2] = number
            spans.append(current)
            current = None
    code = [n for n in sorted(touched)
            if lines[n - 1].strip() and not lines[n - 1].strip().startswith('//')]
    inside = {t: [n for n in code if a <= n <= b] for t, a, b in spans}
    covered = {n for ns in inside.values() for n in ns}
    print(f)
    for t, ns in inside.items():
        if ns:
            print('    changed test:', t, ns)
    print('    changed lines outside any test:', [n for n in code if n not in covered])
