# How the annotated Expected images of the 210 backlog items were made

Honest summary first: the tool was ImageMagick 7 (`magick`, /opt/homebrew/bin/magick). PIL is not
installed, `sips` cannot draw (it was only used for `sips -Z 1000` at the end). The rectangle
coordinates were NOT computed from selectors: I read them by eye from screenshots I had opened,
in the pixel space of the saved JPEG. Section 2 gives the selector-based method a driver feature
should use instead; that method is described, not tested by me.

## 1. Tool and exact commands

Font: ImageMagick had no default font ("unable to read font"), so every text command passes
`-font /System/Library/Fonts/Supplemental/Arial.ttf` (macOS).

Colours: red `rgb(200,30,30)` = the defect, green `rgb(30,140,50)` = expected / working case,
dark grey `rgb(40,40,40)` = panel label bar. White text, 14 pt.
Line width: 3 px, no fill (`-fill none -stroke COLOR -strokewidth 3`).

Three shell functions did everything:

```bash
F=/System/Library/Fonts/Supplemental/Arial.ttf
RED="rgb(200,30,30)"; GRN="rgb(30,140,50)"

# outline: box IN OUT COLOR x1 y1 x2 y2   (JPEG pixel coordinates)
box(){ magick "$1" -fill none -stroke "$3" -strokewidth 3 -draw "rectangle $4,$5 $6,$7" "$2"; }

# one-line caption band at the BOTTOM: note IN OUT COLOR "text"
# (-gravity south BEFORE -splice, otherwise the band lands in the middle of the image)
note(){ magick "$1" -background "$3" -fill white -font $F -pointsize 14 \
        -gravity south -splice 0x40 -annotate +0+11 "$4" "$2"; }

# label band at the TOP, used above each panel of a before/after pair: lab IN "text" OUT
lab(){ magick "$1" -background "rgb(40,40,40)" -fill white -font $F -pointsize 14 \
       -gravity north -splice 0x30 -annotate +0+7 "$2" "$3"; }
```

No arrows were drawn; only rectangles plus the bottom note. (An arrow would be
`-draw "line x1,y1 x2,y2"` plus a small `polygon`; not used.)

Crops before annotating: `magick shot.jpg -crop 490x430+0+0 +repage out.jpg`
(`WxH+X+Y`, `+repage` is required or the canvas offset leaks into later steps).

## 2. Coordinates: window pixels to shot pixels

Scale. `q shot NAME --clip preview` captures the preview webview rectangle (from `q frames`:
here x=746 y=65 width=393 height=802, window coordinates in CSS px) and saves it with the
default `--px 1000`, which scaled the HEIGHT to 1000: 802 -> 1000, so the factor is
1000/802 = 1.247 and the shot was 490x1000 (393*1.247 = 490). After the sash drag the pane was
566 wide and the same rule applied. Check with `sips -g pixelWidth -g pixelHeight shot.jpg`.

What I did: opened the shot and estimated the rectangle in shot pixels (so no conversion was
needed). Examples: `box c1-1-before.jpg e1.jpg GRN 68 385 435 610` (link card),
`box c3.jpg e4.jpg RED 58 232 345 268` (lazy line).

Recommended for the driver feature (method, untested): get the element box from the driver
itself, which already returns window coordinates:

```bash
q box 'aside[data-okf-github-alert]' --limit 1     # -> {x,y,w,h} in window coordinates
q frames                                           # -> webview {x,y,width,height} = clip origin
# shot pixel = (window px - clip origin) * S,  S = shot_height / clip_height  (1000/802 = 1.247)
# x1=(b.x-fx)*S  y1=(b.y-fy)*S  x2=(b.x+b.w-fx)*S  y2=(b.y+b.h-fy)*S
```
Take the box right before the shot, with the same scroll position, and keep the margin of a few
px around the box. Compute S from the real JPEG size, not from the 1000 constant.

## 3. Montages and resizing to 1000 px

Before/after pair (two shots side by side, each with a label band), final width 490*2 = 980:

```bash
lab c1-1-before.jpg "1. Edit mode, double-click the card header" a1.jpg
lab c1-1-fail.jpg   "2. The preview opens targets/alpha.md"      a2.jpg
magick a1.jpg a2.jpg +append currently.jpg          # +append = horizontal, -append = vertical
```
Both inputs must have the same height; they came from the same clip so they did.

Final resize of every evidence file (never enlarges below 1000 on the long side, keeps ratio):
`sips -Z 1000 file.jpg`. Note that -Z bounds the LONGER side, so a 490x1000 shot is unchanged.

Contact sheets for my own review (not saved as evidence), to open many shots in one image:
`magick montage a.jpg b.jpg c.jpg -tile 3x2 -geometry 330x+4+4 sheet.jpg`.

## 4. Worked example: item alert-palette-after-lazy-continuation

Fixture `synth/admon.md` (a Note and a plain quote, each with a lazy continuation line):

```
# Admonitions

> [!NOTE]
> Line one of a note.
lazy continuation line of the note.

Between paragraph.

> Line one of a quote.
lazy continuation line of the quote.
```

```bash
export QA_SESSION=ev
# 1. shot of the symptom (scenario c3-1 with an unconditional shot step; same as `q shot`)
q shot c3-1 --clip preview            # -> runs/ev/shots/c3-1.jpg  (490x1000)

# 2. crop to the interesting top part, keep as Currently
magick c3-1.jpg -crop 490x430+0+0 +repage c3a.jpg
cp c3a.jpg .../P2/alert-palette-after-lazy-continuation/evidence/currently.jpg

# 3. Expected = same crop, red outline on the misplaced lazy line,
#    green outline on the plain quote that renders right, green caption band
box c3a.jpg e4.jpg  "$RED" 58 232 345 268
box e4.jpg  e4b.jpg "$GRN" 64 327 427 410
note e4b.jpg .../evidence/expected.jpg "$GRN" \
     "Expected: lazy line inside the Note, as the quote below renders it"

# 4. resize guard
sips -Z 1000 .../evidence/expected.jpg
```
The intent file then embeds `evidence/currently.jpg` and `evidence/expected.jpg` in a
`| Currently | Expected |` table with one caption row.

## 5. Pitfalls met

- `cp`/`rm` are aliased to interactive mode: use `\cp -f`, `\rm`. One `cp` silently did not
  overwrite and left a stale image until I re-ran it.
- Reusing one temp filename for two items overwrote the first (an item-10 image ended up in item 04).
  Use per-item temp names or a temp dir per item.
- `-gravity center` before `-splice` puts the band in the middle of the image.
- ImageMagick needs an explicit TTF path on this machine.
- Scenario shots with `"onFail": true` are only taken on failure; for evidence strip it
  (`perl -pi -e 's/,\s*"onFail":\s*true//'`; BSD `sed -i ''` failed here) or add explicit shot steps.
- Take the shot at the symptom moment, not at the scenario end (several replays end after Escape
  or after navigating away, which hides the symptom).
