"""Scratch: reference solutions of the 11 feature CRs, applied to a checkout of the sandbox base.

Usage (from the checkout's root): python refs.py <slug>
Never committed to chantier. Each solution is written from the frozen specification only.
"""
import sys
from pathlib import Path


def read(p):
    return Path(p).read_text(encoding="utf-8")


def write(p, text):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def sub(p, old, new):
    text = read(p)
    assert text.count(old) == 1, (p, old, text.count(old))
    write(p, text.replace(old, new))


def append(p, text):
    write(p, read(p).rstrip("\n") + "\n" + text)


APP = "src/shelf/app.py"
VIEWS = "src/shelf/views.py"
MODELS = "src/shelf/models.py"
STORE = "src/shelf/store.py"
README = "README.md"
STATIC_ANCHOR = '    if path == "/static/style.css":'
HEALTHZ_ROW = '| GET | `/healthz` | `{"status": "ok", "version": "<version>"}` as JSON |\n'
ITEM_STATUS_RE = 'ITEM_STATUS = re.compile(r"^/items/(\\d+)/status$")\n'
QUERY_HELPER = '''

def _query(environ) -> dict:
    return {k: v[0] for k, v in parse_qs(environ.get("QUERY_STRING") or "", keep_blank_values=True).items()}
'''
FORM_END = '    return {k: v[0] for k, v in parse_qs(raw, keep_blank_values=True).items()}\n'
ITEM_BACK = '    <p><a href="/">Back to the list</a></p>\n'
ERROR_LINE_VIEW = '    message = f\'<p class="error">{escape(error)}</p>\' if error else ""\n'


def readme_rows(rows):
    sub(README, HEALTHZ_ROW, HEALTHZ_ROW + rows)


def route(code):
    sub(APP, STATIC_ANCHOR, code + STATIC_ANCHOR)


def delete_item():
    # the store keeps the next id, so the data file becomes {"next_id": n, "items": [...]}
    sub(STORE, '''def load() -> list[dict]:
    path = data_path()
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save(items: list[dict]) -> None:
    path = data_path()
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(items, indent=2) + "\\n", encoding="utf-8")
    os.replace(temporary, path)
''', '''def _read() -> dict:
    path = data_path()
    if not path.exists():
        return {"next_id": 1, "items": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):  # a file written before ids were kept
        data = {"next_id": max((i["id"] for i in data), default=0) + 1, "items": data}
    return data


def load() -> list[dict]:
    return _read()["items"]


def _next_id(items: list[dict]) -> int:
    return max(_read()["next_id"], max((i["id"] for i in items), default=0) + 1)


def save(items: list[dict]) -> None:
    path = data_path()
    temporary = path.with_name(path.name + ".tmp")
    state = {"next_id": _next_id(items), "items": items}
    temporary.write_text(json.dumps(state, indent=2) + "\\n", encoding="utf-8")
    os.replace(temporary, path)
''')
    sub(STORE, '        "id": max((i["id"] for i in items), default=0) + 1,\n', '        "id": _next_id(items),\n')
    append(STORE, '''

def delete(item_id: int) -> bool:
    items = load()
    kept = [i for i in items if i["id"] != item_id]
    if len(kept) == len(items):
        return False
    save(kept)
    return True
''')
    sub(APP, ITEM_STATUS_RE, ITEM_STATUS_RE + 'ITEM_DELETE = re.compile(r"^/items/(\\d+)/delete$")\n')
    route('''    match = ITEM_DELETE.match(path)
    if match:
        if method != "POST":
            return _error(start_response, 405, [("Allow", "POST")])
        if not store.delete(int(match.group(1))):
            return _error(start_response, 404)
        return _redirect(start_response, "/")

''')
    sub("src/shelf/templates/item.html", ITEM_BACK, '''    <form method="post" action="/items/$id/delete">
      <button type="submit">Delete</button>
    </form>
''' + ITEM_BACK)
    readme_rows("| POST | `/items/<id>/delete` | Deletes the item. 303 to `/`; 404 on an unknown item. An id is never given twice |\n")
    sub("tests/test_store.py", 'json.loads(shelf_data.read_text(encoding="utf-8"))[0]["title"]',
        'json.loads(shelf_data.read_text(encoding="utf-8"))["items"][0]["title"]')
    append("tests/test_items.py", '''

def test_deleting_an_item_and_never_reusing_its_id(client):
    client.post("/items", {"title": "First"})
    client.post("/items", {"title": "Second"})
    response = client.post("/items/2/delete", {})
    assert (response.status, response.headers["location"]) == (303, "/")
    assert client.get("/items/2").status == 404
    client.post("/items", {"title": "Third"})
    assert "Third" in client.get("/items/3").text
    assert client.post("/items/9/delete", {}).status == 404
    assert client.get("/items/1/delete").status == 405
''')


