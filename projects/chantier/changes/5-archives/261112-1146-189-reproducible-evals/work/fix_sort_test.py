p = "tests/test_pages.py"
t = open(p, encoding="utf-8").read()
old = """assert client.get("/?sort=title").text.count('aria-current="page"') == 1"""
assert old in t
new = """nav = client.get("/?sort=title").text.split('<nav class="sort">')[1]
    assert nav.count('aria-current="page"') == 1"""
open(p, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
