// Verifier probe of the built-in PlantUML engine's answers (CR-521, claim 3).
//   node --import ./scripts/register-myst-patches.mjs <this file> <worktree> <output folder> <errors|drawn|salt>
// It reuses realflow.cjs (real render pipeline, real page, real bundles, real export controller, export opened
// with JavaScript off). For each source, light and dark: render state, disclosure shown/open, the picture's text,
// in the preview and the export, and a contact sheet of the pictures for a look by eye.
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const [worktree, outDir, set = "errors"] = process.argv.slice(2);
const uml = (...l) => ["@startuml", ...l, "@enduml"];
const kind = (k, ...l) => ["@start" + k, ...l, "@end" + k];
const J = "Your data does not sound like JSON data";
const Y = "Your data does not sound like YAML data";
const U = "Diagram not supported by this release of PlantUML";
const SETS = {
  errors: {
    seqline: uml("Alice -> Bob: hello", "this is not plantuml ((( ###"),
    seqarrow: uml("Alice ->>>>x<< : ", "}}}"),
    classbody: uml("class A {", "  +x : int", "activate ??? !!"),
    firstline: uml("(((( ###"),
    late: uml(...Array.from({ length: 60 }, (_, i) => `Alice -> Bob: m${i}`), "this is not plantuml ((( ###"),
    activity: uml("start", ":one;", "if (x) then", "endwhile ???", "stop"),
    state: uml("[*] --> A", "state B {", "  A -> ", "}}}}"),
    component: uml("component A", "[A] --> [B", "!!!???"),
    usecase: uml("actor X", "X --> (U", "usecase ???)))"),
    skinbad: uml("skinparam {{{", "Alice -> Bob"),
    preprocif: uml("!if (%true())", "Alice -> Bob"),
    preprocfn: uml("Alice -> Bob : %nofunction(", "!$x = (", "Bob -> Alice"),
    preprocvar: uml("!$a = $b + ", "Alice -> Bob"),
    preprocunknown: uml("!foobar", "Alice -> Bob"),
    preprocassert: uml("!assert %false() : \"boom\"", "Alice -> Bob"),
    endfunction: uml("!endfunction", "Alice -> Bob"),
    notheme: uml("!theme does-not-exist", "Alice -> Bob"),
    pragma: uml("!pragma layout nothing", "class A", "A --> "),
    noenduml: ["@startuml", "Alice -> Bob"],
    nostart: ["this is not plantuml ((( ###"],
    empty: uml(),
    mindmapbad: kind("mindmap", "this is not a mindmap"),
    wbsbad: kind("wbs", "not wbs ((("),
    ganttbad: kind("gantt", "[A] lasts 2 days", "this is ((( not gantt"),
    jsonbad: kind("json", "[1, 2,, ]"),
    yamlbad: kind("yaml", "\t- : : :", "  x"),
    mathbad: kind("math", "(((("),
    latexbad: kind("latex", "\\frac{"),
    ditaabad: kind("ditaa", "+---+", "| A |", "+---+"),
    dotbad: kind("dot", "digraph G { a -> "),
    saltbad: kind("salt", "{", "[OK"),
    regexbad: kind("regex", "((("),
    ebnfbad: kind("ebnf", "a = ((( ;"),
    nwdiagbad: uml("nwdiag {", "  network {{{ ", "}"),
    unknownstart: kind("nothing", "x"),
    chartbad: kind("chart", "((( nonsense"),
    timingbad: uml("robust \"A\" as A", "@0", "A is ", "((( ###"),
    objectbad: uml("object A", "A : = ", "((( ###"),
    erbad: uml("entity A {", "}", "A ||--o{ ", "((( ###"),
    sprite: uml("sprite $x [bad] {", "zz", "Alice -> Bob"),
    duplicate: uml("class A", "package A {", "}", "interface A"),
    returnbad: uml("return x", "deactivate Nobody"),
  },
  drawn: {
    sequence: uml("title Order", "autonumber", "Alice -> Bob: hello", "Bob --> Alice: Syntax Error?"),
    classd: uml("class A {", "  +x : int", "}", "A <|-- B"),
    activitynew: uml("start", ":one;", "if (ok?) then (yes)", "  :two;", "else (no)", "  :three;", "endif", "stop"),
    activityold: uml("(*) --> \"First\"", "--> (*)"),
    stated: uml("[*] --> Idle", "Idle --> Busy : go", "Busy --> [*]"),
    usecased: uml("actor User", "User --> (Login)"),
    componentd: uml("[Web] --> [Api]", "database Db", "[Api] --> Db"),
    deployment: uml("node n1 {", "  artifact a1", "}", "cloud c1", "n1 --> c1"),
    objectd: uml("object o1 {", "  x = 1", "}", "object o2", "o1 --> o2"),
    timing: uml("robust \"User\" as U", "@0", "U is Idle", "@10", "U is Busy"),
    er: uml("entity A {", "  *id", "}", "entity B", "A ||--o{ B"),
    archimate: uml("archimate #Technology \"VPN\" as vpn <<technology-device>>"),
    note: uml("note as N", U, J, "end note"),
    legend: uml("legend", "[From textarea (line 3) ]", "end legend", "Alice -> Bob"),
    header: uml("header " + J, "footer " + U, "Alice -> Bob"),
    caption: uml("caption " + U, "Alice -> Bob"),
    classnamed: uml("class \"" + J + "\""),
    participant: uml("participant \"" + U + "\" as P", "P -> P"),
    actfirst: uml("start", ":" + J + ";", "stop"),
    theme: uml("!theme plain", "Alice -> Bob"),
    themecy: uml("!theme cyborg", "class A"),
    handwritten: uml("skinparam handwritten true", "Alice -> Bob"),
    bg: uml("skinparam backgroundColor #33FF02", "Alice -> Bob"),
    mindmap: kind("mindmap", "* " + U, "** child"),
    wbs: kind("wbs", "* " + J, "** child"),
    gantt: kind("gantt", "[" + U + "] lasts 3 days"),
    json: kind("json", "{ \"" + J + "\": 1 }"),
    jsonarr: kind("json", "[ \"" + U + "\" ]"),
    yaml: kind("yaml", Y + ": 1"),
    salt: kind("salt", "{", "  Login | \"user\"", "  [OK] | [Cancel]", "}"),
    saltuml: uml("salt", "{", "  [OK]", "}"),
    nwdiag: uml("nwdiag {", "  network dmz {", "    web01;", "  }", "}"),
    ditaa: kind("ditaa", "+---+", "| A |", "+---+"),
    regex: kind("regex", "a(b|c)*"),
    ebnf: kind("ebnf", "a = \"x\", { \"y\" } ;"),
    board: kind("board", "A", "+B"),
    files: kind("files", "/a/b.txt"),
    chronology: kind("chronology", "[A] happens on 2024-01-01"),
    wire: kind("wire", "* a", "* b"),
    packet: uml("packetdiag {", "  0-15: Source", "}"),
    noteright: uml("title t", "Alice -> Bob : hi", "note right: " + U),
    newpage: uml("Alice -> Bob", "newpage", "Bob -> Alice"),
    bignote: uml("skinparam backgroundColor transparent", "class A", "note right of A : " + J),
  },
  // The known gap of the body: salt text as the first thing drawn, and neighbours of it.
  salt: {
    saltjson: kind("salt", "{", "  " + J, "}"),
    saltyaml: kind("salt", "{", "  " + Y, "}"),
    saltunsup: kind("salt", "{", "  " + U, "}"),
    saltumljson: uml("salt", "{", "  " + J, "}"),
    saltumlunsup: uml("salt", "{", "  " + U, "}"),
    saltrow: kind("salt", "{", "  " + J + " | [OK]", "}"),
    saltbutton: kind("salt", "{", "  [" + J + "]", "}"),
    saltgrid: kind("salt", "{+", "  " + J, "}"),
    salttitle: kind("salt", "title " + J, "{", "  [OK]", "}"),
    saltbanner: kind("salt", "{", "  <back:#33FF02>[From textarea (line 3) ]", "}"),
    saltsecond: kind("salt", "{", "  Title", "  " + J, "}"),
    saltlonger: kind("salt", "{", "  " + J + " today", "}"),
    ditaajson: kind("ditaa", J),
    mindmapjson: kind("mindmap", "*_ " + J),
    wbsunsup: kind("wbs", "*_ " + U),
    uml_title_only: uml("title " + J),
    uml_note_only: uml("note \"" + J + "\" as N"),
    uml_legend_only: uml("legend", J, "end legend"),
    json_title: kind("json", "title " + J, "[1]"),
    nwdiag_name: uml("nwdiag {", "  network \"" + J + "\" {", "  }", "}"),
    board_text: kind("board", J),
    files_text: kind("files", "/" + J),
    gantt_title: kind("gantt", "title " + J, "[A] lasts 1 day"),
    wire_text: kind("wire", "* " + J),
    math_text: kind("math", J),
    regex_text: kind("regex", J),
    activity_floating: uml("start", "floating note left: " + J, "stop"),
    timing_text: uml("concise \"" + J + "\" as C", "@0", "C is x"),
  },
};
SETS.errors2 = require("./more-errors.cjs")(uml, kind);
SETS.errors3 = require("./more-ebnf.cjs")(uml, kind);
const names = Object.keys(SETS[set]);
const FIGURES_SRC = names.map((n) => ({ word: n, kind: "plantuml", md: ["## " + n, "", "```plantuml", ...SETS[set][n], "```", ""] }));
const source = fs.readFileSync(path.join(__dirname, "realflow.cjs"), "utf8");
// realflow's helpers (everything before its main block) with this set of figures.
const helpers = source.slice(0, source.indexOf("(async () => {"))
  .replace('const [worktree, outDir, mode = "assert"] = process.argv.slice(2);', "")
  .replace(/const figures = mode === [^\n]*\n/u, "const figures = FIGURES_SRC;\n");