def edit_item():
    sub(APP, ITEM_STATUS_RE, ITEM_STATUS_RE + 'ITEM_EDIT = re.compile(r"^/items/(\\d+)/edit$")\n')
    route('''    match = ITEM_EDIT.match(path)
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

''')
    append(VIEWS, '''

def edit(entry: dict, error: str = "", values: dict | None = None) -> str:
    values = values or {"title": entry["title"], "url": entry.get("url") or ""}
    message = f'<p class="error">{escape(error)}</p>' if error else ""
    body = _template("edit.html").substitute(
        id=entry["id"],
        error=message,
        title_value=escape(values.get("title", ""), quote=True),
        url_value=escape(values.get("url", ""), quote=True),
    )
    return page("Edit " + entry["title"], body)
''')
    write("src/shelf/templates/edit.html", '''    <h1>Edit item</h1>
$error
    <form method="post" action="/items/$id/edit">
      <label>Title <input name="title" value="$title_value" maxlength="400" required></label>
      <label>Link <input name="url" value="$url_value" placeholder="https://"></label>
      <button type="submit">Save</button>
    </form>
    <p><a href="/items/$id">Back to the item</a></p>
''')
    sub("src/shelf/templates/item.html", ITEM_BACK, '    <p><a href="/items/$id/edit">Edit</a></p>\n' + ITEM_BACK)
    readme_rows("| GET | `/items/<id>/edit` | The edit form for the title and the link; 404 page if unknown |\n"
                "| POST | `/items/<id>/edit` | Saves `title` and `url`, validated as when adding. 303 to the item's page; 400 with the form again on invalid input; 404 on an unknown item |\n")
    append("tests/test_items.py", '''

def test_editing_an_item(client):
    client.post("/items", {"title": "Old", "url": ""})
    assert 'value="Old"' in client.get("/items/1/edit").text
    response = client.post("/items/1/edit", {"title": " New ", "url": "https://example.com"})
    assert (response.status, response.headers["location"]) == (303, "/items/1")
    assert "New" in client.get("/items/1").text
    bad = client.post("/items/1/edit", {"title": "", "url": ""})
    assert bad.status == 400 and "The title is required." in bad.text
    assert client.get("/items/9/edit").status == 404
    assert client.post("/items/9/edit", {"title": "x", "url": ""}).status == 404
''')


def _query_helper():
    sub(APP, FORM_END, FORM_END + QUERY_HELPER)


def status_filter():
    _query_helper()
    sub(APP, '''        return _respond(start_response, 200, views.index(store.load()))
''', '''        status = _query(environ).get("status", "")
        if status and status not in STATUSES:
            return _respond(start_response, 400, views.index(store.load(), f"Unknown status: {status}"))
        items = [i for i in store.load() if not status or i["status"] == status]
        return _respond(start_response, 200, views.index(items, status=status))
''')
    sub(VIEWS, 'def index(items: list[dict], error: str = "", values: dict | None = None) -> str:',
        '''FILTERS = (("All", ""), ("To read", "to-read"), ("Reading", "reading"), ("Done", "done"))


def _filters(current: str) -> str:
    links = []
    for label, value in FILTERS:
        href = f"/?status={value}" if value else "/"
        mark = ' aria-current="page"' if value == current else ""
        links.append(f'<a href="{href}"{mark}>{label}</a>')
    return '<nav class="filters">' + " ".join(links) + "</nav>"


def index(items: list[dict], error: str = "", values: dict | None = None, status: str = "") -> str:''')
    sub(VIEWS, '    rows = "\\n".join(\n', '    empty = "No items with this status." if status else "Nothing on the shelf yet."\n    rows = "\\n".join(\n')
    sub(VIEWS, '''    ) or '<li class="empty">Nothing on the shelf yet.</li>'
''', '''    ) or f'<li class="empty">{empty}</li>'
''')
    sub(VIEWS, '''        url_value=escape(values.get("url", ""), quote=True),
    )
    return page("shelf", body)''', '''        url_value=escape(values.get("url", ""), quote=True),
        filters=_filters(status),
    )
    return page("shelf", body)''')
    sub("src/shelf/templates/index.html", '    <ul class="items">\n', '$filters\n    <ul class="items">\n')
    readme_rows("| GET | `/?status=<s>` | The list filtered to `to-read`, `reading` or `done` (empty: all); 400 on any other value |\n")
    append("tests/test_pages.py", '''

def test_the_status_filter(client):
    client.post("/items", {"title": "One"})
    client.post("/items", {"title": "Two"})
    client.post("/items/2/status", {"status": "reading"})
    page = client.get("/?status=reading").text
    assert "Two" in page and "One" not in page
    assert client.get("/?status=lost").status == 400
    assert "No items with this status." in client.get("/?status=done").text
    assert 'aria-current="page"' in client.get("/").text
''')


