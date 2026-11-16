"""One-off generator of docs/demo/ (kept in the CR's work folder, not committed)."""

from __future__ import annotations

import hashlib
import json
import shutil
import struct
import sys
import zlib
from pathlib import Path

OUT = Path(sys.argv[1])
if OUT.exists():
    shutil.rmtree(OUT)

SHOP = "https://github.com/example/shop-api"


def w(path: str, text: str) -> None:
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))


def j(path: str, data: object) -> None:
    w(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def cr(
    base: str,
    title: str,
    intent: str | None = None,
    answers: str | None = None,
    spec: str | None = None,
    request: str | None = None,
    summary: dict | None = None,
    late: bool = False,
    extra: dict[str, str] | None = None,
) -> None:
    files: dict[str, str] = {}
    if request:
        files["intake/request.md"] = f"# {title}\n\n{request}\n"
    if intent:
        files["01-intent.md"] = f"# {title}\n\n{intent}\n"
    if answers:
        files["02-answers.md"] = f"# Answers\n\n{answers}\n"
    if spec:
        files["03-change-spec.md"] = f"# Change Specification: {title}\n\n{spec}\n"
    for name, text in files.items():
        w(f"{base}/{name}", text)
    for name, text in (extra or {}).items():
        w(f"{base}/{name}", text)
    if summary:
        sources = {n: sha(t) for n, t in sorted(files.items()) if n.endswith(".md")}
        if late and sources:
            first = next(iter(sources))
            sources[first] = "0" * 64
        summary = {"schema": 1, "title": title, "sources": sources, **summary}
        summary.setdefault("summarized", "2026-06-17T16:05:00Z")
        j(f"{base}/summary.json", summary)


def GH(n: int, repo: str = SHOP) -> dict:
    return {"kind": "github", "ref": f"#{n}", "url": f"{repo}/issues/{n}"}


def JIRA(k: str) -> dict:
    return {"kind": "jira", "ref": k, "url": f"https://example.atlassian.net/browse/{k}"}


VERBAL = {"kind": "verbal"}

# ---------------------------------------------------------------- the surface

w(
    "README.md",
    """# The demo planning surface

A fictional planning surface, kept in the repository for one purpose: `just docs-screenshots`
copies it to a temporary folder, starts the web board on the copy and takes the screenshots of
`docs/web-board/`. Nothing else reads it.

- It is **not** a planning folder of this repository: chantier's own planning is `.agents/changes/`.
  This folder has no `.agents/changes/` and the CLI never discovers it from the repository's root.
- Everything in it is made up: the shop, its people, its pull requests (`example` URLs that no
  screenshot follows) and its dates (the capture fixes the clock at `2026-06-18T10:30:00Z`).
- It is a multi-project planning surface, as [planning-modes](../planning-modes.md) describes:
  `projects/<name>/` with `project.md`, `checkout.yml` and `changes/`.

| Project | What it shows |
| --- | --- |
| `shop-api` | a batch running in stack mode, with every state a CR can be in; an inbox, a backlog from P1 to P4 (P3 left empty), `3-ready`, a CR with sub-folders |
| `mobile-app` | no batch running; an inbox; the last merged CRs in `5-archives/` |
| `docs-portal` | a small project, for the "All projects" table |

The record files a running batch keeps (`batch.json`, `events.jsonl`, `seat.json`) are kept here
too, in the format the server reads. The capture script adds what git does not hold: it initialises
a git repository in its copy and writes the autosync tool's state files there (a group waiting for
an approval), so that the board's pill has a fixed state to draw.
""",
)

w(
    "AGENTS.md",
    """# Demo surface

This is a fictional planning surface. Its sync is handled by the autosync tool described in
`.agents/guidelines/autosync.guidelines.md`: run `scripts/ai-autosync-git.py` as that file says.
""",
)
w(
    ".agents/guidelines/autosync.guidelines.md",
    """# Autosync (demo)

In the demo, `scripts/ai-autosync-git.py` is a stub that does nothing: the capture script writes
the state the board shows.
""",
)
w(
    "scripts/ai-autosync-git.py",
    '''# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""A stub of the surface's autosync tool, for the demo: it does nothing and ends at once. The
board runs it for `join`, `start`, `stop` and `approve`; the demo's state is written by the
capture script, and nothing here touches a git remote."""

import sys

print("demo autosync stub:", " ".join(sys.argv[1:]))
''',
)

for name, remote in (
    ("shop-api", f"{SHOP}.git"),
    ("mobile-app", "https://github.com/example/shop-mobile.git"),
    ("docs-portal", "https://github.com/example/docs-portal.git"),
):
    w(
        f"projects/{name}/project.md",
        f"# {name}\n\nA fictional project of the demo.\n\n- Remote: {remote}\n"
        "- Default branch: main\n- Archive in the PR: yes\n",
    )
    w(f"projects/{name}/checkout.yml", "repo: .repo\nworktrees: .worktrees\n")

# ---------------------------------------------------------------- shop-api

P = "projects/shop-api/changes"
CLOCK_BATCH = "2026-06-18T07:42:10Z"

cr(f"{P}/1-inbox/dark-mode-admin", "Dark mode for the admin console",
   request="The support team works late and asks for a dark theme in the admin console.",
   summary={"summary": "A dark theme for the admin console, asked by the support team.",
            "origin": VERBAL, "labels": ["admin"]})
cr(f"{P}/1-inbox/rate-limit-public-api", "Rate limit the public API",
   request="A partner's script hammered `/v1/products` last Friday. Add a per-key rate limit and "
   "answer 429 with a `Retry-After` header.",
   summary={"summary": "Per-key rate limit on the public API, 429 with Retry-After.",
            "origin": GH(58), "labels": ["api", "perf"], "group": "api-hardening"})
cr(f"{P}/1-inbox/csv-product-import", "Import products from a CSV file",
   request="Merchants want to load their catalogue from a spreadsheet instead of one product at a time.",
   summary={"summary": "Bulk product import from a CSV file, with a dry run that lists the errors.",
            "origin": JIRA("SHOP-212"), "labels": ["admin"]})
cr(f"{P}/1-inbox/typo-confirmation-email", "Typo in the order confirmation email",
   request="\"Thank you for your ordre\" in the footer of the confirmation email.",
   summary={"summary": "Fix the typo in the confirmation email's footer.",
            "origin": GH(61), "labels": ["bug"]})

cr(f"{P}/2-backlog/P1/guest-checkout", "Guest checkout without an account",
   intent="Visitors leave at the account-creation step. A guest should be able to pay with only an "
   "email address, and be offered an account afterwards.",
   answers="- Q: keep the guest's email? A: yes, for the receipt, 30 days.\n"
   "- Q: pay in one page? A: yes, the same page as signed-in customers.",
   request="Conversion drops by a third at the account step.",
   summary={"summary": "Let a visitor pay with an email address only, then offer an account.",
            "origin": JIRA("SHOP-190"), "labels": ["checkout"], "group": "checkout-polish"})
cr(f"{P}/2-backlog/P1/stock-alerts", "Alert the merchant when stock runs low",
   request="Merchants find out about an empty shelf from customers.",
   summary={"summary": "An email to the merchant when a product's stock falls under its threshold.",
            "origin": VERBAL, "labels": ["admin"]})
cr(f"{P}/2-backlog/P2/saved-addresses", "Saved delivery addresses",
   intent="A returning customer retypes the same address at each order.",
   answers="- Q: how many addresses? A: up to five.",
   spec="A signed-in customer can save up to five delivery addresses, pick one at checkout, and "
   "delete them from the account page.\n\nIt does not change guest checkout.",
   summary={"summary": "Up to five saved delivery addresses, picked at checkout.",
            "origin": GH(44), "labels": ["checkout"], "group": "checkout-polish"})
cr(f"{P}/2-backlog/P2/product-reviews", "Customer reviews on product pages",
   request="Marketing wants stars and short reviews under each product.",
   summary={"summary": "Star ratings and short reviews on product pages, moderated by the team.",
            "origin": VERBAL, "labels": ["search"]})
cr(f"{P}/2-backlog/P4/archive-old-orders", "Archive orders older than five years",
   request="The orders table is the largest of the database.",
   summary={"summary": "Move orders older than five years to cold storage.",
            "origin": GH(33), "labels": ["perf"]})

cr(f"{P}/3-ready/wishlist", "A wishlist for signed-in customers",
   intent="Customers keep a list of products they may buy later.",
   answers="- Q: shareable? A: no, private for now.",
   spec="A signed-in customer adds a product to a private wishlist from its page and sees the "
   "list under their account.\n\nA product that goes out of stock stays on the list, marked.",
   summary={"summary": "A private wishlist under the customer's account.",
            "origin": JIRA("SHOP-201"), "labels": ["checkout"]})
cr(f"{P}/3-ready/coupon-codes", "Coupon codes at checkout",
   intent="Marketing runs campaigns with a code and has no way to apply one.",
   answers="- Q: stack with other discounts? A: no, one code per order.\n"
   "- Q: expiry? A: a date, set when the code is created.",
   summary={"summary": "One coupon code per order, with an expiry date.",
            "origin": VERBAL, "labels": ["checkout"]},
   late=True)

PNG_W, PNG_H = 320, 180


def png() -> bytes:
    rows = []
    for y in range(PNG_H):
        row = bytearray([0])
        for x in range(PNG_W):
            if 24 <= x < 296 and 20 <= y < 38:
                px = (60, 90, 160)
            elif 24 <= x < 296 and 52 <= y < 120 and (x - 24) % 96 < 88:
                px = (226, 232, 240)
            elif 24 <= x < 150 and 134 <= y < 154:
                px = (34, 139, 94)
            else:
                px = (250, 250, 252)
            row += bytes(px)
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(kind: bytes, data: bytes) -> bytes:
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    header = struct.pack(">IIBBBBB", PNG_W, PNG_H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


B = f"{P}/4-batch"

SPECS = {
    "141-order-tax-rules": (
        "Order totals use the tax rules of the delivery country",
        "Totals use one flat rate. Orders delivered abroad must use the delivery country's rate.",
        "The order total applies the tax rate of the delivery country, from the rates table, "
        "and shows the rate on the receipt.\n\nIt does not change prices shown on product pages.",
        "3-done"),
    "142-persistent-cart": (
        "The cart keeps its items across sessions",
        "A customer who closes the tab loses the cart.",
        "The cart is stored on the server for signed-in customers and in a cookie for guests, and "
        "both merge at sign-in.\n\nA cart untouched for 30 days is emptied.",
        "2-actives"),
    "143-search-in-stock-first": (
        "Product search ranks in-stock items first",
        "Search results show sold-out products at the top.",
        "Search ranks products in stock before the others, keeping the relevance order inside each "
        "group.\n\nA sold-out product is marked and still found.",
        "2-actives"),
    "144-webhook-backoff": (
        "Payment webhooks retry with a back-off",
        "A failing endpoint of a merchant receives a retry every second.",
        "A webhook that fails is retried after 1 minute, 5 minutes and 30 minutes, then given up "
        "and listed in the admin console.\n\nIt does not change the payload.",
        "2-actives"),
    "145-delivery-dates": (
        "The checkout page shows delivery dates",
        "Customers ask when their order arrives, and the page does not say.",
        "The checkout page shows an estimated delivery date for each shipping method, computed "
        "from the carrier's lead time and the warehouse's cut-off hour.\n\nA date falls on a "
        "working day.",
        "2-actives"),
    "146-payment-api-v3": (
        "Move the payment provider integration to its v3 API",
        "The provider ends the v2 API in September.",
        "The integration calls the provider's v3 API for payments and refunds.\n\n"
        "Refunds of orders paid before the switch keep using v2 for 30 days.",
        "2-actives"),
    "147-admin-csv-export": (
        "Export the orders list as a CSV file",
        "The accountant copies the orders list by hand each month.",
        "The admin console exports the filtered orders list as a CSV file, with one line per "
        "order and the columns of the list.",
        "1-pending"),
    "148-localised-receipts": (
        "Email receipts are localised",
        "Receipts are always in English.",
        "The receipt email uses the language of the customer's account, with English as the "
        "fallback.",
        "1-pending"),
    "149-negative-stock-fix": (
        "Fix: stock goes negative after a cancelled order",
        "Cancelling an order twice gives the stock back twice.",
        "Cancelling an order gives its stock back once, whatever the number of cancel requests.",
        "2-actives"),
}
for slug, (title, intent, spec, state) in SPECS.items():
    extra = {}
    if slug == "145-delivery-dates":
        extra = {
            "work/r1.md": "# Round 1\n\nThe date is computed from the carrier's lead time. "
            "The cut-off hour is read from the warehouse settings.\n\nGates: `just check` pass.\n",
            "work/r2.md": "# Round 2\n\nWorking days skip the weekend and the public holidays "
            "of the delivery country.\n\nGates: `just check` pass, one test failing on the "
            "year's last day.\n",
        }
    cr(f"{B}/{state}/{slug}", title, intent=intent,
       answers="- Q: in scope for this release? A: yes." if slug != "148-localised-receipts" else None,
       spec=spec, request=intent if slug == "145-delivery-dates" else None, extra=extra)
ev_dir = OUT / f"{B}/2-actives/145-delivery-dates/evidence"
ev_dir.mkdir(parents=True, exist_ok=True)
(ev_dir / "checkout-mock.png").write_bytes(png())
w(f"{B}/2-actives/145-delivery-dates/evidence/notes.md",
  "# Evidence\n\nThe mock-up of the checkout page, with the delivery date under each shipping "
  "method.\n\n| Method | Lead time |\n| --- | --- |\n| Standard | 3 days |\n| Express | 1 day |\n")
j(f"{B}/1-pending/147-admin-csv-export/depends.json", {"after": ["CR-144"]})
j(f"{B}/2-actives/143-search-in-stock-first/depends.json", {"after": ["CR-142"]})
j(f"{B}/2-actives/145-delivery-dates/depends.json", {"after": ["CR-143"]})


def PR(n: int) -> str:
    return f"{SHOP}/pull/{n}"


def entry(n: int, slug: str, state_dir: str, status: str, order: int, round_: int,
          cost: float | None, **kw: object) -> dict:
    title = SPECS[slug][0]
    d: dict = {
        "id": f"CR-{n}",
        "title": f"Change Specification: {title}",
        "kind": "change",
        "status": status,
        "order": order,
        "path": f"4-batch/{state_dir}/{slug}",
        "specification": "03-change-spec.md",
        "round": round_,
        "agent": None,
        "pr": None,
        "head": None,
        "branch": f"chantier/batch-03/cr-{n}-{slug.split('-', 1)[1]}"[:62].rstrip("-"),
        "worktree": f"/work/shop-api.worktrees/batch-03-CR-{n}",
        "notes": [],
        "updated": "2026-06-18T10:20:00Z",
        "after": [],
        "blocked_reason": None,
        "cost_usd": cost,
    }
    d.update(kw)
    return d


crs = [
    entry(141, "141-order-tax-rules", "3-done", "merged", 1, 2, 6.82, pr=PR(12),
          merged_at="2026-06-18T09:12:40Z", updated="2026-06-18T09:12:40Z",
          head="a1f03c9d2e7b45668e0f19b3c4d5a6e7f8091a2b", rounds=3, agent="a1e3"),
    entry(142, "142-persistent-cart", "2-actives", "ready", 2, 2, 9.35, pr=PR(14), stacked=True,
          head="b27d4e1f90a8c3562d7e84f1a0b9c8d7e6f5a4b3", updated="2026-06-18T09:58:12Z"),
    entry(143, "143-search-in-stock-first", "2-actives", "ready", 3, 1, 8.10, pr=PR(15),
          stacked=True, after=["CR-142"],
          head="c38e5f2a01b9d4673e8f95a2b1c0d9e8f7a6b5c4", updated="2026-06-18T10:05:31Z"),
    entry(144, "144-webhook-backoff", "2-actives", "working", 4, 2, 11.60, pr=PR(16),
          agent="a4c7", head="d49f6a3b12c0e5784f9aa6b3c2d1e0f9a8b7c6d5",
          updated="2026-06-18T10:27:50Z"),
    entry(145, "145-delivery-dates", "2-actives", "working", 5, 3, 14.85, after=["CR-143"],
          agent="a5d8", updated="2026-06-18T10:26:15Z", rounds=3),
    entry(146, "146-payment-api-v3", "2-actives", "blocked", 6, 1, 5.20,
          blocked_reason="question: should refunds of orders paid before the switch keep the v2 "
          "endpoint for 30 days, or move to v3 at once?",
          updated="2026-06-18T10:11:03Z"),
    entry(147, "147-admin-csv-export", "1-pending", "queued", 7, 0, None, after=["CR-144"]),
    entry(148, "148-localised-receipts", "1-pending", "queued", 8, 0, None),
    entry(149, "149-negative-stock-fix", "2-actives", "ready", 9, 1, 3.45, kind="fix",
          fix_for="CR-141", pr=PR(17),
          head="e5a07b4c23d1f6895a0bb7c4d3e2f1a0b9c8d7e6", updated="2026-06-18T10:14:48Z"),
]

foreman = "local_7c1d92aa-3b40-4e55-9d63-1f2a8c4b5e07"
j(f"{B}/batch.json", {
    "id": "batch-03",
    "version": "0.9.0",
    "created": CLOCK_BATCH,
    "status": "running",
    "host": "claude",
    "mode": "stack",
    "slots": 4,
    "budget_usd": 120.0,
    "spent_usd": 63.18,
    "unpriced": {},
    "foreman": foreman,
    "foreman_epoch": 1,
    "foreman_transcript": "5b2e8f10-77a3-4c19-8d02-aa31c0de9f11",
    "foreman_transcripts": ["5b2e8f10-77a3-4c19-8d02-aa31c0de9f11"],
    "foreman_claims": [
        {"transcript": "5b2e8f10-77a3-4c19-8d02-aa31c0de9f11", "since": "2026-06-18T07:43:02Z"}
    ],
    "steering": "foreman",
    "chief_transcript": "0e9a4c63-18d5-4b7a-b2f1-6d3c7a8e9f20",
    "chief_transcripts": ["0e9a4c63-18d5-4b7a-b2f1-6d3c7a8e9f20"],
    "stack_agent": "af3b19",
    "heartbeat": "2026-06-18T10:28:40Z",
    "heartbeat_stopped": None,
    "settings": {"default_branch": "main", "remote": "origin", "max_rounds": 3},
    "orders": [
        {"id": "O-1", "kind": "budget", "cr": "-", "note": "120",
         "sent": "2026-06-18T07:50:12Z", "done": "2026-06-18T07:50:30Z", "applied": True},
        {"id": "O-2", "kind": "rounds", "cr": "CR-145", "note": "3",
         "sent": "2026-06-18T09:30:00Z", "done": "2026-06-18T09:30:21Z", "applied": True},
    ],
    "asks": [
        {"id": "A-3", "text": "blocked CR-146: should refunds keep the v2 endpoint for 30 days?",
         "sent": "2026-06-18T10:11:05Z", "read": None}
    ],
    "crs": crs,
    "release": None,
})

ev: list[dict] = []


def e(t: str, actor: str, kind: str, cr_: str | None = None, **kw: object) -> None:
    ev.append({"t": t, "actor": actor, "kind": kind, "cr": cr_, **kw})


e("2026-06-18T07:42:10Z", "chief-of-staff", "open", None, crs=[c["id"] for c in crs])
e("2026-06-18T07:43:02Z", "foreman", "foreman", None, session=foreman, epoch=1)
for c in crs:
    e("2026-06-18T07:42:10Z", "chief-of-staff", "add", c["id"], title=c["title"], path=c["path"])
e("2026-06-18T07:50:12Z", "chief-of-staff", "order", None, order="O-1", order_kind="budget", note="120")
e("2026-06-18T07:55:20Z", "foreman", "take", "CR-141")
e("2026-06-18T08:03:44Z", "driver", "round", "CR-141", round=1, note="round 1: the rates table and the totals")
e("2026-06-18T08:31:09Z", "driver", "round", "CR-141", round=2, note="round 2: the receipt shows the rate")
e("2026-06-18T08:52:30Z", "driver", "gate", "CR-141", result="pass", head=crs[0]["head"], command="just check")
e("2026-06-18T08:55:02Z", "driver", "ship", "CR-141", pr=PR(12), base="main", head=crs[0]["head"])
e("2026-06-18T09:02:17Z", "driver", "verdict", "CR-141", result="VERIFIED", head=crs[0]["head"])
e("2026-06-18T09:03:00Z", "driver", "handback", "CR-141", result="ready", note=PR(12))
e("2026-06-18T09:12:40Z", "chief-of-staff", "order", "CR-141", order="O-4", order_kind="merged", note=PR(12))
e("2026-06-18T08:05:10Z", "foreman", "take", "CR-142")
e("2026-06-18T08:44:50Z", "driver", "round", "CR-142", round=1, note="round 1: the server-side cart")
e("2026-06-18T09:24:31Z", "driver", "round", "CR-142", round=2, note="round 2: merge the guest cart at sign-in")
e("2026-06-18T09:50:44Z", "driver", "ship", "CR-142", pr=PR(14), base="main", head=crs[1]["head"])
e("2026-06-18T09:57:30Z", "driver", "verdict", "CR-142", result="VERIFIED", head=crs[1]["head"])
e("2026-06-18T09:58:12Z", "driver", "handback", "CR-142", result="ready", note=PR(14))
e("2026-06-18T08:09:05Z", "foreman", "take", "CR-143")
e("2026-06-18T09:41:12Z", "driver", "round", "CR-143", round=1, note="round 1: ranking by stock, then by relevance")
e("2026-06-18T10:01:20Z", "driver", "ship", "CR-143", pr=PR(15), base="CR-142", head=crs[2]["head"])
e("2026-06-18T10:04:55Z", "driver", "verdict", "CR-143", result="VERIFIED", head=crs[2]["head"])
e("2026-06-18T10:05:31Z", "driver", "handback", "CR-143", result="ready", note=PR(15))
e("2026-06-18T08:20:00Z", "foreman", "take", "CR-146")
e("2026-06-18T10:09:40Z", "driver", "round", "CR-146", round=1, note="round 1: payments on v3, refunds open")
e("2026-06-18T10:11:03Z", "driver", "handback", "CR-146", result="blocked", note=crs[5]["blocked_reason"])
e("2026-06-18T10:11:05Z", "foreman", "ask", None, ask="A-3", text="blocked CR-146: should refunds keep the v2 endpoint for 30 days?")
e("2026-06-18T09:30:00Z", "chief-of-staff", "order", "CR-145", order="O-2", order_kind="rounds", note="3")
e("2026-06-18T09:20:10Z", "foreman", "take", "CR-145")
e("2026-06-18T09:49:02Z", "driver", "round", "CR-145", round=1, note="round 1: the date from the carrier's lead time")
e("2026-06-18T10:08:18Z", "driver", "round", "CR-145", round=2, note="round 2: working days and holidays")
e("2026-06-18T10:26:15Z", "driver", "round", "CR-145", round=3, note="round 3: the cut-off hour, last round")
e("2026-06-18T09:35:00Z", "foreman", "take", "CR-144")
e("2026-06-18T09:58:40Z", "driver", "round", "CR-144", round=1, note="round 1: the retry schedule")
e("2026-06-18T10:15:09Z", "driver", "ship", "CR-144", pr=PR(16), base="CR-143", head=crs[3]["head"])
e("2026-06-18T10:27:50Z", "driver", "round", "CR-144", round=2, note="round 2: the admin list of given-up webhooks")
e("2026-06-18T10:10:00Z", "foreman", "take", "CR-149")
e("2026-06-18T10:13:30Z", "driver", "verdict", "CR-149", result="VERIFIED", head=crs[8]["head"])
e("2026-06-18T10:14:48Z", "driver", "handback", "CR-149", result="ready", note=PR(17))
e("2026-06-18T10:20:30Z", "chief-of-staff", "note", "CR-145", note="the user: the express date must not promise Sunday")
e("2026-06-18T10:28:40Z", "foreman", "heartbeat", None)
ev.sort(key=lambda x: x["t"])
w(f"{B}/events.jsonl", "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in ev))
j(f"{P}/seat.json", {
    "session": "local_a8f51c20-6e0b-4d3a-91c7-3b5e2d8f4a60",
    "env": "desktop",
    "title": "Chief of Staff - shop-api",
})


def archive(proj: str, stamp: str, n: int, slug: str, title: str, batch: str, pr: str, cost: float) -> None:
    base = f"projects/{proj}/changes/5-archives/{stamp}-{n}-{slug}"
    j(f"{base}/STATUS.json", {
        "schema": 3, "cr": f"CR-{n}", "title": f"Change Specification: {title}",
        "state": "merged", "batch": batch, "pr": {"url": pr}, "cost_usd": cost,
    })
    w(f"{base}/delivery.md", f"# Delivery\n\n{title}.\n\n- PR: {pr}\n- Batch: {batch}\n")
    w(f"{base}/03-change-spec.md", f"# Change Specification: {title}\n\n{title}.\n")


archive("shop-api", "260611-1632", 138, "newsletter-opt-in", "A newsletter opt-in at checkout", "batch-02", PR(9), 7.40)
archive("shop-api", "260611-1648", 139, "invoice-pdf", "Invoices are downloadable as PDF files", "batch-02", PR(10), 10.95)
archive("shop-api", "260611-1655", 140, "slow-product-list", "The product list loads in under a second", "batch-02", PR(11), 12.30)

# ---------------------------------------------------------------- mobile-app

M = "projects/mobile-app/changes"
MA = "https://github.com/example/shop-mobile"
cr(f"{M}/1-inbox/biometric-login", "Sign in with a fingerprint or a face",
   request="Customers ask to skip the password on their phone.",
   summary={"summary": "Biometric sign-in as an option, with the password as the fallback.",
            "origin": GH(17, MA), "labels": ["login"]})
cr(f"{M}/1-inbox/offline-cart", "The cart works offline",
   request="On the train the app shows an error instead of the cart.",
   summary={"summary": "Keep the cart readable and editable without a network.",
            "origin": VERBAL, "labels": ["offline"]})
cr(f"{M}/1-inbox/push-order-updates", "Push notifications for order updates",
   request="Customers want to know when their parcel ships.",
   summary={"summary": "A push notification when an order ships or is delivered.",
            "origin": JIRA("APP-77"), "labels": ["push"]})
cr(f"{M}/2-backlog/P1/crash-on-launch-android-9", "Crash on launch on Android 9",
   intent="A crash report from about 2% of the Android 9 devices, on a null theme.",
   answers="- Q: backport to the previous release? A: no.",
   summary={"summary": "Fix the launch crash on Android 9.", "origin": GH(21, MA), "labels": ["bug"]})
cr(f"{M}/2-backlog/P2/deep-links", "Open product links in the app",
   request="A product link from an email opens the browser.",
   summary={"summary": "Universal links to products and orders.", "origin": VERBAL, "labels": ["links"]})
cr(f"{M}/2-backlog/P3/app-icon-refresh", "Refresh the app icon",
   request="Marketing wants the new logo.",
   summary={"summary": "New icon set for iOS and Android.", "origin": VERBAL, "labels": ["design"]})
cr(f"{M}/3-ready/barcode-scan", "Scan a barcode to find a product",
   intent="Customers in the shop want to look up a product from its barcode.",
   answers="- Q: which formats? A: EAN-13 and QR.",
   summary={"summary": "Scan EAN-13 and QR codes to open a product page.",
            "origin": JIRA("APP-64"), "labels": ["search"]})
archive("mobile-app", "260604-1410", 31, "tablet-layout", "A two-column layout on tablets", "batch-01", f"{MA}/pull/6", 9.80)
archive("mobile-app", "260604-1422", 32, "dark-mode", "Dark mode follows the system setting", "batch-01", f"{MA}/pull/7", 6.15)
archive("mobile-app", "260612-1015", 33, "faster-startup", "Start the app in under two seconds", "batch-02", f"{MA}/pull/8", 11.70)
archive("mobile-app", "260612-1030", 34, "accessible-buttons", "Buttons have accessible labels", "batch-02", f"{MA}/pull/9", 4.55)

# ---------------------------------------------------------------- docs-portal

D = "projects/docs-portal/changes"
DP = "https://github.com/example/docs-portal"
cr(f"{D}/1-inbox/broken-search-anchor", "Search results link to the wrong anchor",
   request="A search for 'webhooks' lands in the middle of the page.",
   summary={"summary": "Make search results link to the heading that matched.",
            "origin": VERBAL, "labels": ["bug"]})
cr(f"{D}/2-backlog/P2/versioned-docs", "Versioned documentation",
   intent="Customers on v2 read the v3 pages.",
   summary={"summary": "A version switcher on every page.", "origin": GH(12, DP), "labels": ["docs"]})
archive("docs-portal", "260609-0915", 21, "dark-code-blocks", "Code blocks in dark mode", "batch-01", f"{DP}/pull/4", 3.90)

print("demo written to", OUT)
