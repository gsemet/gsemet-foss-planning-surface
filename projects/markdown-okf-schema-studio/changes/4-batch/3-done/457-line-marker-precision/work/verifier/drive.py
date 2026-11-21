"""Verifier driver for CR-457: opens the rendered fixture 94 at a requested line, as the host's previewRevealLine does,
and writes a screenshot plus the facts (marker box, expected element box) per case, theme and side.

usage: python -I drive.py <before|after> <worktree root with out/reports/visual/pages> <output folder>
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

side, root, outdir = sys.argv[1], pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
outdir.mkdir(parents=True, exist_ok=True)

# name, line, JS expression for the element the marker should sit on
CASES = [
    ("table-row", 15, "[...document.querySelectorAll('table tr')].find(r => r.textContent.includes('beta'))"),
    ("table-row-quote", 20, "[...document.querySelectorAll('blockquote table tr')].find(r => r.textContent.includes('second'))"),
    ("table-row-note", 26, "[...document.querySelectorAll('.admonition table tr, .myst-admonition table tr')].find(r => r.textContent.includes('south'))"),
    ("hidden-tab-paragraph", 36, "[...document.querySelectorAll('p')].find(r => r.textContent.includes('The third source line'))"),
    ("hidden-tab-code", 39, "[...document.querySelectorAll('.myst-code-line')].find(r => r.textContent.includes('second_tab_code'))"),
    ("hidden-tab-nested", 48, "[...document.querySelectorAll('p')].find(r => r.textContent.includes('Nested hidden tab line'))"),
    ("frontmatter-row", 4, "document.querySelector('tr[data-okf-field=\"owner\"]')"),
    ("frontmatter-list-value", 6, "document.querySelector('tr[data-okf-field=\"tags\"]')"),
    ("frontmatter-comment", 2, "document.querySelector('section[data-okf-properties]')"),
]
FACTS = """(expr) => {
  const marker = document.querySelector('.sphinx-preview-line-marker');
  const box = (e) => { if (!e) return null; const b = e.getBoundingClientRect(); return {top: Math.round(b.top*10)/10, height: Math.round(b.height*10)/10}; };
  const target = eval(expr);
  const panels = [...document.querySelectorAll('.myst-tab-panel')].map(p => ({text: p.textContent.trim().slice(0, 24), hidden: p.hidden}));
  return {markers: document.querySelectorAll('.sphinx-preview-line-marker').length, marker: box(marker), target: box(target),
    scrollY: Math.round(scrollY), panels};
}"""

results = {}
with sync_playwright() as p:
    browser = p.chromium.launch(args=["--allow-file-access-from-files"])
    for theme in ("light", "dark"):
        page_file = root / "out/reports/visual/pages" / f"94-line-marker-precision--{theme}--sticky-3--default.html"
        for name, line, expr in CASES:
            context = browser.new_context(viewport={"width": 900, "height": 1000}, device_scale_factor=2, reduced_motion="reduce")
            page = context.new_page()
            page.goto(page_file.as_uri())
            page.wait_for_timeout(800)
            page.evaluate(
                """(data) => { const root = document.documentElement;
                  window.dispatchEvent(new MessageEvent("message", { data: { ...data,
                    documentId: root.getAttribute("data-sphinx-preview-document-id"),
                    revision: Number(root.getAttribute("data-sphinx-preview-document-version")),
                    requestId: Number(root.getAttribute("data-sphinx-preview-request-id")) } })); }""",
                {"type": "previewRevealLine", "line": line},
            )
            page.wait_for_timeout(700)
            facts = page.evaluate(FACTS, expr)
            results[f"{theme}/{name}"] = {"line": line, **facts}
            page.screenshot(path=str(outdir / f"{side}-{name}-{theme}.png"))
            context.close()
    browser.close()
print(json.dumps(results, indent=1))