def json_api():
    sub(APP, 'from shelf.models import STATUSES, validate_new\n', 'from shelf.models import STATUSES, validate_new\nfrom shelf import api\n')
    sub(APP, ITEM_STATUS_RE, ITEM_STATUS_RE + 'API_ITEM = re.compile(r"^/api/items/(\\d+)$")\n')
    route('''    if path == "/api/items":
        if method != "GET":
            return _error(start_response, 405, [("Allow", "GET")])
        return _respond(start_response, 200, api.items_body(), api.JSON)

    match = API_ITEM.match(path)
    if match:
        if method != "GET":
            return _error(start_response, 405, [("Allow", "GET")])
        entry = store.get(int(match.group(1)))
        if entry is None:
            return _respond(start_response, 404, api.error_body(), api.JSON)
        return _respond(start_response, 200, api.item_body(entry), api.JSON)

''')
    write("src/shelf/api.py", '''"""The read-only JSON API."""
from __future__ import annotations

import json

from shelf import store

JSON = "application/json; charset=utf-8"


def _item(entry: dict) -> dict:
    return {
        "id": entry["id"],
        "title": entry["title"],
        "url": entry.get("url") or None,
        "status": entry["status"],
        "added": entry["added"],
    }


def items_body() -> str:
    return json.dumps([_item(i) for i in store.load()])


def item_body(entry: dict) -> str:
    return json.dumps(_item(entry))


def error_body() -> str:
    return json.dumps({"error": "not found"})
''')
    sub("src/shelf/templates/index.html", '    <h2>Add an item</h2>\n', '    <p><a href="/api/items">JSON</a></p>\n    <h2>Add an item</h2>\n')
    readme_rows("| GET | `/api/items` | All items as a JSON array, in id order |\n"
                "| GET | `/api/items/<id>` | One item as JSON; 404 `{\"error\": \"not found\"}` if unknown |\n")
    write("tests/test_api.py", '''import json


def test_the_api_lists_and_shows_items(client):
    assert json.loads(client.get("/api/items").text) == []
    client.post("/items", {"title": "<b>", "url": ""})
    items = json.loads(client.get("/api/items").text)
    assert items[0]["title"] == "<b>" and items[0]["url"] is None and items[0]["id"] == 1
    assert json.loads(client.get("/api/items/1").text)["status"] == "to-read"
    missing = client.get("/api/items/9")
    assert (missing.status, json.loads(missing.text)) == (404, {"error": "not found"})
    assert client.post("/api/items", {}).status == 405
    assert client.get("/api/items").headers["content-type"] == "application/json; charset=utf-8"
    assert 'href="/api/items"' in client.get("/").text
''')


