"""Writes evals/kit/sandbox-crs/<slug>/ (13 folders). Run: python gen_crs.py <worktree root>."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) / "evals" / "kit" / "sandbox-crs"

COMMON = [
    'each behaviour of "Change" has a test, in {test}, using the `client` fixture;',
    "the README's \"Routes\" table lists every new route and every new query parameter of `/`;",
    "all user text is HTML-escaped; no JavaScript; no new runtime dependency; a known path with the wrong method gets 405, like the base routes;",
    "the fast gate (`uv run pytest -q -x`) and the long gate (`uv run --locked pytest -q`) pass.",
]

CRS = {}


def cr(slug, title, request, intent, answers, change, files, test, extra_done=()):
    CRS[slug] = dict(title=title, request=request, intent=intent, answers=answers,
                     change=change, files=files, test=test, extra=list(extra_done))


cr("delete-item", "Delete an item",
   "I added a book by mistake. Let me delete an item from my shelf.",
   "The user wants to delete an item from the shelf, from the item's page.",
   ["A button on the item page, a POST route; no confirmation page.",
    "After a delete the user lands on the list.",
    "An id is never given twice, even after a delete: a new item never takes the id of a deleted one."],
   ["The item page has `<form method=\"post\" action=\"/items/<id>/delete\">` with a button `Delete`.",
    "`POST /items/<id>/delete` removes the item and answers 303 to `/`. An unknown id: the 404 page. `GET` on that path: 405.",
    "After a delete, the item is gone from `/` and `/items/<id>` is 404; the other items stay.",
    "An id is never given twice: an item added after a delete gets an id higher than any id the shelf ever gave, the deleted one included (the store keeps the next id)."],
   ["`src/shelf/store.py`", "`src/shelf/app.py`", "`src/shelf/templates/item.html`", "`README.md`", "`tests/test_items.py`"],
   "`tests/test_items.py`")

cr("edit-item", "Edit an item",
   "I made a typo in a title. Let me edit an item's title and link.",
   "The user wants to correct an item's title and URL after adding it.",
   ["A separate edit page, `/items/<id>/edit`, linked from the item page.",
    "The rules are the same as adding: one validation function serves both.",
    "Only the title and the URL are editable; the status and the date stay as they are.",
    "An invalid edit shows the edit page again with the message and the values entered, and saves nothing."],
   ["`GET /items/<id>/edit`: a page with `<form method=\"post\" action=\"/items/<id>/edit\">`, inputs `name=\"title\"` and `name=\"url\"` holding the current values (escaped). An unknown id: 404.",
    "`POST /items/<id>/edit` (`title`, `url`) is validated exactly as adding (title 1-200 characters after trimming; URL empty or starting with `http://` or `https://`), by one validation function in `models.py` that adding uses too. Valid: title and URL saved (trimmed), status and date added unchanged, 303 to `/items/<id>`. Invalid: 400, the edit page again with the error message and the values entered; nothing saved. Unknown id: 404.",
    "The item page links to `/items/<id>/edit` with the text `Edit`."],
   ["`src/shelf/models.py`", "`src/shelf/app.py`", "`src/shelf/views.py`", "`src/shelf/templates/edit.html` (new)", "`src/shelf/templates/item.html`", "`README.md`", "`tests/test_items.py`"],
   "`tests/test_items.py`")

cr("status-filter", "Filter the list by status",
   "My list is long. I want to see only the books I am reading, or only the ones I finished.",
   "The user wants to filter the list page by status.",
   ["The filter is a query parameter of the list page: `?status=`.",
    "Four links above the list: all, to read, reading, done; the current one is marked with `aria-current`.",
    "An unknown status is a 400, not an empty list.",
    "A filter with no match says so in one sentence."],
   ["`GET /?status=<s>`, `<s>` one of `to-read`, `reading`, `done`: only the items with that status. `status` absent or empty: all items. Any other value: 400, with the message `Unknown status: <value>` (the value escaped).",
    "Above the list, `<nav class=\"filters\">` with four links in this order: `All` (`/`), `To read` (`/?status=to-read`), `Reading` (`/?status=reading`), `Done` (`/?status=done`). The link of the current filter (`All` with no filter) has `aria-current=\"page\"`; no other link of that nav has it.",
    "A filter that matches nothing shows `No items with this status.`."],
   ["`src/shelf/app.py`", "`src/shelf/views.py`", "`src/shelf/templates/index.html`", "`README.md`", "`tests/test_pages.py`"],
   "`tests/test_pages.py`")

cr("json-api", "Read the items as JSON",
   "I want to read my shelf from a script. Give me a JSON API.",
   "The user wants a read-only JSON view of the items.",
   ["Two read-only routes: the list and one item; nothing to write through the API.",
    "Titles are given as entered, not HTML-escaped: JSON is not HTML.",
    "An unknown id answers 404 with a small JSON error body, not the HTML page.",
    "The list page links to the API."],
   ["`GET /api/items`: 200, `Content-Type: application/json; charset=utf-8`, a JSON array of all items in id order. Each item is an object with at least `id` (integer), `title` (string), `url` (string, or `null` when the item has none), `status` (string) and `added` (`YYYY-MM-DD`).",
    "`GET /api/items/<id>`: that object. Unknown id: 404, body `{\"error\": \"not found\"}`, same content type.",
    "Any other method on these paths: 405. Titles are given as entered, not HTML-escaped.",
    "The list page links to `/api/items` with the text `JSON`."],
   ["`src/shelf/app.py`", "`src/shelf/api.py` (new)", "`src/shelf/templates/index.html`", "`README.md`", "`tests/test_api.py` (new)"],
   "`tests/test_api.py`")

cr("stats-page", "A statistics page",
   "How many books have I read? Show me some numbers about my shelf.",
   "The user wants a page with the number of items per status.",
   ["One page, `/stats`, reachable from the navigation of every page.",
    "A table with the three statuses and the total, in the order of the reading flow.",
    "The page has the same footer as every page."],
   ["`GET /stats`: a page whose `<h1>` is `Statistics`, with `<table class=\"stats\">` of four rows in this order: `To read`, `Reading`, `Done`, `Total`; each row a `<th>` holding the label and a `<td>` holding the count. An empty shelf shows four zeros.",
    "The navigation in `base.html`, on every page, links to `/stats` with the text `Statistics`.",
    "`POST /stats`: 405. The page shows the version in its footer, like every page."],
   ["`src/shelf/app.py`", "`src/shelf/views.py`", "`src/shelf/templates/stats.html` (new)", "`src/shelf/templates/base.html`", "`README.md`", "`tests/test_pages.py`"],
   "`tests/test_pages.py`")

cr("csv-export", "Export the shelf as CSV",
   "I want my shelf in a spreadsheet. Let me export it as CSV.",
   "The user wants to download the whole shelf as a CSV file.",
   ["One route, `/export.csv`, served as a download.",
    "Python's `csv` module with its default dialect; exactly five columns.",
    "The list page links to it."],
   ["`GET /export.csv`: 200, `Content-Type: text/csv; charset=utf-8`, `Content-Disposition: attachment; filename=\"shelf.csv\"`. The body is written with Python's `csv` module, default dialect (comma, minimal quoting, `\\r\\n` line ends): the header `id,title,url,status,added`, then one row per item in id order; `url` empty when the item has none. Exactly these five columns.",
    "The list page links to `/export.csv` with the text `Export CSV`. `POST /export.csv`: 405."],
   ["`src/shelf/app.py`", "`src/shelf/export.py` (new)", "`src/shelf/templates/index.html`", "`README.md`", "`tests/test_export.py` (new)"],
   "`tests/test_export.py`")

cr("item-notes", "Notes on an item",
   "I want to keep a few notes on each book.",
   "The user wants a free-text note on each item, edited from the item's page.",
   ["The notes are plain text, at most 2000 characters after trimming.",
    "Line breaks are kept when the notes are shown.",
    "Items stored before this change have empty notes; no migration.",
    "A too long note is refused with a message, and the old notes stay."],
   ["Each item has `notes`, a text, empty by default; an item stored before this change reads as empty notes. At most 2000 characters, counted after removing leading and trailing whitespace.",
    "The item page shows the notes in an element with class `notes`, escaped, with their line breaks kept (`.notes { white-space: pre-wrap; }` in `style.css`), and has `<form method=\"post\" action=\"/items/<id>/notes\">` with `<textarea name=\"notes\">` holding the current notes (escaped) and a button `Save notes`.",
    "`POST /items/<id>/notes` (`notes`): saves them trimmed, 303 to `/items/<id>`. Over 2000 characters: 400, the item page with `Notes are limited to 2000 characters.`, nothing saved. Unknown id: 404. `GET` on that path: 405."],
   ["`src/shelf/models.py`", "`src/shelf/store.py`", "`src/shelf/app.py`", "`src/shelf/templates/item.html`", "`src/shelf/static/style.css`", "`README.md`", "`tests/test_items.py`"],
   "`tests/test_items.py`")

cr("title-search", "Search the titles",
   "I cannot find a book in my long list. Let me search the titles.",
   "The user wants to search the list by title.",
   ["A search box on the list page, a GET form, query parameter `q`.",
    "A plain substring match on the title, ignoring case.",
    "A blank query shows everything.",
    "A query with no match says so, naming the query."],
   ["`GET /?q=<text>`: the items whose title contains the text, trimmed, ignoring case. `q` absent or blank: all items.",
    "The list page has `<form method=\"get\" action=\"/\">` with `<input name=\"q\">`, whose `value` is the current query (escaped), and a button `Search`.",
    "A query that matches nothing shows `No items match \"<query>\".` (the query escaped)."],
   ["`src/shelf/app.py`", "`src/shelf/views.py`", "`src/shelf/templates/index.html`", "`README.md`", "`tests/test_pages.py`"],
   "`tests/test_pages.py`")

cr("item-rating", "Rate an item",
   "I want to give each book a rating from one to five.",
   "The user wants an optional rating, from 1 to 5, on each item.",
   ["The rating is optional and can be cleared; none by default.",
    "It is set from the item page with a select; the list shows it for the rated items.",
    "A value outside 1 to 5, or not a whole number, is refused with a message, and the old rating stays.",
    "Items stored before this change have no rating; no migration."],
   ["Each item has an optional `rating`, a whole number from 1 to 5, none by default; an item stored before this change has none.",
    "The item page shows `Rating: <n>/5`, or `Rating: none`, and has `<form method=\"post\" action=\"/items/<id>/rating\">` with `<select name=\"rating\">` whose options are `\"\"` (text `No rating`), then `1` to `5`; the current one is `selected`.",
    "The list page shows `<n>/5` in the row of each rated item.",
    "`POST /items/<id>/rating` (`rating`): `\"\"` clears it, `1` to `5` sets it, 303 to `/items/<id>`. Any other value: 400, the item page with `Rating must be a whole number from 1 to 5.`, nothing saved. Unknown id: 404."],
   ["`src/shelf/models.py`", "`src/shelf/store.py`", "`src/shelf/app.py`", "`src/shelf/templates/item.html`", "`src/shelf/templates/index.html`", "`README.md`", "`tests/test_items.py`"],
   "`tests/test_items.py`")

cr("sort-list", "Sort the list",
   "Let me sort my list: newest first, or by title.",
   "The user wants to choose the order of the list page.",
   ["The order is a query parameter of the list page: `?sort=`; the default is the oldest first, as today.",
    "Three orders: oldest, newest, title.",
    "An unknown order is a 400.",
    "The sort links mark the current order with `aria-current`.",
    "The sort combines with the other query parameters of the list page: each keeps the other."],
   ["`GET /?sort=<order>`: `oldest` (id ascending; also when `sort` is absent or empty), `newest` (id descending), `title` (title A to Z ignoring case, ties by id). Any other value: 400, with `Unknown sort: <value>` (escaped).",
    "The list page has `<nav class=\"sort\">` with three links: `Oldest` (`/?sort=oldest`), `Newest` (`/?sort=newest`), `Title` (`/?sort=title`); the current one (`Oldest` when absent) has `aria-current=\"page\"`, no other link of that nav has it.",
    "The sort combines with the list page's other query parameters, when the page has some (in 0.2.0, the status filter and the search): its links keep them, and their links keep the sort."],
   ["`src/shelf/app.py`", "`src/shelf/views.py`", "`src/shelf/templates/index.html`", "`README.md`", "`tests/test_pages.py`"],
   "`tests/test_pages.py`")

cr("duplicate-url", "Refuse a duplicate URL",
   "I keep adding the same book twice. Warn me when a link is already on my shelf.",
   "The user wants an item whose URL is already on the shelf to be refused, with a pointer to the existing item.",
   ["Two URLs are the same after trimming, ignoring the case of the scheme and the host and one trailing `/`; the path stays case-sensitive.",
    "An item with no URL never clashes.",
    "The refusal is a 400 on the list page, with the values entered and a link to the existing item.",
    "The same check applies to the edit form, where an item's own URL is not a clash."],
   ["Adding an item (`POST /items`) whose URL is already another item's: 400, the list page with the values entered and the message `Already on the shelf:` followed by a link to the existing item (`href=\"/items/<id>\"`, its title as the link's text); nothing added. Two URLs are the same when they are equal after trimming, ignoring the case of the scheme and the host and one trailing `/`. An item with no URL never clashes.",
    "The same check on the edit form (`POST /items/<id>/edit`, released in 0.2.0), where an item's own URL is not a clash."],
   ["`src/shelf/models.py`", "`src/shelf/app.py`", "`src/shelf/templates/index.html`", "`src/shelf/templates/edit.html`", "`README.md`", "`tests/test_items.py`"],
   "`tests/test_items.py`")


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


for slug, c in CRS.items():
    d = ROOT / slug
    write(d / "intake" / "request.md", f"# {c['title']}\n\n{c['request']}\n")
    write(d / "01-intent.md", f"# {c['title']}\n\n{c['intent']}\n\nFrom `intake/request.md`.\n")
    write(d / "02-answers.md", "# Answers\n\n" + "".join(f"- {a}\n" for a in c["answers"]))
    done = c["extra"] + [x.format(test=c["test"]) for x in COMMON]
    spec = (f"# {c['title']}\n\n## Change\n\n" + "".join(f"- {b}\n" for b in c["change"])
            + "\n## Files\n\nThe expected footprint; a Coder may add a helper module, never a dependency.\n\n"
            + "".join(f"- {f}\n" for f in c["files"])
            + "\n## Done when\n\n" + "".join(f"- {x}\n" for x in done))
    write(d / "03-change-spec.md", spec)

for slug, ver in (("release-v0-2-0", "0.2.0"), ("release-v0-3-0", "0.3.0")):
    d = ROOT / slug
    t = f"Release v{ver}"
    write(d / "intake" / "request.md", f"# {t}\n\nRelease what is merged as v{ver}.\n")
    write(d / "01-intent.md", f"# {t}\n\nPublish what is merged on `main` as version {ver}, by the project's procedure.\n\nFrom `intake/request.md`.\n")
    write(d / "02-answers.md", "# Answers\n\n- The maintainer approves the release notes before they go anywhere.\n"
          "- No grant at the start: each irreversible action waits for the user.\n")
    write(d / "03-change-spec.md",
          f"# {t}\n\n## Change\n\n- Version: `{ver}`.\n- Scope: everything merged on `main`.\n"
          "- Procedure: `RELEASING.md`, at the repository's root.\n"
          "- The maintainer approves the release notes before they go anywhere.\n\n"
          "## Files\n\nBy `RELEASING.md`:\n\n- `pyproject.toml`\n- `src/shelf/__init__.py`\n- `CHANGELOG.md`\n\n"
          "## Done when\n\n"
          f"- the tag `v{ver}` is on the origin;\n"
          f"- a GitHub release `v{ver}` holds that version's `CHANGELOG.md` section;\n"
          f"- the version `{ver}` is in `pyproject.toml` and `src/shelf/__init__.py`;\n"
          f"- `uv run python scripts/release_check.py` ends with `release check passed` at the tag.\n")
print(len(CRS) + 2, "CRs written")
