p = "src/shelf/app.py"
t = open(p, encoding="utf-8").read()
old = """            return _respond(start_response, 400, views.edit(entry, problem, values))
        items = store.load()
"""
assert t.count(old) == 1
new = """            return _respond(start_response, 400, views.edit(entry, problem, values))
        items = store.load()
        duplicate = find_duplicate(values["url"], items, ignore_id=item_id)
        if duplicate:
            return _respond(start_response, 400, views.edit(entry, f"Already on the shelf: {duplicate['title']}", values))
"""
open(p, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
p = "tests/test_items.py"
t = open(p, encoding="utf-8").read()
t += '''

def test_editing_cannot_create_a_duplicate_url(client):
    client.post("/items", {"title": "First", "url": "https://example.com/a"})
    client.post("/items", {"title": "Second", "url": "https://example.com/b"})
    assert client.post("/items/2/edit", {"title": "Second", "url": "https://EXAMPLE.com/a/"}).status == 400
    assert client.post("/items/1/edit", {"title": "First again", "url": "https://example.com/a"}).status == 303
'''
open(p, "w", encoding="utf-8", newline="\n").write(t)