def stats_page():
    sub(APP, STATIC_ANCHOR, STATIC_ANCHOR)  # sanity: anchor exists once
    route('''    if path == "/stats":
        if method != "GET":
            return _error(start_response, 405, [("Allow", "GET")])
        return _respond(start_response, 200, views.stats(store.load()))

''')
    append(VIEWS, '''

def stats(items: list[dict]) -> str:
    counts = [(label, sum(1 for i in items if i["status"] == s)) for label, s in
              (("To read", "to-read"), ("Reading", "reading"), ("Done", "done"))]
    counts.append(("Total", len(items)))
    rows = "\\n".join(f"<tr><th>{label}</th><td>{count}</td></tr>" for label, count in counts)
    return page("Statistics", _template("stats.html").substitute(rows=rows))
''')
    write("src/shelf/templates/stats.html", '''    <h1>Statistics</h1>
    <table class="stats">
$rows
    </table>
''')
    sub("src/shelf/templates/base.html", '  <header><a href="/">shelf</a></header>\n',
        '  <header><a href="/">shelf</a> <a href="/stats">Statistics</a></header>\n')
    readme_rows("| GET | `/stats` | The number of items per status and the total |\n")
    append("tests/test_pages.py", '''

def test_the_stats_page(client):
    assert "<td>0</td>" in client.get("/stats").text
    client.post("/items", {"title": "One"})
    client.post("/items", {"title": "Two"})
    client.post("/items/2/status", {"status": "done"})
    page = client.get("/stats").text
    assert "<th>Total</th><td>2</td>" in page and "<th>Done</th><td>1</td>" in page
    assert 'href="/stats"' in client.get("/").text
    assert client.post("/stats", {}).status == 405
''')


def csv_export():
    sub(APP, 'from shelf.models import STATUSES, validate_new\n', 'from shelf.models import STATUSES, validate_new\nfrom shelf import export\n')
    route('''    if path == "/export.csv":
        if method != "GET":
            return _error(start_response, 405, [("Allow", "GET")])
        headers = [("Content-Disposition", 'attachment; filename="shelf.csv"')]
        return _respond(start_response, 200, export.to_csv(store.load()), "text/csv; charset=utf-8", headers)

''')
    write("src/shelf/export.py", '''"""The shelf as CSV."""
from __future__ import annotations

import csv
import io

COLUMNS = ("id", "title", "url", "status", "added")


def to_csv(items: list[dict]) -> str:
    out = io.StringIO(newline="")
    writer = csv.writer(out)
    writer.writerow(COLUMNS)
    for i in items:
        writer.writerow([i["id"], i["title"], i.get("url") or "", i["status"], i["added"]])
    return out.getvalue()
''')
    sub("src/shelf/templates/index.html", '    <h2>Add an item</h2>\n', '    <p><a href="/export.csv">Export CSV</a></p>\n    <h2>Add an item</h2>\n')
    readme_rows("| GET | `/export.csv` | The shelf as a CSV download: `id,title,url,status,added` |\n")
    write("tests/test_export.py", '''def test_the_csv_export(client):
    assert client.get("/export.csv").text == "id,title,url,status,added\\r\\n"
    client.post("/items", {"title": 'Hello, "world"', "url": ""})
    response = client.get("/export.csv")
    assert response.text.splitlines()[1].startswith('1,"Hello, ""world""",,to-read,')
    assert response.headers["content-disposition"] == 'attachment; filename="shelf.csv"'
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert 'href="/export.csv"' in client.get("/").text
    assert client.post("/export.csv", {}).status == 405
''')


def item_notes():
    sub(MODELS, 'MAX_TITLE = 200\n', 'MAX_TITLE = 200\nMAX_NOTES = 2000\n')
    append(MODELS, '''

def validate_notes(notes: str) -> tuple[str, str | None]:
    """Return the trimmed notes and an error message (None when valid)."""
    notes = (notes or "").strip()
    if len(notes) > MAX_NOTES:
        return notes, f"Notes are limited to {MAX_NOTES} characters."
    return notes, None
''')
    sub(STORE, '        "added": datetime.date.today().isoformat(),\n', '        "added": datetime.date.today().isoformat(),\n        "notes": "",\n')
    append(STORE, '''

def set_notes(item_id: int, notes: str) -> dict | None:
    items = load()
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        return None
    item["notes"] = notes
    save(items)
    return item
''')
    sub(APP, 'from shelf.models import STATUSES, validate_new\n', 'from shelf.models import STATUSES, validate_new\nfrom shelf.models import validate_notes\n')
    sub(APP, ITEM_STATUS_RE, ITEM_STATUS_RE + 'ITEM_NOTES = re.compile(r"^/items/(\\d+)/notes$")\n')
    route('''    match = ITEM_NOTES.match(path)
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

''')
    sub(VIEWS, 'def item(entry: dict) -> str:', 'def item(entry: dict, error: str = "") -> str:')
    sub(VIEWS, '    body = _template("item.html").substitute(\n',
        ERROR_LINE_VIEW + '    body = _template("item.html").substitute(\n        error=message,\n')
    sub(VIEWS, '        options=options,\n    )',
        '        options=options,\n        notes=escape(entry.get("notes", "")),\n    )')
    sub("src/shelf/templates/item.html", '    <h1>$title</h1>\n', '    <h1>$title</h1>\n$error\n')
    sub("src/shelf/templates/item.html", ITEM_BACK, '''    <div class="notes">$notes</div>
    <form method="post" action="/items/$id/notes">
      <label>Notes <textarea name="notes">$notes</textarea></label>
      <button type="submit">Save notes</button>
    </form>
''' + ITEM_BACK)
    append("src/shelf/static/style.css", '''
.notes {
  white-space: pre-wrap;
}
''')
    readme_rows("| POST | `/items/<id>/notes` | Saves the item's `notes` (at most 2000 characters, trimmed). 303 to the item's page; 400 when too long; 404 on an unknown item |\n")
    append("tests/test_items.py", '''

def test_item_notes(client):
    client.post("/items", {"title": "Book"})
    response = client.post("/items/1/notes", {"notes": " a\\n<b> "})
    assert (response.status, response.headers["location"]) == (303, "/items/1")
    assert "a\\n&lt;b&gt;" in client.get("/items/1").text
    too_long = client.post("/items/1/notes", {"notes": "x" * 2001})
    assert too_long.status == 400 and "Notes are limited to 2000 characters." in too_long.text
    assert "a\\n&lt;b&gt;" in client.get("/items/1").text
    assert client.post("/items/9/notes", {"notes": "x"}).status == 404
    assert client.get("/items/1/notes").status == 405
    assert "pre-wrap" in client.get("/static/style.css").text
''')


