# Verify CR-300 at ae16c9fb
Command: `npm run site` in the worktree (after `rm -rf out/site`); built OK.
- og/*.png written: gallery, home, contributing, how-we-ship; PIL sizes all (1200, 630).
- `grep -cE 'og:|twitter:'`: gallery/index/contributing/docs/how-we-ship.html = 15 each; requirements.html and the other docs/*.html = 0.
- Gallery tags: og:image = https://gsemet.github.io/markdown-okf-schema-studio/og/gallery.png, width 1200, height 630, twitter:card summary_large_image.
- Live count: page says "542 E2E screenshots", 542 image files on disk, card and meta say 542, mosaic of 3 tiles.
- site-manifest.json lists the four cards.
- Pictures viewed: nothing cut off; gallery card has title, count, line, 3-tile mosaic.
Not run: unit tests, CI workflows (pages dry run, heavy gallery), before worktree (new files only; pages without card unchanged = 0 tags).
Evidence: work/verifier/evidence/{gallery,home,contributing,how-we-ship}.png
VERIFIED
