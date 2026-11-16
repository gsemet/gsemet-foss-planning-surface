PLAN = {
    "README.md": ["UNION"],
    "tests/test_pages.py": ["UNION2"],
    "src/shelf/templates/index.html": ['''$filters
$sort_nav
    <form method="get" action="/">
      <input name="q" value="$q_value">$hidden <button type="submit">Search</button>
    </form>
'''],
    "src/shelf/app.py": ['''        params = _query(environ)
        status = params.get("status", "")
        sort = params.get("sort", "") or "oldest"
        query = params.get("q", "").strip()
        if status and status not in STATUSES:
            return _respond(start_response, 400, views.index(store.load(), f"Unknown status: {status}"))
        if sort not in SORTS:
            return _respond(start_response, 400, views.index(store.load(), f"Unknown sort: {sort}"))
        items = [
            i for i in store.load()
            if (not status or i["status"] == status) and query.lower() in i["title"].lower()
        ]
        items = sorted(items, key=SORTS[sort])
        return _respond(start_response, 200, views.index(items, status=status, query=query, sort=sort))
'''],
    "src/shelf/views.py": [
        '''def _rated(entry: dict) -> str:
    return f' <span class="rating">{entry["rating"]}/5</span>' if entry.get("rating") else ""


def _href(status: str = "", query: str = "", sort: str = "oldest", keep_sort: bool = False) -> str:
    """The list page's address with the parameters in play (the default order only when asked)."""
    params = {}
    if status:
        params["status"] = status
    if query:
        params["q"] = query
    if keep_sort or sort != "oldest":
        params["sort"] = sort
    return escape("/?" + urlencode(params) if params else "/", quote=True)


FILTERS = (("All", ""), ("To read", "to-read"), ("Reading", "reading"), ("Done", "done"))
ORDERS = (("Oldest", "oldest"), ("Newest", "newest"), ("Title", "title"))


def _filters(current: str, query: str, sort: str) -> str:
    links = []
    for label, value in FILTERS:
        mark = ' aria-current="page"' if value == current else ""
        links.append(f'<a href="{_href(value, query, sort)}"{mark}>{label}</a>')
    return '<nav class="filters">' + " ".join(links) + "</nav>"


def _sort_nav(current: str, status: str, query: str) -> str:
    links = []
    for label, value in ORDERS:
        mark = ' aria-current="page"' if value == current else ""
        links.append(f'<a href="{_href(status, query, value, True)}"{mark}>{label}</a>')
    return '<nav class="sort">' + " ".join(links) + "</nav>"


def _hidden(status: str, sort: str) -> str:
    """The search form keeps the status filter and the order."""
    fields = {"status": status, "sort": sort if sort != "oldest" else ""}
    return "".join(f'<input type="hidden" name="{k}" value="{escape(v, quote=True)}">' for k, v in fields.items() if v)


def index(
    items: list[dict], error: str = "", values: dict | None = None, status: str = "", query: str = "", sort: str = "oldest"
) -> str:
''',
        '''        filters=_filters(status, query, sort),
        sort_nav=_sort_nav(sort, status, query),
        q_value=escape(query, quote=True),
        hidden=_hidden(status, sort),
''',
    ],
}
