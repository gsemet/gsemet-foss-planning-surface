# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""chantier board: a read-only progress page over .agents/changes, for a phone.

Run:  uv run --script board.py --changes <repo>/.agents/changes [--host 0.0.0.0] [--port 8765]
Pages: /  (board, refreshes every 30 s), /api/status (JSON), /file?p=<path under changes>.
Reads only; writes nothing. No authentication: bind 127.0.0.1 unless the network is private
(home LAN, Tailscale).
"""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

BATCH_DIRS = ("3-requests", "4-batches")  # in-project layout, surface layout
SEVERITY = {"green": "#2e9d5b", "yellow": "#d79b00", "red": "#d1453b", "grey": "#888"}


def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def first_heading(folder: Path) -> str:
    for name in ("01-intent.md", "01-request.md", "03-change-spec.md"):
        f = folder / name
        if f.is_file():
            for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("# "):
                    return re.sub(r"^(Intent|Request|Change Specification):\s*", "", line[2:]).strip()
    intake = folder / "intake"
    if intake.is_dir():
        for f in sorted(intake.glob("*.md")):
            text = f.read_text(encoding="utf-8", errors="replace").strip()
            if text:
                return text.splitlines()[0].lstrip("# ")[:160]
    return folder.name


def tail_events(path: Path, n: int) -> list[dict]:
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-n:]
    out = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def collect(changes: Path) -> dict:
    batches = []
    for d in BATCH_DIRS:
        root = changes / d
        if not root.is_dir():
            continue
        for b in sorted(root.iterdir(), reverse=True):
            st = read_json(b / "STATUS.json")
            if not st:
                continue
            st["_dir"] = b.relative_to(changes).as_posix()
            st["_events"] = [
                e for e in tail_events(b / "events.jsonl", 60) if e.get("kind") not in ("heartbeat", "cost")
            ][-12:]
            batches.append(st)
    backlog = []
    bl = changes / "2-backlog"
    if bl.is_dir():
        for prio in sorted(p for p in bl.iterdir() if p.is_dir()):
            for item in sorted(i for i in prio.iterdir() if i.is_dir()):
                backlog.append(
                    {
                        "priority": prio.name,
                        "item": item.name,
                        "title": first_heading(item),
                        "spec": (item / "03-change-spec.md").is_file(),
                        "dir": item.relative_to(changes).as_posix(),
                    }
                )
    inbox = []
    ib = changes / "1-inbox"
    if ib.is_dir():
        for item in sorted(i for i in ib.iterdir() if i.is_dir()):
            inbox.append({"item": item.name, "title": first_heading(item), "dir": item.relative_to(changes).as_posix()})
    return {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "batches": batches,
        "backlog": backlog,
        "inbox": inbox,
    }


def ago(ts: str | None) -> str:
    if not ts:
        return "-"
    try:
        t = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return ts
    m = int((datetime.now(timezone.utc) - t).total_seconds() // 60)
    return f"{m} min ago" if m < 120 else f"{m // 60} h ago"


def flink(path: str, label: str) -> str:
    return f'<a href="/file?p={quote(path)}">{html.escape(label)}</a>'


def render(data: dict) -> str:
    e = html.escape
    parts = []
    for b in data["batches"]:
        if b.get("state") in ("closed",) and len(data["batches"]) > 1:
            continue
        spent, budget = b.get("spent_usd") or 0, b.get("budget_usd") or 0
        pct = min(100, int(100 * spent / budget)) if budget else 0
        rows = []
        for c in b.get("crs", []):
            color = SEVERITY.get(c.get("severity"), "#888")
            pr = c.get("pr")
            pr_html = f'<a href="{e(pr)}">#{e(pr.rstrip("/").split("/")[-1])}</a>' if pr else "-"
            spec = c.get("specification")
            spec_path = (Path(b["_dir"]) / spec).as_posix() if spec else None
            title = e(re.sub(r"^Change Specification:\s*", "", c.get("title", "")))
            if spec_path:
                title = flink(spec_path, re.sub(r"^Change Specification:\s*", "", c.get("title", "")))
            blocked = f'<div class="blk">⛔ {e(str(c["blocked"]))}</div>' if c.get("blocked") else ""
            waits = f'<div class="muted">waits: {e(", ".join(map(str, c["waits"])))}</div>' if c.get("waits") else ""
            silent = c.get("silent_minutes")
            silent_html = f'<span class="muted"> · silent {silent} min</span>' if silent is not None else ""
            rows.append(
                f'<div class="cr"><span class="dot" style="background:{color}"></span>'
                f'<div class="crbody"><div><b>{e(c.get("cr", ""))}</b> {title}</div>'
                f'<div class="muted">{e(c.get("step") or c.get("state", ""))} · round {e(str(c.get("round", "-")))}'
                f" · ${c.get('cost_usd') or 0:.2f} · PR {pr_html}{silent_html}</div>{blocked}{waits}</div></div>"
            )
        events = "".join(
            f'<li><span class="muted">{e(ev.get("t", "")[11:16])}</span> {e(ev.get("actor", ""))} '
            f'<b>{e(ev.get("kind", ""))}</b> {e(ev.get("cr") or "")}</li>'
            for ev in reversed(b["_events"])
        )
        asks = b.get("asks_unread") or 0
        parts.append(
            f'<section><h2>{e(b.get("batch", ""))} <span class="pill">{e(b.get("state", ""))}</span>'
            f'<span class="pill">{e(b.get("mode", ""))}</span><span class="pill">{e(b.get("steering", ""))}</span></h2>'
            f'<div class="bar"><div style="width:{pct}%"></div></div>'
            f'<div class="muted">${spent:.2f} of ${budget:.0f} · heartbeat {ago(b.get("heartbeat"))}'
            f'{" · <b>" + str(asks) + " question(s) waiting</b>" if asks else ""}</div>'
            f'{"".join(rows) or "<p class=muted>No CR.</p>"}'
            f'<details><summary>Recent events</summary><ul class="ev">{events}</ul></details></section>'
        )
    if not parts:
        parts.append('<section><p class="muted">No batch.</p></section>')
    if data["inbox"]:
        items = "".join(f'<li>{flink(i["dir"], i["item"])} <span class="muted">{e(i["title"])}</span></li>' for i in data["inbox"])
        parts.append(f"<section><h2>Inbox ({len(data['inbox'])})</h2><ul>{items}</ul></section>")
    by_prio: dict[str, list] = {}
    for i in data["backlog"]:
        by_prio.setdefault(i["priority"], []).append(i)
    for prio, items in by_prio.items():
        lis = "".join(
            f'<li>{flink(i["dir"], i["item"])}{" <span class=pill>spec</span>" if i["spec"] else ""}'
            f'<div class="muted">{e(i["title"][:200])}</div></li>'
            for i in items
        )
        parts.append(f"<details class='sec'><summary><b>Backlog {e(prio)}</b> ({len(items)})</summary><ul>{lis}</ul></details>")
    return PAGE.format(body="".join(parts), generated=e(data["generated"]))


PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="30">
<title>chantier board</title><style>
:root{{color-scheme:light dark;--bg:#fafafa;--card:#fff;--fg:#222;--mut:#777;--line:#e4e4e4}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151515;--card:#1f1f1f;--fg:#e8e8e8;--mut:#999;--line:#333}}}}
body{{font:15px/1.4 system-ui,sans-serif;background:var(--bg);color:var(--fg);margin:0;padding:12px;max-width:760px;margin:auto}}
h1{{font-size:18px;margin:4px 0 12px}} h2{{font-size:16px;margin:0 0 8px}}
section,.sec{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin-bottom:12px}}
.pill{{font-size:11px;font-weight:normal;border:1px solid var(--line);border-radius:9px;padding:1px 7px;margin-left:6px}}
.bar{{height:6px;background:var(--line);border-radius:3px;margin:6px 0}} .bar div{{height:100%;background:#4a7fd4;border-radius:3px}}
.cr{{display:flex;gap:10px;padding:8px 0;border-top:1px solid var(--line)}} .crbody{{flex:1;min-width:0}}
.dot{{width:10px;height:10px;border-radius:50%;margin-top:6px;flex:none}}
.muted{{color:var(--mut);font-size:13px}} .blk{{color:#d1453b;font-size:13px}}
a{{color:#4a7fd4;text-decoration:none}} ul{{padding-left:18px;margin:6px 0}} li{{margin:4px 0}}
.ev{{list-style:none;padding:0;font-size:13px}} summary{{cursor:pointer}} pre{{white-space:pre-wrap;word-wrap:break-word}}
</style></head><body><h1>chantier board</h1>{body}
<p class="muted">Updated {generated} · refreshes every 30 s · <a href="/api/status">JSON</a></p></body></html>"""


