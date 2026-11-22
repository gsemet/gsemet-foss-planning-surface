p = r"C:\Users\gaeta\Projets\chantier.worktrees\batch-30-CR-452\skills\chantier\scripts\cli\tests\test_store_reads.py"
s = open(p, encoding="utf-8").read()
a = '    ("status/views.py", "_documents"): "a project file of the code repository, a spec\'s link",\n'
assert a in s
b = a + '''    ("gate_slots.py", "lock_text"): "a held OS lock file, read past its locked byte (spec 5.3)",
    ("rails.py", "worktree_print"): "a CR's worktree (is_dir, and its untracked files' bytes)",
    ("commands/crs.py", "cr_worktree"): "a CR's worktree, a folder of the code repository",
'''
s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
