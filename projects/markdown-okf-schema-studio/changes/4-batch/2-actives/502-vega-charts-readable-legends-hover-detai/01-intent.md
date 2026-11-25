# Vega charts: readable legends, hover detail, no Chart source

The owner finds the text of Vega-Lite and Vega charts too small in the preview, legends first. The
fix makes chart text readable by default in every theme (Cream, light and dark). The default
legend, axis and title sizes come from a rendering exploration: two or three candidates were drawn
by the real preview page and judged by a critic (02-answers.md).

The preview also shows a hover detail on chart marks by default, as far as Vega allows (Q4). It
drops the collapsed **Chart source** section under each chart, which is useless there because the
source is the document itself. The HTML export keeps the section (Q5).

The writing skill, `docs/user/charts.md` and the requirements (SwRS-MDOKFSTUDIO-DIAG-121 and
DIAG-123) follow the change.
