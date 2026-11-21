# Diagnosis: CI visual red, CORE-001 caption "runs past the map"

CR-441, PR #450 at 13cb386b. Failing test: `test/site/requirementsViewer/metroMap.browser.test.ts`,
"every use case of the requirements report draws its map without an overlap at both widths"
(CI log `work/ci-44844766446.log`, line 854 on). Two problems only, both for
StRS-MDOKFSTUDIO-CORE-001 (1280 and 800 px):
`"a long word, URL or Japanese, Chinese or Korean paragraph wraps in" runs past the map`.

## Reproduction (Windows, passes) and the numbers

Probe: `work/debugger/probe.cjs` (run from the worktree root with `node`; it builds the viewer pages of
`out/reports/requirements/requirements-report.json`, opens CORE-001 in Chromium with `pinSiteFonts`, and
prints the caption's box). Result, local Windows Chromium:

| item | value |
| --- | --- |
| caption | 66 characters, one line, `italic 13.5px "Studio Test Serif"` (KaTeX_Main-Italic) |
| measured width (1280 px) | 407.8 px (6.18 px per character) |
| layout estimate `len * CHAR` (CHAR = 6.4) | 422.4 px |
| caption left (`stem + 24`) | 358 px |
| `svg` natural width = frame width | 797 px = ceil(358 + 422.4 + 16) |
| check's widened right edge | 358 + 407.8 * 1.05 = 786.1 px, under 797 (passes, 10.9 px spare) |

The test widens each text by 5 % per side (`widen`, line 44) and requires it to stay inside the SVG frame.

## Cause

`layout.ts` line 425 sets the map's right extent from an estimate of the widest outcome caption:

    right = Math.max(right, stem + 24 + Math.max(...caption.map((line) => line.length * CHAR)), ...)
    fullWidth = Math.ceil(Math.max(width, right + 16))     // line 450

So the room right of the caption is `(CHAR * len - real width) + 16` px: a fixed 16 px plus whatever the
estimate over-shoots the font. Here that is 14.6 + 16 = 30.6 px on Windows, of which the test needs
5 % of 408 = 20.4 px. The slack is thin because the estimate and the padding are not proportional to the label:
the 5 % check grows with the caption, the 16 px does not, and the 6.4 px per character is only 3.6 % above the
pinned font's 6.18 on this machine (the caption is the longest line the map holds, wrapped at `INLINE_ROOM` 460 px,
so it is the case with the biggest absolute need).

The check fails as soon as the real width W satisfies 358 + 1.05 W > 797, that is W > 418.1 px, i.e. more than
6.33 px per character: only +2.5 % over the Windows rendering. The pinned fonts make the glyph outlines and design
advances identical on every machine, but the rasteriser is not: Linux Chromium (FreeType, fontconfig hinting,
integer glyph advances at 13.5 px; Windows uses DirectWrite with fractional advances) lays text out a little wider.
A 2.5 % widening of a 66-character line is the usual size of that effect. I could not prove the Linux number:
no Linux Chromium here, and the log prints only the problem text, not the measured width. What is proved is the
margin arithmetic above (the line is the only one so close, since it is the single caption that fills the
whole 460 px room) and that the layout leaves only 2.5 % of tolerance. Per-glyph probe `work/debugger/round.cjs`
shows that plain rounding of advances gives 407 px (no change), so the Linux excess comes from hinted advances,
not from rounding: treat "Linux is at least 2.5 % wider" as inferred.

The wrap itself has the same weakness: `wrapOf` (line 330) counts `floor((room - 24) / CHAR)` characters per line, with
the same bare CHAR. A wider font could push a wrapped line into the next column's state, though no check caught it yet.

## Place to fix (layout, not the check)

`test/site/requirementsViewer/layout.ts`:

1. Line 425: use the existing `WIDTH_MARGIN` (1.1, already applied to pills, line 176) on the caption estimate:
   `line.length * CHAR * WIDTH_MARGIN`. Spare room becomes about 464 - 408 + 16 = 72 px, enough for text 17 % wider than
   the pinned Windows rendering (the test needs 5 % of the line on top). Cost: the map is about 42 px wider only when an
   outcome caption is the widest item, which is rare, and it shows as blank room on the right.
2. Line 330 (`wrapOf`): divide by `CHAR * WIDTH_MARGIN` too, so a caption never grows past the room that was reserved for
   it: 460 px room gives 62 characters per line instead of 68. The "66 characters" caption then wraps in two lines.
   (Lines 332-334 use the same CHAR for `roomOf`; keep them consistent with the same constant.)
3. Better but heavier: take the widths from a measure instead of an estimate (canvas `measureText` with the pinned
   font cannot run at build time, so a per-character width table of the pinned serif, with the hinted maximum, would do).
   Not needed if 1 and 2 are applied.

After the fix, re-run `just ci-visual` on Linux (CI) to confirm; the frozen-use-case tests and the full-ID test must keep
passing since their captions are shorter.