const main = async (h) => {
  const { chromium, buildPage, openPage, exportFile, pathToFileURL, root } = h;
  const browser = await chromium.launch({ args: ["--allow-file-access-from-files"] });
  const noJs = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 900, height: 1000 } });
  const report = {};
  const read = (page) => page.evaluate(() => [...document.querySelectorAll(".myst-plantuml-diagram")].map((d) => {
    const s = d.parentElement.querySelector(":scope > details.myst-plantuml-source");
    const src = d.querySelector("img")?.getAttribute("src");
    const svg = src ? decodeURIComponent(src.slice(src.indexOf(",") + 1)) : "";
    const says = svg ? [...new DOMParser().parseFromString(svg, "image/svg+xml").querySelectorAll("text")].map((e) => e.textContent).join(" ") : "";
    return {
      state: d.getAttribute("data-render-state"), dark: d.getAttribute("data-plantuml-dark"), picture: Boolean(src),
      display: s ? getComputedStyle(s).display : "NO-DETAILS", open: s ? s.open : null, says,
      message: d.querySelector("p")?.textContent ?? "", src: src ?? "", head: svg.slice(0, 700),
    };
  }));
  const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;");
  try {
    for (const themeId of ["light", "dark"]) {
      const pagePath = await buildPage(set + "-" + themeId, "builtin", true);
      const { page, problems } = await openPage(browser, pagePath, themeId);
      await page.waitForFunction((n) => document.querySelectorAll(".myst-plantuml-diagram[data-render-state]").length === n,
        names.length, { timeout: 90000 }).catch((e) => console.log("WAIT: " + e.message.split("\n")[0]));
      await page.waitForTimeout(5000);
      const preview = await read(page);
      console.log(themeId, "figures in page:", preview.length, "of", names.length);
      const exported = await exportFile(page, set + "-" + themeId);
      const reader = await noJs.newPage();
      await reader.goto(pathToFileURL(exported.target).href);
      const out = await read(reader);
      await reader.close();
      report[themeId] = names.map((n, i) => ({ name: n, ...preview[i], export: out[i] && { state: out[i].state, display: out[i].display, open: out[i].open, samePicture: out[i].src === preview[i].src } }));
      report[themeId + "Errors"] = problems;
      const sheet = await browser.newPage({ viewport: { width: 1480, height: 900 } });
      await sheet.setContent('<body style="margin:8px;background:' + (themeId === "dark" ? "#555" : "#bbb")
        + ';font:12px sans-serif;display:flex;flex-wrap:wrap;gap:8px;align-items:flex-start">' + report[themeId].map((r) =>
          '<div style="border:3px solid ' + (r.state === "rendered" ? "green" : "red") + ';padding:4px;width:350px;background:'
          + (themeId === "dark" ? "#1e1e1e" : "#fff") + ';color:' + (themeId === "dark" ? "#ddd" : "#000") + '"><b>' + esc(r.name) + " / " + r.state + " / " + r.display + "</b><br>"
          + (r.src ? '<img style="width:340px;height:150px;object-fit:contain;object-position:left top" src="' + r.src + '">' : esc(r.message.slice(0, 220))) + "</div>").join("") + "</body>");
      await sheet.waitForTimeout(1500);
      await sheet.screenshot({ path: path.join(root, set + "-sheet-" + themeId + ".png"), fullPage: true });
      await sheet.close();
      await page.close();
    }
  } finally {
    await browser.close();
    for (const t of ["light", "dark"]) for (const r of report[t] ?? []) delete r.src;
    fs.writeFileSync(path.join(root, "report-" + set + ".json"), JSON.stringify(report, null, 1));
  }
  for (const t of ["light", "dark"]) {
    console.log("== " + set + " " + t + " pageErrors=" + JSON.stringify(report[t + "Errors"]));
    for (const r of report[t]) {
      console.log([r.name, r.state, "dark=" + r.dark, "pic=" + r.picture, r.display, "open=" + r.open,
        "| export", r.export?.state, r.export?.display, "open=" + r.export?.open, "same=" + r.export?.samePicture, "|",
        (r.says || r.message).replace(/\s+/g, " ").slice(0, 120)].join(" "));
    }
  }
};

const factory = new Function("require", "process", "__dirname", "console", "FIGURES_SRC", "worktree", "outDir", "mode",
  helpers + "\nreturn { chromium, buildPage, openPage, exportFile, pathToFileURL, root };");
main(factory(require, process, __dirname, console, FIGURES_SRC, worktree, outDir, "kinds"))
  .catch((error) => { console.error(error); process.exit(1); });
