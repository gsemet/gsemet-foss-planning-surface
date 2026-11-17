# Front matter change bars: follow-ups

Non-blocking review notes from the front matter change bars fix
(PR [#169](https://github.com/gsemet/markdown-okf-schema-studio/pull/169)):

- A source that starts with a BOM gets no row bars on the properties table.
- The removed-field case (bar on the whole properties table) has unit tests but no visual scenario.
- The before/after screenshots of the front matter change-bar scenarios have a large blank area
  under the document; crop the capture to the content.
