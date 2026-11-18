"""What a fresh steering session does and holds in its first calls (figures and names only).

Command: python 04-fresh-starts.py > 04-fresh-starts.csv

For the first calls of each fresh Foreman or Chief of Staff session it writes: the call's context,
cost, its wake cause (a fixed label), the tools it used (tool names), the `chantier` subcommand words
of its shell commands (the word after `chantier ... ` such as seat, rules, status, foreman, asks,
watch), and the file names it read (base names only, under the references folder or the planning
surface's well-known names). No message text, no path.
"""
import csv, importlib.util, json, os, re, sys

spec = importlib.util.spec_from_file_location("calls03", os.path.join(os.path.dirname(os.path.abspath(__file__)), "03-steering-calls.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
SUBS = ("seat", "rules", "status", "foreman", "asks", "watch", "brief", "take", "order", "handback", "cost", "close", "heartbeat", "preflight", "next")
SESSIONS = [  # (label, kind, folder, session, until)
    ("foreman-b17", "foreman", m.CH, "bd1945f6-9982-485f-b29f-477277e80753"),
    ("foreman-b18", "foreman", m.CH, "446cff2e-8291-4f73-9ff0-f19c29743e6e"),
    ("foreman-b23-24", "foreman", m.CH, "1b6c0af3-8055-48dc-975e-95b0619755c4"),
    ("foreman-b25", "foreman", m.CH, "cc65c0a9-973c-4a5c-bde4-616fc2581097"),
    ("foreman-b26", "foreman", m.CH, "993a179a-630e-4ad6-913f-c10286a32ded"),
    ("foreman-b27", "foreman", m.CH, "62abbcd1-9358-4768-abec-8aa99767d8eb"),
    ("chief-surface", "chief", m.PS, "6eae8e55-4c71-4c8e-b28c-7788a8975d81"),
    ("chief-seat-take-a", "chief", m.CH, "11e74fa4-5c3f-435f-9e22-6c6ad6ba3f17"),
    ("chief-seat-take-b", "chief", m.CH, "cd5055f5-2871-4472-99b6-23742d3a5770"),
    ("chief-fresh-c", "chief", m.CH, "bf484d59-5971-41cd-b77e-e4275c2d0901"),
    ("chief-fresh-d", "chief", m.CH, "fd80eb73-cdfd-4808-8a50-2200c1bd191e"),
]
N = 80
w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(["label", "kind", "seq", "time", "wake_cause", "context", "usd", "cum_usd", "tools", "chantier_subcommands", "files_read"])
for label, kind, folder, sid in SESSIONS:
    path = f"{m.B}/{folder}/{sid}.jsonl"
    seen, cause, n, cum, own = set(), None, 0, 0.0, {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            k = d.get("type")
            if k == "user" and m.is_wake(d):
                cause = cause or m.classify(d, own)
            if k != "assistant":
                continue
            msg = d.get("message") or {}
            u = msg.get("usage")
            if not u or msg.get("model") == "<synthetic>" or msg.get("id") in seen:
                # tool_use blocks arrive one per record: gather them for the call
                if msg.get("id") in seen and n and (n <= N):
                    pass
                continue
            cc = u.get("cache_creation") or {}
            t = (u.get("input_tokens", 0), cc.get("ephemeral_5m_input_tokens", 0), cc.get("ephemeral_1h_input_tokens", 0), u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0))
            if not any(t):
                continue
            seen.add(msg["id"])
            n += 1
            rate = m.PRICE.get(re.sub(r"-\d{8}$", "", msg.get("model", "")))
            usd = sum(x * y / 1e6 for x, y in zip(t, rate)) if rate else 0.0
            cum += usd
            tools, subs, files = [], [], []
            for b in msg.get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    tools.append(b.get("name"))
                    i = b.get("input") or {}
                    if b.get("name") == "Bash":
                        c = str(i.get("command", ""))
                        for s in SUBS:
                            if re.search(r"\bchantier\b[^|;&\n]*?\s" + s + r"\b", c) or re.search(r"\$CHANTIER\s+(?:--\S+\s+)*" + s + r"\b", c):
                                subs.append(s)
                    if b.get("name") == "Read":
                        files.append(os.path.basename(str(i.get("file_path", "")).replace("\\", "/")))
            if n <= N:
                w.writerow([label, kind, n, d["timestamp"], cause or "", sum(t[:4]), round(usd, 4), round(cum, 4), "+".join(tools), "+".join(subs), "+".join(files)])
            cause = None
            if n > N:
                break
