# Auto width: linked or multi-image paragraphs do not widen

In width mode Auto, two kinds of top-level image paragraphs do not widen as
SwRS-MDOKFSTUDIO-LAYOUT-023 says an oversized image should:

1. A linked image alone in a top-level paragraph is not widened.
2. A top-level paragraph holding no text and several images, at least one of them not wrapped in a
   link or another element, is measured and marked as a whole, once, from its first image's sizes,
   so a wide image after a narrow first one does not widen it.

Found while CR-511 (`nested-code-blocks-do-not-widen-in-auto`, requirements only) restated
LAYOUT-023; CR-511 records both as a Known issue on that requirement and does not change the code.

Asked: fix the code. Not grilled yet (expected layout for a paragraph of several images is open).

Origin: Foreman ask A-31, 2026-11-26.
