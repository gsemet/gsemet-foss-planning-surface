Thank you for the detailed report and the reproduction document.

Your report has been taken up. Two changes (#549 and #550) are merged on `main`. They are not released yet and will be in the next release.

- **Restyling after a content change** (#549): the three `:has()` rules on the preview content root are replaced by one attribute on that root.
- **Selection, hover and scroll** (#549): the Comment button, the hover outline and the copy button are updated at most once per frame, a scroll only moves the Comment button, and a selection ending at the very start of a block no longer lists every source line of the document.
- **Comment updates** (#550): only the highlights, badges and orphan entries that differ are changed, and the page is measured again only when a block can have moved.

Measured in a real VS Code window on a Linux CI runner, on a generated document of the same shape as yours (about 464 lines, 22 tables, 11 SVG images, 9 comment threads), over three runs:

- Elements restyled when one comment is created: 3109 before, 41 after #549, 4 after #550.
- Comment save to highlight drawn: median 53 ms before, 46 ms after #549. The further effect of #550 on this time is within runner noise.

What we have not shown:

- We did not reproduce the slow text selection: before these changes, no drag or release blocked the page for more than 50 ms in our runs, and the selection timings did not change measurably.
- We cannot yet say that comment creation is no longer slow on your machine.
- Every comment write still indexes the document and re-anchors all threads in the extension (about 2 ms for 9 threads on our document, timed outside VS Code), and adding or deleting a comment on selected words still measures the page.

Could you try the next release on your document? If it is still slow, your VS Code version, your OS, roughly how long selecting text and creating a comment take, and if possible a Developer Tools performance recording of the preview would help us a lot. This issue stays open meanwhile.
