# Autodetect MyST feature

By default, keep MyST feature behind a feature gate per file.

Autodetect MyST by finding the closest conf.py, look if the MyST is enabled and detect extension.

Enabled/disable extension according to https://myst-parser.readthedocs.io/en/latest/syntax/optional.html

if a feature is used but the extension disable, display an error line with this message:
"Warning: `XXX` is used but this is behind the extension YYY, which does not seem enabled in your config.py. Please install extension "YYY" and register in `myst_enable_extensions`

---

When an url appears in the markdown, make it clickable
