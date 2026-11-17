# Keyboard navigation: follow-ups

Non-blocking review notes from the empty-document keyboard start
(PR [#171](https://github.com/gsemet/markdown-okf-schema-studio/pull/171)) and the structural keyboard navigation
(PR [#170](https://github.com/gsemet/markdown-okf-schema-studio/pull/170)), both landed on main with PR [#166](https://github.com/gsemet/markdown-okf-schema-studio/pull/166):

- Right on a tab can select a block in an inactive (hidden) panel; it should go into the shown
  panel only.
- The editing guide line saying a mouse move hides the selection ring is true for block rings
  only, not for the table-cell ring or the Start writing ring.
- The real-window step in test/integration/realInput/blockKeys.ts may need a focus click on the
  page (as in windowSwitchKeys.test.ts) before the keys, if it flakes.
- SwRS-MDOKFSTUDIO-BLOCK-253 has no `@implements_req` marker in `createInsertPoint`
  (src/page/features/insertPoints.ts), and its verification notes cite
  test/page/runtimeBlockEditor.test.ts, which carries no marker for it.