def make_handler(changes: Path):
    root = changes.resolve()

    class Handler(BaseHTTPRequestHandler):
        def send(self, code: int, body: str, ctype: str) -> None:
            raw = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", f"{ctype}; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self) -> None:  # noqa: N802
            url = urlparse(self.path)
            if url.path == "/":
                self.send(200, render(collect(root)), "text/html")
            elif url.path == "/api/status":
                self.send(200, json.dumps(collect(root), indent=2, ensure_ascii=False), "application/json")
            elif url.path == "/file":
                rel = parse_qs(url.query).get("p", [""])[0]
                target = (root / rel).resolve()
                if not target.is_relative_to(root) or not target.exists():
                    self.send(404, "not found", "text/plain")
                elif target.is_dir():
                    lis = "".join(
                        f"<li>{flink(c.relative_to(root).as_posix(), c.name + ('/' if c.is_dir() else ''))}</li>"
                        for c in sorted(target.iterdir())
                    )
                    self.send(200, PAGE.format(body=f"<section><h2>{html.escape(rel)}</h2><ul>{lis}</ul></section>",
                                               generated=""), "text/html")
                else:
                    text = target.read_text(encoding="utf-8", errors="replace")
                    body = f'<section><h2>{html.escape(rel)}</h2><pre>{html.escape(text)}</pre></section>'
                    self.send(200, PAGE.format(body=body, generated=""), "text/html")
            else:
                self.send(404, "not found", "text/plain")

        def log_message(self, *args) -> None:
            pass

    return Handler


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--changes", default=".agents/changes", help="the changes folder to show")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    changes = Path(args.changes)
    if not changes.is_dir():
        raise SystemExit(f"no changes folder at {changes.resolve()}")
    server = ThreadingHTTPServer((args.host, args.port), make_handler(changes))
    print(f"chantier board on http://{args.host}:{args.port}/ over {changes.resolve()}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
