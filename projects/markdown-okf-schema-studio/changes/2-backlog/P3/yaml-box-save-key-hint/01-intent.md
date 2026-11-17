# A YAML value box shows no hint of the key that saves it

Severity Low · Gap · Area Front matter · P3

A YAML value box (a field with no schema, of unknown type, or holding an object) shows no key hint. The
one-line text box shows "Enter saves · Shift+Enter adds a line", but in the YAML box Enter adds a line and
only Cmd or Ctrl+Enter saves, so the author has to guess. Add a "Cmd/Ctrl+Enter saves" hint to the YAML box.
