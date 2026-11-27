"""Runs the real PlantUML "success" page check (visual scenarios v04 and v05) without PlantUML.

Argument: a worktree root where `renderFixtures.js` wrote the pages. On each page the failure message is
replaced by a loaded picture with the render state `rendered`, as a working JAR would, then PAGE_CHECKS runs.
"""

import json
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "test/visual"))
from capture_support import PAGE_CHECKS  # noqa: E402

VALUES = {
    "__MIN_CONTRAST__": "0", "__EXPECTED_ADMONITIONS__": "0", "__EXPECTED_FIGURES__": "0",
    "__EXPECTED_MERMAID__": "0", "__EXPECTED_PLANTUML__": "1", "__EXPECTED_CONTEXT_TAGS__": "0",
    "__CONTEXT_TAG_CHECKS__": "false", "__PLANTUML_EXPECTATION__": '"success"', "__MERMAID_EXPECTATION__": '"none"',
}
DRAWN = """async () => {
  const diagram = document.querySelector('.myst-plantuml-diagram');
  const image = new Image();
  image.className = 'myst-plantuml-image';
  image.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="20"><rect width="40" height="20"/></svg>');
  diagram.replaceChildren(image);
  diagram.setAttribute('data-render-state', 'rendered');
  await image.decode();
}"""

checks = PAGE_CHECKS
for placeholder, value in VALUES.items():
    checks = checks.replace(placeholder, value)
left = re.findall(r"__[A-Z_]+__", checks)
if left:
    sys.exit(f"placeholders without a value: {left}")

manifest = json.loads((ROOT / "out/reports/visual/manifest.json").read_text(encoding="utf-8"))
pages = pathlib.Path(manifest["pageDirectory"])
found = 0

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(args=["--allow-file-access-from-files"])
    for prefix in ("diagrams/v04-", "diagrams/v05-"):
        scenario = next(s for s in manifest["scenarios"] if s["id"].startswith(prefix))
        context = browser.new_context(viewport={"width": scenario["width"], "height": 900})
        page = context.new_page()
        page.goto((pages / scenario["page"]).as_uri())
        page.wait_for_selector(".myst-plantuml-diagram[data-render-state]", state="attached")
        page.evaluate(DRAWN)
        failures = [f for f in page.evaluate(checks) if "PlantUML" in f]
        found += len(failures)
        print(scenario["id"], "PlantUML failures:", failures)
        context.close()
    browser.close()
sys.exit(1 if found else 0)
