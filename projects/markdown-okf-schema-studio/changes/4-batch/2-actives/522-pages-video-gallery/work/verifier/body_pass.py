"""Judge the posted PR body's pictures: map, download (no credentials), compare with the evidence."""
import hashlib, json, pathlib, re, sys, urllib.request
meta, files, evidence = (pathlib.Path(p) for p in sys.argv[1:4])
pr = json.loads(meta.read_text(encoding="utf-8"))
body, html = pr["body"], pr["body_html"]
print("head", pr["head"]["sha"], "updated", pr["updated_at"])
by_hash = {hashlib.sha256(p.read_bytes()).hexdigest(): p.name for p in evidence.glob("*.png")}
images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", body)
print("markdown images", len(images), "distinct urls", len({u for _, u in images}))
used = []
for i, (alt, url) in enumerate(images, 1):
    assert url.startswith("https://github.com/user-attachments/assets/"), url
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "generic-client"}), timeout=60) as r:
        data, status, ctype = r.read(), r.status, r.headers.get("Content-Type")
    (files / f"{i:02}.png").write_bytes(data)
    name = by_hash.get(hashlib.sha256(data).hexdigest(), "NO MATCH")
    used.append(name)
    print(f"{i:02} {status} {ctype} {len(data)} B | {alt} -> {name} | {url.rsplit('/',1)[1]}")
print("evidence pictures", len(by_hash), "attached and matched", len(set(used) - {'NO MATCH'}), "unused", sorted(set(by_hash.values()) - set(used)))
print("html: img", html.count("<img"), "h2", re.findall(r"<h2[^>]*>(.*?)</h2>", html), "table", html.count("<table"), "mermaid", html.count("mermaid") > 0,
      "checkboxes", html.count('type="checkbox"'), "checked", len(re.findall(r'type="checkbox"[^>]*checked|checked[^>]*type="checkbox"', html)), "br", html.count("<br"),
      "literal ![", html.count("!["), "relative evidence paths", body.count("verifier/evidence"))
for src in re.findall(r'<img[^>]*src="([^"]+)"', html):
    with urllib.request.urlopen(urllib.request.Request(src, headers={"User-Agent": "generic-client"}), timeout=60) as r:
        print("rendered img", r.status, r.headers.get("Content-Type"), hashlib.sha256(r.read()).hexdigest()[:12], src.split("?")[0][-60:])
