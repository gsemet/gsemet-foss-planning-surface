// Coder probe, round 4: a CommonJS copy of the error-picture test of src/page/modules/plantumlDiagram.ts,
// for ebnf_probe.cjs --match. Keep in step with the source.
"use strict";
const ENGINE_ERROR_PICTURE = new RegExp(
  "^<svg\\b[^>]*><defs/><g>(?:"
  + "(?:<text\\b[^>]*>[^<]*</text>)*<rect\\b[^>]*\\bfill=\"#33FF02\"[^>]*/>"
  + "<text\\b[^>]*>\\[From [^<]*\\(line \\d+\\)[^<]*\\]</text>"
  + "|<text\\b[^>]*>(?:Your data does not sound like (?:JSON|YAML) data"
  + "|Diagram not supported by this release of PlantUML)</text>"
  + ")",
  "u",
);
const EBNF_SOURCE = /^\s*@startebnf\b/iu;
const EBNF_LABEL_GROUP = /<g class="[^"]*"[^>]*>(?:(?!<\/?g\b)[^])*<\/g>/gu;
const EBNF_NOTE = /<path\b[^>]*\/><path d="M([\d.]+),([\d.]+) L\1,[\d.]+ L[\d.]+,[\d.]+ L\1,\2"[^>]*\/>(?:<text\b[^>]*>[^<]*<\/text>)+/gu;
const EBNF_ERROR_LINE = /^<svg\b[^>]*><defs\/><g>(?:<[^>]*>[^<]*)*?(?:<g>|<\/text>|<path\b[^>]*\/>)<text\b(?![^>]*\bfont-weight=)[^>]*>Syntax error!<\/text>(?=<\?plantuml-src|<text\b|<\/g>)/u;

module.exports = (svg, source) => {
  if (ENGINE_ERROR_PICTURE.test(svg)) return true;
  if (!EBNF_SOURCE.test(source)) return false;
  return EBNF_ERROR_LINE.test(svg.replace(EBNF_LABEL_GROUP, "").replace(EBNF_NOTE, ""));
};
