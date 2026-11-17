# Plan: render inline SVG

What Markdown OKF-Schema Studio will do for SVG written straight into Markdown. Accepted, not
scheduled yet; the pull request will be linked on the issue.

## What renders

- A fenced block with the `svg` language.
- A raw `<svg>` element that fills a whole block. A `<svg>` inside a sentence stays dropped.

Both show as a picture. A click in edit mode opens the source editor of the block, as for a Mermaid
diagram.

## Safety

The SVG is cleaned, then placed in the page. Cleaning removes:

- scripts and event handlers (`onclick` and the like);
- `foreignObject`;
- links to other sites;
- `<style>` elements.

It also renames `id`s, so two SVGs on one page cannot clash.

## Theme colours

An SVG can use these CSS variables. Each one follows the Cream, White and Dark themes:

| Variable | Meaning |
| --- | --- |
| `--surface`, `--background`, `--bg` | Block background |
| `--border` | Borders and separators |
| `--text`, `--foreground`, `--fg` | Text |
| `--muted` | Secondary text |
| `--accent`, `--primary` | Accent |
| `--red`, `--green`, `--blue`, `--orange` | Named colours, adjusted for light and dark |

An unknown variable uses the fallback written in `var()`, else the text colour.

## Size

The picture keeps its `viewBox` and declared width, never wider than the text column. In Auto width
it may break out of the column like an image.

## Writing skill

The writing skill shipped with the extension will describe:

- both forms;
- the variables above;
- what cleaning removes;
- when a separate `.svg` file shown with `{figure}` is still the better choice.