def title_search():
    _query_helper()
    sub(APP, '''        return _respond(start_response, 200, views.index(store.load()))
''', '''        query = _query(environ).get("q", "").strip()
        items = [i for i in store.load() if query.lower() in i["title"].lower()]
        return _respond(start_response, 200, views.index(items, query=query))
''')
    sub(VIEWS, 'def index(items: list[dict], error: str = "", values: dict | None = None) -> str:',
        'def index(items: list[dict], error: str = "", values: dict | None = None, query: str = "") -> str:')
    sub(VIEWS, '    rows = "\\n".join(\n', '    empty = f\'No items match "{escape(query)}".\' if query else "Nothing on the shelf yet."\n    rows = "\\n".join(\n')
    sub(VIEWS, '''    ) or '<li class="empty">Nothing on the shelf yet.</li>'
''', '''    ) or f'<li class="empty">{empty}</li>'
''')
    sub(VIEWS, '''        url_value=escape(values.get("url", ""), quote=True),
    )
    return page("shelf", body)''', '''        url_value=escape(values.get("url", ""), quote=True),
        q_value=escape(query, quote=True),
    )
    return page("shelf", body)''')
    sub("src/shelf/templates/index.html", '    <ul class="items">\n', '''    <form method="get" action="/">
      <input name="q" value="$q_value"> <button type="submit">Search</button>
    </form>
    <ul class="items">
''')
    readme_rows("| GET | `/?q=<text>` | The list filtered to the titles containing the text, ignoring case (blank: all) |\n")
    append("tests/test_pages.py", '''

def test_the_title_search(client):
    client.post("/items", {"title": "Dune Messiah"})
    client.post("/items", {"title": "Foundation"})
    page = client.get("/?q=DUNE").text
    assert "Dune Messiah" in page and "Foundation" not in page
    assert "Foundation" in client.get("/?q=%20").text
    none = client.get("/?q=<i>").text
    assert 'value="&lt;i&gt;"' in none and 'No items match "&lt;i&gt;".' in none
''')


