"""Scratch: repair app.py after the union merge of item-notes (run from the ref root)."""
from pathlib import Path

p = Path("src/shelf/app.py")
t = p.read_text(encoding="utf-8")
old_start = t.index('    match = ITEM_EDIT.match(path)\n')
old_end = t.index('    if path == "/api/items":')
fixed = '''    match = ITEM_EDIT.match(path)
    if match:
        if method not in ("GET", "POST"):
            return _error(start_response, 405, [("Allow", "GET, POST")])
        item_id = int(match.group(1))
        entry = store.get(item_id)
        if entry is None:
            return _error(start_response, 404)
        if method == "GET":
            return _respond(start_response, 200, views.edit(entry))
        form = _form(environ)
        values, problem = validate_new(form.get("title", ""), form.get("url", ""))
        if problem:
            return _respond(start_response, 400, views.edit(entry, problem, values))
        items = store.load()
        for stored in items:
            if stored["id"] == item_id:
                stored.update(values)
        store.save(items)
        return _redirect(start_response, f"/items/{item_id}")

    match = ITEM_NOTES.match(path)
    if match:
        if method != "POST":
            return _error(start_response, 405, [("Allow", "POST")])
        item_id = int(match.group(1))
        entry = store.get(item_id)
        if entry is None:
            return _error(start_response, 404)
        notes, problem = validate_notes(_form(environ).get("notes", ""))
        if problem:
            return _respond(start_response, 400, views.item(entry, problem))
        store.set_notes(item_id, notes)
        return _redirect(start_response, f"/items/{item_id}")

'''
t = t[:old_start] + fixed + t[old_end:]
tail = '''
        notes, problem = validate_notes(_form(environ).get("notes", ""))
        if problem:
            return _respond(start_response, 400, views.item(entry, problem))
        store.set_notes(item_id, notes)
        return _redirect(start_response, f"/items/{item_id}")

    if path == "/static/style.css":'''
assert t.count(tail) == 1
t = t.replace(tail, '\n    if path == "/static/style.css":')
with open(p, "w", encoding="utf-8", newline="\n") as f:
    f.write(t)
