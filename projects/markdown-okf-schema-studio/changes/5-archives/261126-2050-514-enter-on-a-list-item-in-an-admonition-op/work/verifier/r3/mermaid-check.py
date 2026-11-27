"""Render the posted description's mermaid diagram in Chromium with the repository's mermaid.

Usage: python mermaid-check.py <pr-body.md> <mermaid.min.js> <out.png>
"""

import re
import sys

from playwright.sync_api import sync_playwright

body, library, out = sys.argv[1:4]
text = open(body, encoding="utf-8").read().replace("\r\n", "\n")
diagrams = re.findall(r"```mermaid\n(.*?)\n```", text, re.S)
print(f"diagrams: {len(diagrams)}")
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1400, "height": 700})
    page.set_content("<body style='background:white'><div id='o'></div></body>")
    page.add_script_tag(path=library)
    for diagram in diagrams:
        result = page.evaluate(
            """async (source) => {
                mermaid.initialize({ startOnLoad: false });
                try {
                    const { svg } = await mermaid.render('d', source);
                    document.getElementById('o').innerHTML = svg;
                    const nodes = [...document.querySelectorAll('#o .node')].map((n) => n.textContent.trim());
                    return { version: mermaid.version, ok: true, nodes, edges: document.querySelectorAll('#o .flowchart-link').length };
                } catch (error) {
                    return { version: mermaid.version, ok: false, error: String(error) };
                }
            }""",
            diagram,
        )
        print(result)
        page.locator("#o svg").screenshot(path=out)
    browser.close()
