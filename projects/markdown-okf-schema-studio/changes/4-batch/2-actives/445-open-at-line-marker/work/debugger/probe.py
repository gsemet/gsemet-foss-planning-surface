import sys
from playwright.sync_api import sync_playwright
page_path = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":900,"height":700})
    pg.on("console", lambda m: print("console:", m.type, m.text))
    pg.on("pageerror", lambda e: print("pageerror:", e))
    pg.goto("file:///" + page_path.replace("\\","/"))
    pg.wait_for_timeout(1500)
    print("marker", pg.evaluate("document.querySelectorAll('.sphinx-preview-line-marker').length"))
    print("msgs", pg.evaluate("JSON.stringify(window.visualMessages.map(m=>m.type))"))
    print(pg.evaluate("""(()=>{const r=document.documentElement;return JSON.stringify({id:r.getAttribute('data-sphinx-preview-document-id'),v:r.getAttribute('data-sphinx-preview-document-version'),rq:r.getAttribute('data-sphinx-preview-request-id')})})()"""))
    # re-dispatch manually
    print(pg.evaluate("""(()=>{const r=document.documentElement;
      window.dispatchEvent(new MessageEvent('message',{data:{type:'previewRevealLine',line:22,documentId:r.getAttribute('data-sphinx-preview-document-id'),revision:Number(r.getAttribute('data-sphinx-preview-document-version')),requestId:Number(r.getAttribute('data-sphinx-preview-request-id'))}}));
      return document.querySelectorAll('.sphinx-preview-line-marker').length})()"""))
    print("mappings", pg.evaluate("document.querySelectorAll('[data-sphinx-source-line]').length"))
    b.close()
