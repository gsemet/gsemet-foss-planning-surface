# Dropdown content lost in the preview

Found by the spec critic of blank-runs-inside-quotes-admonitions (2026-11-21): ':::{dropdown} Dd' renders as an empty, unmapped <details></details> on origin/main 2d3187b6: its content is lost in the preview. Probe: a colon-fence dropdown with a title and a paragraph body. Fix: render and map the dropdown body.