PLAN = {
    "README.md": ["UNION"],
    "tests/test_pages.py": ["UNION2"],
    "src/shelf/templates/index.html": ["UNION"],
    "src/shelf/app.py": ['''        status = _query(environ).get("status", "")
        if status and status not in STATUSES:
            return _respond(start_response, 400, views.index(store.load(), f"Unknown status: {status}"))
        query = _query(environ).get("q", "").strip()
        items = [
            i for i in store.load()
            if (not status or i["status"] == status) and query.lower() in i["title"].lower()
        ]
        return _respond(start_response, 200, views.index(items, status=status, query=query))
'''],
    "src/shelf/views.py": [
        '''FILTERS = (("All", ""), ("To read", "to-read"), ("Reading", "reading"), ("Done", "done"))


def _filters(current: str) -> str:
    links = []
    for label, value in FILTERS:
        href = f"/?status={value}" if value else "/"
        mark = ' aria-current="page"' if value == current else ""
        links.append(f'<a href="{href}"{mark}>{label}</a>')
    return '<nav class="filters">' + " ".join(links) + "</nav>"


def index(items: list[dict], error: str = "", values: dict | None = None, status: str = "", query: str = "") -> str:
    values = values or {}
    if query:
        empty = f'No items match "{escape(query)}".'
    elif status:
        empty = "No items with this status."
    else:
        empty = "Nothing on the shelf yet."
''',
        '''        filters=_filters(status),
        q_value=escape(query, quote=True),
''',
    ],
}
