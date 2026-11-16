"""Scratch: item-rating applied on top of the nine-minus-one batch (run from the ref root)."""
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
import refs  # noqa: E402
from refs import APP, MODELS, README, STORE, VIEWS, append, readme_rows, route, sub  # noqa: E402

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
sub(APP, 'from shelf.models import validate_notes\n', 'from shelf.models import parse_rating, validate_notes\n')
sub(APP, 'ITEM_NOTES = re.compile(r"^/items/(\\d+)/notes$")\n',
    'ITEM_NOTES = re.compile(r"^/items/(\\d+)/notes$")\nITEM_RATING = re.compile(r"^/items/(\\d+)/rating$")\n')
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
sub(VIEWS, '    body = _template("item.html").substitute(\n        error=message,\n', '''    rating = entry.get("rating")
    rating_options = "\\n".join(
        f'<option value="{v}"{" selected" if v == (str(rating) if rating else "") else ""}>{t}</option>'
        for v, t in [("", "No rating"), *[(str(n), str(n)) for n in range(1, 6)]]
    )
    body = _template("item.html").substitute(
        error=message,
''')
sub(VIEWS, '        notes=escape(entry.get("notes", "")),\n',
    '        notes=escape(entry.get("notes", "")),\n        rating=f"{rating}/5" if rating else "none",\n        rating_options=rating_options,\n')
sub(VIEWS, 'FILTERS = (', '''def _rated(entry: dict) -> str:
    return f' <span class="rating">{entry["rating"]}/5</span>' if entry.get("rating") else ""


FILTERS = (''')
sub(VIEWS, '''        f'<span class="added">{escape(i["added"])}</span></li>\'''', '''        f'<span class="added">{escape(i["added"])}</span>{_rated(i)}</li>\'''')
sub("src/shelf/templates/item.html", refs.ITEM_BACK, '''    <p>Rating: $rating</p>
    <form method="post" action="/items/$id/rating">
      <label>Rating <select name="rating">
$rating_options
      </select></label>
      <button type="submit">Rate</button>
    </form>
''' + refs.ITEM_BACK)
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
