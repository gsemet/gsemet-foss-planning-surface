// STAB-04 probe: a PlantUML child that exits without reading stdin must not raise an uncaught error.
// POSIX only (uses /bin/sh). Run from src/markdown-okf-schema-studio after `npm run compile`.
const childProcess = require("node:child_process");
const path = require("node:path");
const out = path.resolve(process.env.OUT ?? "out/src");
const plantUml = require(`${out}/render/plantUmlRenderer.js`);
let uncaught = 0;
process.on("uncaughtException", () => { uncaught += 1; });
plantUml.setPlantUmlProcessSpawnerForTests({
  spawn: (_command, _args, options) => childProcess.spawn("/bin/sh", ["-c", "exit 0"],
    { ...options, stdio: ["pipe", "pipe", "pipe"] }),
});
const diagram = "@startuml\nA -> B : " + "x".repeat(900 * 1024) + "\n@enduml";
plantUml.renderPlantUmlDiagrams(`<div class="myst-plantuml-diagram">${diagram}</div>`,
  { workspaceRoot: process.cwd(), trusted: true })
  .then((result) => setTimeout(() => console.log(JSON.stringify({
    probe: "plantuml-epipe", uncaughtExceptions: uncaught,
    diagnostics: result.diagnostics.map((item) => item.message.slice(0, 80)),
  })), 200));