def item_rating():
    append(MODELS, '''

def parse_rating(value: str) -> tuple[int | None, str | None]:
    """Return the rating (None clears it) and an error message (None when valid)."""
    value = (value or "").strip()
    if value == "":
        return None, None
    if value in ("1", "2", "3", "4", "5"):
        return int(value), None
    return None, "Rating must be a whole number from 1 to 5."
''')
    append(STORE, '''

def set_rating(item_id: int, rating: int | None) -> dict | None:
    items = load()
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        return None
    item["rating"] = rating
    save(items)
    return item
''')
    sub(APP, 'from shelf.models import STATUSES, validate_new\n', 'from shelf.models import STATUSES, validate_new\nfrom shelf.models import parse_rating\n')
    sub(APP, ITEM_STATUS_RE, ITEM_STATUS_RE + 'ITEM_RATING = re.compile(r"^/items/(\\d+)/rating$")\n')
    route('''    match = ITEM_RATING.match(path)
    if match:
        if method != "POST":
            return _error(start_response, 405, [("Allow", "POST")])
        item_id = int(match.group(1))
        entry = store.get(item_id)
        if entry is None:
            return _error(start_response, 404)
        rating, problem = parse_rating(_form(environ).get("rating", ""))
        if problem:
            return _respond(start_response, 400, views.item(entry, problem))
        store.set_rating(item_id, rating)
        return _redirect(start_response, f"/items/{item_id}")

''')
    sub(VIEWS, 'def item(entry: dict) -> str:', 'def item(entry: dict, error: str = "") -> str:')
    sub(VIEWS, '    body = _template("item.html").substitute(\n',
        ERROR_LINE_VIEW + '''    rating = entry.get("rating")
    rating_options = "\\n".join(
        f'<option value="{v}"{" selected" if v == (str(rating) if rating else "") else ""}>{t}</option>'
        for v, t in [("", "No rating"), *[(str(n), str(n)) for n in range(1, 6)]]
    )
    body = _template("item.html").substitute(
        error=message,
''')
    sub(VIEWS, '        options=options,\n    )',
        '        options=options,\n        rating=f"{rating}/5" if rating else "none",\n        rating_options=rating_options,\n    )')
    sub(VIEWS, 'def index(items', '''def _rated(entry: dict) -> str:
    return f' <span class="rating">{entry["rating"]}/5</span>' if entry.get("rating") else ""


def index(items''')
    sub(VIEWS, '''        f'<span class="added">{escape(i["added"])}</span></li>\'''', '''        f'<span class="added">{escape(i["added"])}</span>{_rated(i)}</li>\'''')
    sub("src/shelf/templates/item.html", '    <h1>$title</h1>\n', '    <h1>$title</h1>\n$error\n')
    sub("src/shelf/templates/item.html", ITEM_BACK, '''    <p>Rating: $rating</p>
    <form method="post" action="/items/$id/rating">
      <label>Rating <select name="rating">
$rating_options
      </select></label>
      <button type="submit">Rate</button>
    </form>
''' + ITEM_BACK)
    readme_rows("| POST | `/items/<id>/rating` | Sets the item's `rating` (`1` to `5`, or empty to clear). 303 to the item's page; 400 on any other value; 404 on an unknown item |\n")
    append("tests/test_items.py", '''

def test_item_rating(client):
    client.post("/items", {"title": "Book"})
    assert "Rating: none" in client.get("/items/1").text
    assert client.post("/items/1/rating", {"rating": "4"}).status == 303
    assert "Rating: 4/5" in client.get("/items/1").text and "4/5" in client.get("/").text
    bad = client.post("/items/1/rating", {"rating": "6"})
    assert bad.status == 400 and "Rating must be a whole number from 1 to 5." in bad.text
    assert client.post("/items/1/rating", {"rating": ""}).status == 303
    assert "Rating: none" in client.get("/items/1").text
    assert client.post("/items/9/rating", {"rating": "3"}).status == 404
''')


