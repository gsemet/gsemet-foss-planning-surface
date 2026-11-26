"""Open the pages written by cards-browser.js in Chromium and report which body words are on screen.

A word counts as on screen when its element is visible, has a box, and is the element hit at the
centre of its own text.

Usage: python cards-browser.py <pagesDir> <outDir>
"""

import pathlib
import sys

from playwright.sync_api import sync_playwright

pages, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 700, "height": 600})
    for file in sorted(pages.glob("*.html")):
        page.goto(file.as_uri())
        result = page.evaluate(
            """() => ['Alpha', 'Beta', 'Gamma'].map((word) => {
                const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
                let node;
                while ((node = walker.nextNode())) {
                    const at = node.textContent.indexOf(word);
                    if (at < 0 || node.parentElement.closest('style, script')) continue;
                    const range = document.createRange();
                    range.setStart(node, at);
                    range.setEnd(node, at + word.length);
                    const box = range.getBoundingClientRect();
                    const hit = document.elementFromPoint(box.x + box.width / 2, box.y + box.height / 2);
                    return `${word}: visible=${node.parentElement.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })} ` +
                        `size=${Math.round(box.width)}x${Math.round(box.height)} y=${Math.round(box.y)} hit=${hit === node.parentElement}`;
                }
                return `${word}: not in the page`;
            })"""
        )
        print(file.stem, "|", " | ".join(result))
        page.screenshot(path=str(out / f"{file.stem}.png"), clip={"x": 0, "y": 0, "width": 700, "height": 330})
    browser.close()
