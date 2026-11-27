// Coder probe, round 4: the built-in PlantUML engine's EBNF "Syntax error!" pictures, and drawn
// diagrams that write the same words. node <this file> <worktree> <output folder> [--match <module>]
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");
const { pathToFileURL } = require("node:url");

const [worktree, outDir] = process.argv.slice(2);
const requireWt = createRequire(path.join(worktree, "package.json"));
const { build } = requireWt("esbuild");
const { chromium } = requireWt("playwright-core");

const ebnf = (...lines) => ["@startebnf", ...lines, "@endebnf"];
const uml = (...lines) => ["@startuml", ...lines, "@enduml"];
// Expected: "error" for a source the engine cannot read, "rendered" for one it draws.
const CASES = {
  // errors
  eBracket: ["error", ebnf('a = [ "x" ;')],
  eParens: ["error", ebnf("a = ((( ;")],
  eBarEnd: ["error", ebnf('a = "x" | ;')],
  eNoComma: ["error", ebnf("a = b c ;")],
  eTitled: ["error", ebnf("title Grammar", 'a = "x" ;', 'b = "y" ;;')],
  eGoodThenBad: ["error", ebnf('good = "x", { "y" } ;', 'bad = [ "x" ;')],
  eDigit: ["error", ebnf("bar = digit, { digit } ;", 'digit = "0" | "1" | ;;')],
  eThreeGoodThenBad: ["error", ebnf('a = "x" ;', 'b = "y", a ;', "c = { a | b } ;", "d = ( a ;")],
  eUnclosedBrace: ["error", ebnf('a = { "x" ;')],
  eDoubleSemi: ["error", ebnf('a = "x" ;;')],
  eBadThenGood: ["error", ebnf('a = [ "x" ;', 'b = "y" ;')],
  eStyled: ["error", ebnf("<style>", "element { FontColor red }", "</style>", 'a = [ "x" ;')],
  eTitleThenBad: ["error", ebnf("title Grammar", 'a = [ "x" ;')],
  eTitleGoodBad: ["error", ebnf("title Grammar", 'a = "x" ;', 'b = [ "y" ;')],
  eCommentThenBad: ["error", ebnf("(* note *)", 'a = [ "x" ;')],
  eGoodBadGood: ["error", ebnf('a = "x" ;', 'b = [ "y" ;', 'c = "z" ;')],
  eTwoBad: ["error", ebnf('a = [ "x" ;', 'b = ( "y" ;')],
  eScale: ["error", ebnf("scale 2", 'a = [ "x" ;')],
  eTheme: ["error", ebnf("!theme plain", 'a = [ "x" ;')],
  eSkin: ["error", ebnf("skinparam backgroundColor #EEEEEE", 'a = [ "x" ;')],
  eCaption: ["error", ebnf("caption Fig 1", 'a = [ "x" ;')],
  eHeader: ["error", ebnf("header Top", 'a = [ "x" ;')],
  eFooter: ["error", ebnf("footer Bottom", 'a = [ "x" ;')],
  eLegend: ["error", ebnf("legend", "Grammar", "endlegend", 'a = [ "x" ;')],
  eStyleFont: ["error", ebnf("<style>", "element { FontName serif; FontSize 20 }", "</style>", 'a = [ "x" ;')],
  eCompact: ["error", ebnf("!pragma compact", 'a = [ "x" ;')],
  // drawn, with the words
  dTerminal: ["rendered", ebnf('a = "Syntax error!" ;')],
  dTerminalAfter: ["rendered", ebnf('a = "x", "Syntax error!" ;')],
  dRuleName: ["rendered", ebnf('Syntax_error = "x" ;')],
  dSpecial: ["rendered", ebnf("a = ? Syntax error! ? ;")],
  dComment: ["rendered", ebnf('(* Syntax error! *)', 'a = "x" ;')],
  dTitle: ["rendered", ebnf("title Syntax error!", 'a = "x" ;')],
  dDigitImitate: ["rendered", ebnf('bar = digit, { digit } ;', 'digit = "Syntax error!" ;')],
  dOnlyTerminal: ["rendered", ebnf('Syntax = "error!" ;')],
  dSequence: ["rendered", uml("Alice -> Bob: Syntax error!")],
  dNote: ["rendered", uml("Alice -> Bob: hi", "note over Bob: Syntax error!")],
  dClass: ["rendered", uml('class "Syntax error!"')],
  dSaltLabel: ["rendered", ["@startsalt", '{ "Syntax error!" }', "@endsalt"]],
  dSaltBare: ["rendered", ["@startsalt", "{", "Syntax error!", "}", "@endsalt"]],
  dMindmap: ["rendered", ["@startmindmap", "* Syntax error!", "@endmindmap"]],
  dMindmapBoxless: ["rendered", ["@startmindmap", "*_ Syntax error!", "@endmindmap"]],
  dWbsBoxless: ["rendered", ["@startwbs", "*_ Syntax error!", "@endwbs"]],
  dLegend: ["rendered", uml("Alice -> Bob", "legend", "Syntax error!", "endlegend")],
  dRawText: ["rendered", uml('rectangle "Syntax error!" as r #transparent;line:transparent')],
  dCreole: ["rendered", ["@startcreole", "Syntax error!", "@endcreole"]],
  dCreoleSans: ["rendered", ["@startcreole", "<font:sans-serif>Syntax error!</font>", "@endcreole"]],
  dCreoleSkin: ["rendered", ["@startcreole", "skinparam defaultFontName sans-serif", "Syntax error!", "@endcreole"]],
  dUmlSkinText: ["rendered", uml("skinparam defaultFontName sans-serif", 'label "Syntax error!"')],
  dEbnfCommentOnly: ["rendered", ebnf("(* Syntax error! *)")],
  dSaltSans: ["rendered", ["@startsalt", "skinparam defaultFontSize 14", "{", "Syntax error!", "}", "@endsalt"]],
  dMindmapBoxlessSkin: ["rendered", ["@startmindmap", "<style>", "mindmapDiagram { Padding 0; Margin 0 }", "</style>", "*_ Syntax error!", "@endmindmap"]],
  dMindmapBoxlessRules: ["rendered", ["@startmindmap", "*_ Syntax error!", "**_ b", "@endmindmap"]],
  dEbnfTerminalStyled: ["rendered", ebnf("<style>", "element { Margin 0 }", "</style>", 'a = "Syntax error!" ;')],
  dEbnfNameAndWords: ["rendered", ebnf('a = "x" ;', '(* Syntax error! *)', 'b = "y" ;')],
  dUmlTextAtZero: ["rendered", uml("skinparam defaultFontName sans-serif", "skinparam backgroundColor transparent", "skinparam padding 0", "skinparam shadowing false", 'rectangle "Syntax error!" #transparent;line:transparent')],
  dJson: ["rendered", ["@startjson", '"Syntax error!"', "@endjson"]],
  dRegex: ["rendered", ["@startregex", "Syntax error!", "@endregex"]],
};

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const bundle = path.join(outDir, "engine.js");
  await build({
    stdin: { contents: "import { renderToString } from '@plantuml/core'; import '@plantuml/core/themes.js'; import '@plantuml/core/openiconic.js'; window.render = renderToString;", resolveDir: worktree },
    outfile: bundle, bundle: true, platform: "browser", target: "es2020", format: "iife", logLevel: "silent",
  });
  const html = path.join(outDir, "engine.html");
  fs.writeFileSync(html, '<!doctype html><meta charset="utf-8"><body><script src="engine.js"></script></body>');
  const matchIdx = process.argv.indexOf("--match");
  const matcher = matchIdx > 0 ? require(path.resolve(process.argv[matchIdx + 1])) : null;
  const browser = await chromium.launch({ args: ["--allow-file-access-from-files"] });
  let wrong = 0;
  try {
    const page = await browser.newPage();
    await page.goto(pathToFileURL(html).href);
    for (const dark of [false, true]) {
      for (const [name, [expected, lines]] of Object.entries(CASES)) {
        const result = await page.evaluate(({ lines, dark }) => new Promise((resolve) => {
          const timer = setTimeout(() => resolve({ timeout: true }), 15000);
          try {
            window.render(lines, (svg) => { clearTimeout(timer); resolve({ svg }); }, (error) => { clearTimeout(timer); resolve({ error: String(error) }); }, { dark });
          } catch (error) { resolve({ thrown: String(error) }); }
        }), { lines, dark });
        const label = `${name}${dark ? "-dark" : ""}`;
        if (result.svg) {
          fs.writeFileSync(path.join(outDir, `${label}.svg`), result.svg);
          const texts = [...result.svg.matchAll(/<text[^>]*>([^<]*)<\/text>/gu)].map((m) => m[1]);
          let verdict = "";
          if (matcher) {
            const got = matcher(result.svg) ? "error" : "rendered";
            verdict = `${got === expected ? "OK " : "WRONG "}${got} (expected ${expected})`;
            if (got !== expected) wrong += 1;
          }
          console.log(label, "SVG", result.svg.length, verdict, "texts:", JSON.stringify(texts.slice(-5)));
          for (const m of result.svg.matchAll(/<text([^>]*)>([^<]*rror[^<]*)<\/text>(.{0,40})/gu)) {
            console.log("   ", m[1].replace(/ xml:space="preserve" style="white-space: pre"/u, ""), "|", m[2], "|", m[3]);
          }
        } else console.log(label, JSON.stringify(result).slice(0, 300));
      }
    }
  } finally { await browser.close(); }
  if (matcher) console.log("wrong:", wrong);
})().catch((error) => { console.error(error); process.exit(1); });