def sort_list():
    _query_helper()
    sub(APP, '''        return _respond(start_response, 200, views.index(store.load()))
''', '''        sort = _query(environ).get("sort", "") or "oldest"
        if sort not in SORTS:
            return _respond(start_response, 400, views.index(store.load(), f"Unknown sort: {sort}"))
        return _respond(start_response, 200, views.index(sorted(store.load(), key=SORTS[sort]), sort=sort))
''')
    sub(APP, 'HTML = "text/html; charset=utf-8"\n', '''HTML = "text/html; charset=utf-8"
SORTS = {
    "oldest": lambda i: i["id"],
    "newest": lambda i: -i["id"],
    "title": lambda i: (i["title"].lower(), i["id"]),
}
''')
    sub(VIEWS, 'def index(items: list[dict], error: str = "", values: dict | None = None) -> str:',
        '''ORDERS = (("Oldest", "oldest"), ("Newest", "newest"), ("Title", "title"))


def _sort_nav(current: str) -> str:
    links = []
    for label, value in ORDERS:
        mark = ' aria-current="page"' if value == current else ""
        links.append(f'<a href="/?sort={value}"{mark}>{label}</a>')
    return '<nav class="sort">' + " ".join(links) + "</nav>"


def index(items: list[dict], error: str = "", values: dict | None = None, sort: str = "oldest") -> str:''')
    sub(VIEWS, '''        url_value=escape(values.get("url", ""), quote=True),
    )
    return page("shelf", body)''', '''        url_value=escape(values.get("url", ""), quote=True),
        sort_nav=_sort_nav(sort),
    )
    return page("shelf", body)''')
    sub("src/shelf/templates/index.html", '    <ul class="items">\n', '$sort_nav\n    <ul class="items">\n')
    readme_rows("| GET | `/?sort=<order>` | The list sorted by `oldest` (default), `newest` or `title`; 400 on any other value |\n")
    append("tests/test_pages.py", '''

def test_the_sort_orders(client):
    for title in ("banana", "Apple", "cherry"):
        client.post("/items", {"title": title})

    def order(path):
        page = client.get(path).text
        return sorted(("banana", "Apple", "cherry"), key=lambda t: page.index(f">{t}</a>"))

    assert order("/") == order("/?sort=oldest") == ["banana", "Apple", "cherry"]
    assert order("/?sort=newest") == ["cherry", "Apple", "banana"]
    assert order("/?sort=title") == ["Apple", "banana", "cherry"]
    response = client.get("/?sort=size")
    assert response.status == 400 and "Unknown sort: size" in response.text
    assert client.get("/?sort=title").text.count('aria-current="page"') == 1
''')


def duplicate_url():
    sub(MODELS, 'MAX_TITLE = 200\n', 'MAX_TITLE = 200\n')
    sub(MODELS, 'from __future__ import annotations\n', 'from __future__ import annotations\n\nfrom urllib.parse import urlsplit, urlunsplit\n')
    append(MODELS, '''

def normalize_url(url: str) -> str:
    """The key two URLs share when they are the same address (empty for no URL)."""
    parts = urlsplit((url or "").strip())
    if not parts.scheme and not parts.netloc and not parts.path:
        return ""
    path = parts.path[:-1] if parts.path.endswith("/") else parts.path
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, parts.fragment))


def find_duplicate(url: str, items: list[dict], ignore_id: int | None = None) -> dict | None:
    """The other item that has this URL, or None. An item with no URL never clashes."""
    key = normalize_url(url)
    if not key:
        return None
    return next((i for i in items if i["id"] != ignore_id and normalize_url(i.get("url") or "") == key), None)
''')
    sub(APP, 'from shelf.models import STATUSES, validate_new\n', 'from shelf.models import STATUSES, validate_new\nfrom shelf.models import find_duplicate\n')
    sub(APP, '''        store.add(values["title"], values["url"])
''', '''        duplicate = find_duplicate(values["url"], store.load())
        if duplicate:
            return _respond(start_response, 400, views.index(store.load(), values=values, duplicate=duplicate))
        store.add(values["title"], values["url"])
''')
    sub(VIEWS, 'def index(items: list[dict], error: str = "", values: dict | None = None) -> str:',
        'def index(items: list[dict], error: str = "", values: dict | None = None, duplicate: dict | None = None) -> str:')
    sub(VIEWS, ERROR_LINE_VIEW.replace("message = ", "message = ", 1), ERROR_LINE_VIEW + '''    if duplicate:
        link = f'<a href="/items/{duplicate["id"]}">{escape(duplicate["title"])}</a>'
        message = f'<p class="error">Already on the shelf: {link}</p>'
''')
    readme_rows("| POST | `/items` (duplicate) | An item whose URL is already on the shelf (same after trimming, ignoring the case of the scheme and the host and one trailing `/`) gets 400 and a link to the existing item |\n")
    append("tests/test_items.py", '''

def test_a_duplicate_url_is_refused(client):
    client.post("/items", {"title": "First", "url": "https://example.com/a"})
    response = client.post("/items", {"title": "Second", "url": "https://EXAMPLE.com/a/"})
    assert response.status == 400
    assert 'Already on the shelf: <a href="/items/1">First</a>' in response.text
    assert "Second" not in client.get("/").text
    assert client.post("/items", {"title": "Third", "url": "https://example.com/A"}).status == 303
    assert client.post("/items", {"title": "Four"}).status == 303
    assert client.post("/items", {"title": "Five"}).status == 303
''')


if __name__ == "__main__":
    globals()[sys.argv[1].replace("-", "_")]()
