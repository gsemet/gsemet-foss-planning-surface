// Third set: variants of EBNF and neighbours that may answer "Syntax error!" (kinds.cjs set "errors3").
"use strict";
module.exports = (uml, kind) => ({
  e_unterminated_string: kind("ebnf", "a = \"x ;"),
  e_unterminated_comment: kind("ebnf", "(* open", "a = \"x\" ;"),
  e_missing_rhs: kind("ebnf", "a = ;"),
  e_trailing_bar: kind("ebnf", "a = \"x\" | ;"),
  e_two_words: kind("ebnf", "a = b c ;"),
  e_no_semicolon: kind("ebnf", "a = \"x\""),
  e_paren: kind("ebnf", "a = ((( ;"),
  e_bracket: kind("ebnf", "a = [ \"x\" ;"),
  e_issue_doc: kind("ebnf", "title Number", "number = digit, { digit } ;", "digit = \"0\" | \"1\" | ;;"),
  e_uml_wrapped: uml("ebnf", "a = ((( ;"),
  r_unclosed_paren: kind("regex", "a(b"),
  r_bad_quant: kind("regex", "a{2,1}"),
  r_backslash: kind("regex", "\\"),
});
