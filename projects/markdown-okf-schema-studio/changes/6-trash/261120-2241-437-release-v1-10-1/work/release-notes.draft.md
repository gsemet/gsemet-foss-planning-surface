<h1 align="center">Markdown OKF-Schema Studio 1.10.1</h1>

<p align="center">
  <b>Editing a file with Windows line endings no longer leaves the editor stuck.</b><br>
  <sub>2 changes since 1.10.0 · VS Code 1.95 or later · MIT</sub>
</p>

<p align="center">
  <a href="https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio">Install from VS Code Marketplace</a> ·
  <a href="https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio">Install from Open VSX</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio#readme">Read the guide</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/blob/v1.10.1/CHANGELOG.md">Full changelog</a> ·
  <a href="https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.0.0">1.0 showcase</a>
</p>

---

## 🛠 No more "Saving Markdown..." on CR LF files

In a file with CR LF line endings, leaving a block editor without a change could leave the page on
"Saving Markdown..." for good. It now returns to the page at once, and a block you edit keeps the
line endings of its file.

<details><summary><b>🛠 For contributors</b></summary>

- The test fixtures that hold CR LF line endings now stay CR LF, and the save tests cover CR LF, LF
  and mixed files, so a save that changes a file's line endings fails a test.

</details>
