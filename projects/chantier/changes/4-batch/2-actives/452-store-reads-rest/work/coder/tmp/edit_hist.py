from editlib import Editor

e = Editor("history.py")
e.r(
    '''            and (repo.changes / archive / "work" / "retro.md").is_file()''',
    '''            and repo.store.is_file(f"{archive}/work/retro.md")''',
)
e.save()
