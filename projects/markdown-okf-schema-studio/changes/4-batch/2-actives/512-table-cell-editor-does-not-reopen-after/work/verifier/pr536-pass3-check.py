"""Compare the posted PR 536 body with its earlier version and its source file."""

import difflib
import json
import os
import re
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
source = os.path.normpath(os.path.join(here, "..", "pr-body.md"))


def gh(*args):
    out = subprocess.run(["gh", *args], capture_output=True, check=True)
    return out.stdout.decode("utf-8")


def norm(text):
    return text.replace("\r\n", "\n").rstrip("\n").split("\n")


query = (
    'query { repository(owner:"gsemet", name:"markdown-okf-schema-studio") '
    "{ pullRequest(number:536) { body userContentEdits(first:20) "
    "{ nodes { editedAt diff } } } } }"
)
pr = json.loads(gh("api", "graphql", "-f", "query=" + query))["data"]["repository"]["pullRequest"]
posted = pr["body"]
edits = {n["editedAt"]: n["diff"] for n in pr["userContentEdits"]["nodes"]}
judged = edits["2026-11-26T10:40:22Z"]

with open(source, "rb") as handle:
    raw = handle.read()
print("source file starts with a BOM:", raw.startswith(b"\xef\xbb\xbf"))
print("posted == newest edit (10:44:47Z):", norm(posted) == norm(edits["2026-11-26T10:44:47Z"]))
print("posted == work/pr-body.md:", norm(posted) == norm(raw.decode("utf-8")))

print("--- diff: body of 10:40:22Z (judged by pass 2) -> posted body")
for line in difflib.unified_diff(norm(judged), norm(posted), "10:40:22Z", "posted", lineterm="", n=3):
    print(line)

print("--- image markers in the posted body")
for pattern in (r"!\[", r"<img", r"user-attachments", r"raw\.githubusercontent", r"\.(png|jpe?g|gif|webp|mp4)\b"):
    print(repr(pattern), len(re.findall(pattern, posted, re.I)))

print("--- words that could point at a removed image")
words = r"image|screenshot|screen shot|picture|capture|photo|frame|shown|below|above|following"
for number, line in enumerate(norm(posted), 1):
    if re.search(words, line, re.I):
        print(number, line)

print("--- local names, internal words, marks")
user = os.environ.get("USERNAME", "")
home = os.path.basename(os.path.expanduser("~"))
terms = [re.escape(user), re.escape(home), r"Users[\\/]", r"/home/", r"UNVERIFIED", r"STALE", r"CR-\d+",
         r"batch", r"planning", r"work/", r"Driver|Coder|Inspector|Verifier|Foreman|Chief of Staff"]
for number, line in enumerate(norm(posted), 1):
    if any(re.search(t, line, re.I) for t in terms if t):
        print(number, line)

html = json.loads(
    gh("api", "repos/gsemet/markdown-okf-schema-studio/pulls/536",
       "-H", "Accept: application/vnd.github.full+json")
)["body_html"]
print("--- body_html")
print("h2:", [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S)])
print("tables:", len(re.findall(r"<table", html)), "rows:", len(re.findall(r"<tr", html)))
print("img:", len(re.findall(r"<img", html)))
print("checked task boxes:", len(re.findall(r'<input[^>]*type="checkbox"[^>]*checked', html)),
      "of", len(re.findall(r'<input[^>]*type="checkbox"', html)))
print("mermaid markers:", len(re.findall(r'data-type="mermaid"|lang="mermaid"|highlight-source-mermaid', html)))
print("flowchart source present:", "flowchart LR" in html)
start = html.find("</table>")
end = html.find(">Changes<")
print("--- html between the table and the Changes heading (tags only, first 1500 characters)")
print(html[start:end][:1500])
sys.stdout.flush()
