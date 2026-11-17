# Retro — 297-release-1-7-0

| What happened | Root cause | Process fix |
| --- | --- | --- |
| The owner did not see what an exported HTML file looks like in the notes; a second round added a screenshot of the real exported file (JavaScript off) | The release driver reused only the screenshots the change produced; the export change had a picture of the preview with the Export button, and its picture of an exported file came from the static visual campaign, which never draws Mermaid | Rule candidate for `release-process.guidelines.md` ("Images"): when a highlight produces an artifact outside VS Code (a file, a page), the notes show that artifact itself, captured from a real run |
| The driver flagged a doubt on the Mermaid wording of the changelog, from a P3 backlog item (`static-export-mermaid-as-source`) | That backlog item was filed from the static visual campaign, where Mermaid never draws; it describes the harness, not the product | Close or reword the backlog item (the Chief of Staff verified the embedding in real VS Code) |
| `sips --cropOffset` cropped from the centre, not the top, and gave a wrong image | macOS `sips` ignores the offset with `-c` | None: use ImageMagick (`magick in.png -crop WxH+0+0 +repage out.png`) for release images |
| Foreground waits on CI were moved to the background after 180 s, and a chained `sleep` was refused | Harness limits on foreground commands | None: watch long runs with Monitor and an until-loop from the start |
