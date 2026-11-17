// src/core/palette/emoji.ts
var EMOJI_SOURCE = [
  ["smileys", "Smileys", "\u{1F600} grinning face;\u{1F603} smiling face with big eyes;\u{1F604} smiling face with smiling eyes;\u{1F601} beaming face;\u{1F606} grinning squinting face laugh;\u{1F605} grinning face with sweat;\u{1F602} face with tears of joy;\u{1F642} slightly smiling face;\u{1F643} upside-down face;\u{1F609} winking face;\u{1F60A} smiling face with blush;\u{1F607} smiling face with halo angel;\u{1F60D} smiling face with heart eyes;\u{1F929} star-struck;\u{1F618} face blowing a kiss;\u{1F60B} face savoring food yum;\u{1F60E} smiling face with sunglasses cool;\u{1F914} thinking face;\u{1F610} neutral face;\u{1F634} sleeping face;\u{1F622} crying face sad;\u{1F62D} loudly crying face;\u{1F621} pouting face angry;\u{1F631} face screaming in fear;\u{1F92F} exploding head mind blown;\u{1F973} partying face"],
  ["people", "People and hands", "\u{1F44D} thumbs up like;\u{1F44E} thumbs down dislike;\u{1F44F} clapping hands applause;\u{1F64C} raising hands celebration;\u{1F64F} folded hands please thanks pray;\u{1F91D} handshake agreement;\u{1F44B} waving hand hello;\u270B raised hand stop;\u{1F44C} ok hand;\u270C\uFE0F victory hand peace;\u{1F91E} crossed fingers luck;\u{1F449} backhand index pointing right;\u{1F448} backhand index pointing left;\u{1F446} backhand index pointing up;\u{1F447} backhand index pointing down;\u{1F4AA} flexed biceps strong;\u{1F937} person shrugging;\u{1F926} person facepalming;\u{1F64B} person raising hand;\u{1F440} eyes look;\u{1F9E0} brain;\u{1F464} bust in silhouette user;\u{1F468}\u200D\u{1F4BB} man technologist;\u{1F469}\u200D\u{1F4BB} woman technologist"],
  ["nature", "Nature", "\u{1F331} seedling sprout;\u{1F332} evergreen tree;\u{1F333} deciduous tree;\u{1F338} cherry blossom;\u{1F339} rose;\u{1F33B} sunflower;\u{1F340} four leaf clover;\u{1F341} maple leaf;\u{1F525} fire flame;\u{1F4A7} droplet water;\u{1F30A} water wave;\u26A1 high voltage lightning;\u2600\uFE0F sun;\u{1F319} crescent moon;\u2B50 star;\u{1F31F} glowing star;\u2744\uFE0F snowflake;\u{1F308} rainbow;\u2601\uFE0F cloud;\u{1F41B} bug insect;\u{1F41E} lady beetle;\u{1F41D} honeybee;\u{1F98B} butterfly;\u{1F419} octopus;\u{1F427} penguin;\u{1F98A} fox;\u{1F431} cat face"],
  ["food", "Food and drink", "\u{1F34E} red apple;\u{1F34F} green apple;\u{1F34C} banana;\u{1F347} grapes;\u{1F353} strawberry;\u{1F34B} lemon;\u{1F951} avocado;\u{1F955} carrot;\u{1F33D} ear of corn;\u{1F35E} bread;\u{1F9C0} cheese wedge;\u{1F355} pizza;\u{1F354} hamburger;\u{1F35F} french fries;\u{1F32E} taco;\u{1F363} sushi;\u{1F36A} cookie;\u{1F370} shortcake cake;\u{1F36B} chocolate bar;\u{1F369} doughnut;\u2615 hot beverage coffee;\u{1F375} teacup tea;\u{1F37A} beer mug;\u{1F377} wine glass"],
  ["objects", "Objects", "\u{1F4BB} laptop computer;\u{1F5A5}\uFE0F desktop computer;\u2328\uFE0F keyboard;\u{1F4F1} mobile phone;\u{1F4A1} light bulb idea;\u{1F527} wrench tool;\u{1F528} hammer;\u2699\uFE0F gear settings;\u{1F512} locked padlock;\u{1F513} unlocked padlock;\u{1F511} key;\u{1F4C1} file folder;\u{1F4C2} open file folder;\u{1F4C4} page facing up document;\u{1F4DD} memo note;\u{1F4CE} paperclip;\u{1F4C5} calendar;\u{1F4CA} bar chart;\u{1F4C8} chart increasing;\u{1F4C9} chart decreasing;\u{1F50D} magnifying glass search;\u{1F4E6} package box;\u{1F680} rocket launch;\u{1F3AF} direct hit target;\u{1F389} party popper tada;\u{1F3C6} trophy;\u{1F4DA} books;\u{1F514} bell notification"],
  ["symbols", "Symbols and status", "\u2705 check mark button done;\u2611\uFE0F check box with check;\u2714\uFE0F check mark;\u274C cross mark;\u274E cross mark button;\u26A0\uFE0F warning;\u{1F6AB} prohibited;\u26D4 no entry;\u2757 red exclamation mark;\u2753 red question mark;\u2139\uFE0F information;\u2795 plus;\u2796 minus;\u27A1\uFE0F right arrow;\u2B05\uFE0F left arrow;\u2B06\uFE0F up arrow;\u2B07\uFE0F down arrow;\u{1F504} counterclockwise arrows button refresh;\u{1F501} repeat button;\u2764\uFE0F red heart;\u{1F494} broken heart;\u{1F4AF} hundred points;\u{1F197} ok button;\u{1F534} red circle;\u{1F7E2} green circle;\u{1F535} blue circle"]
];
var EMOJI_CATEGORIES = EMOJI_SOURCE.map(([id, label, list]) => ({
  id,
  label,
  items: list.split(";").map((entry) => {
    const space = entry.indexOf(" ");
    return { char: entry.slice(0, space), name: entry.slice(space + 1) };
  })
}));

// src/core/palette/paletteActions.ts
var ALERT_TYPES = ["NOTE", "TIP", "IMPORTANT", "WARNING", "CAUTION"];
var ADMONITION_TYPES = [
  "note",
  "tip",
  "important",
  "warning",
  "caution",
  "danger",
  "attention",
  "error",
  "hint",
  "seealso"
];
var COLUMN_ALIGNMENTS = ["left", "center", "right"];
var ALERT_OPTIONS = ALERT_TYPES.map((type) => ({
  value: type,
  label: type.charAt(0) + type.slice(1).toLowerCase()
}));
var ADMONITION_OPTIONS = [
  ...ADMONITION_TYPES.map((type) => ({
    value: type,
    label: type === "seealso" ? "See also" : type.charAt(0).toUpperCase() + type.slice(1)
  })),
  { value: "custom", label: "Custom\u2026" }
];
var COLOUR_SWATCHES = [
  "#e53935",
  "#fb8c00",
  "#fdd835",
  "#43a047",
  "#00897b",
  "#1e88e5",
  "#8e24aa",
  "#757575",
  "#ffcdd2",
  "#ffe0b2",
  "#fff9c4",
  "#c8e6c9",
  "#b2dfdb",
  "#bbdefb",
  "#e1bee7",
  "#e0e0e0"
];
var HEADING_OPTIONS = [
  { value: "0", label: "Paragraph" },
  ...[1, 2, 3, 4, 5].map((level) => ({ value: String(level), label: "Heading " + level }))
];
var HEADING_SLASH = [
  ...[1, 2, 3, 4, 5].map((level) => ({
    label: "Heading " + level,
    arg: String(level),
    aliases: level === 1 ? ["h1", "title", "heading1"] : ["h" + level, "heading" + level]
  })),
  { label: "Paragraph", arg: "0", aliases: ["text", "plain", "p"] }
];
var ALERT_SLASH = ALERT_OPTIONS.map((option) => ({
  label: option.label + " alert",
  arg: option.value,
  aliases: [option.label.toLowerCase(), "callout", "github"]
}));
var ADMONITION_SLASH = ADMONITION_OPTIONS.map((option) => ({
  label: option.value === "custom" ? "Custom admonition" : option.label + " admonition",
  arg: option.value,
  aliases: [option.value === "seealso" ? "see also" : option.value, "callout", "admonition"]
}));
var PALETTE_ACTIONS = {
  heading: {
    slash: { variantsOnly: true, variants: HEADING_SLASH },
    label: "Heading",
    title: "Heading level",
    icon: "heading",
    group: "block",
    modes: ["strict"],
    scopes: ["block"],
    popover: "heading",
    options: HEADING_OPTIONS
  },
  bold: {
    slash: { aliases: ["strong", "b"] },
    label: "Bold",
    icon: "bold",
    group: "inline",
    modes: ["strict"],
    scopes: ["block", "cell"],
    shortcut: { codes: ["KeyB"], keys: ["b"] }
  },
  italic: {
    slash: { aliases: ["emphasis", "em", "i"] },
    label: "Italic",
    icon: "italic",
    group: "inline",
    modes: ["strict"],
    scopes: ["block", "cell"],
    shortcut: { codes: ["KeyI"], keys: ["i"] }
  },
  strikethrough: {
    slash: { aliases: ["strike", "del", "delete"] },
    label: "Strikethrough",
    icon: "strikethrough",
    group: "inline",
    modes: ["strict"],
    scopes: ["block", "cell"]
  },
  color: {
    slash: { aliases: ["color", "highlight", "background"] },
    label: "Colour",
    title: "Colour the text or its background",
    icon: "color",
    group: "inline",
    modes: ["strict"],
    scopes: ["block", "cell"],
    popover: "color",
    colors: COLOUR_SWATCHES
  },
  colorCode: {
    label: "Colour code",
    title: "Change this colour code",
    icon: "colorCode",
    group: "inline",
    modes: ["strict"],
    scopes: ["block", "cell"],
    popover: "color",
    colors: COLOUR_SWATCHES
  },
  link: {
    slash: { aliases: ["url", "hyperlink"] },
    label: "Link",
    title: "Link",
    icon: "link",
    group: "inline",
    modes: ["strict"],
    scopes: ["block", "cell"],
    shortcut: { codes: ["KeyK"], keys: ["k"] },
    panel: "link"
  },
  image: {
    slash: { aliases: ["img", "picture", "photo"] },
    label: "Image",
    title: "Image (pick a file next to the document)",
    icon: "image",
    group: "inline",
    modes: ["strict"],
    scopes: ["block"],
    hostDialog: "image"
  },
  codeFence: {
    slash: { aliases: ["code", "fence", "snippet", "pre"] },
    label: "Code block",
    title: "Code block (choose a language)",
    icon: "code",
    group: "block",
    modes: ["strict"],
    scopes: ["block"],
    popover: "language"
  },
  bulletList: {
    slash: { menuOnly: true, aliases: ["bullet", "bullets", "ul", "unordered", "list", "-", "*"] },
    label: "Bulleted list",
    icon: "bulletList",
    group: "block",
    modes: ["strict"],
    scopes: ["block"]
  },
  numberedList: {
    slash: { menuOnly: true, aliases: ["numbered", "ol", "ordered", "list", "1."] },
    label: "Numbered list",
    icon: "numberedList",
    group: "block",
    modes: ["strict"],
    scopes: ["block"]
  },
  quote: {
    slash: { aliases: ["quote", "citation", "bq"] },
    label: "Blockquote",
    icon: "quote",
    group: "block",
    modes: ["strict"],
    scopes: ["block"]
  },
  rule: {
    slash: { aliases: ["hr", "divider", "line", "separator"] },
    label: "Horizontal rule",
    icon: "rule",
    group: "block",
    modes: ["strict"],
    scopes: ["block"]
  },
  table: {
    slash: { aliases: ["grid", "tbl"] },
    label: "Table",
    title: "Table (choose a size)",
    icon: "table",
    group: "block",
    modes: ["strict"],
    scopes: ["block"],
    popover: "grid",
    grid: { rows: 9, cols: 9 }
  },
  emoji: {
    slash: { aliases: ["smiley", "emoticon", "face"] },
    label: "Emoji",
    title: "Emoji",
    icon: "emoji",
    group: "insert",
    modes: ["strict"],
    scopes: ["block", "cell"],
    popover: "emoji",
    emoji: EMOJI_CATEGORIES
  },
  todo: {
    slash: { aliases: ["todo", "fixme", "task"] },
    label: "TODO",
    title: "Toggle TODO comment",
    icon: "todo",
    group: "annotation",
    modes: ["strict"],
    scopes: ["block"],
    shortcut: { codes: ["Slash"], keys: ["/"], anyShift: true, modifier: "any" }
  },
  thread: {
    slash: { aliases: ["thread", "discussion", "comment"] },
    label: "Thread",
    title: "Insert a comment thread",
    icon: "thread",
    group: "annotation",
    modes: ["strict"],
    scopes: ["block"]
  },
  alert: {
    slash: { aliases: ["callout", "github"], variants: ALERT_SLASH },
    label: "Alert",
    title: "GitHub alert (choose a type)",
    icon: "alert",
    group: "github",
    modes: ["gfm"],
    scopes: ["block"],
    popover: "alert",
    popoverAtCaret: true,
    options: ALERT_OPTIONS
  },
  checkbox: {
    slash: { aliases: ["todo", "task", "checklist", "tasklist"] },
    label: "Checkbox",
    title: "Toggle checkbox",
    icon: "checkbox",
    group: "github",
    modes: ["gfm"],
    scopes: ["block"]
  },
  htmlTable: {
    slash: { aliases: ["table", "html"] },
    label: "HTML table",
    title: "HTML table (converts the table at the caret)",
    icon: "htmlTable",
    group: "github",
    modes: ["gfm"],
    scopes: ["block"]
  },
  details: {
    slash: { aliases: ["collapse", "toggle", "spoiler", "accordion"] },
    label: "Collapsible",
    title: "Collapsible section (details)",
    icon: "details",
    group: "github",
    modes: ["gfm"],
    scopes: ["block"]
  },
  footnote: {
    slash: { aliases: ["fn", "endnote"] },
    label: "Footnote",
    title: "Footnote",
    icon: "footnote",
    group: "github",
    modes: ["gfm"],
    scopes: ["block"]
  },
  mermaid: {
    slash: { aliases: ["diagram", "chart", "graph", "flowchart"] },
    label: "Mermaid",
    title: "Mermaid diagram",
    icon: "mermaid",
    group: "github",
    modes: ["gfm"],
    scopes: ["block"]
  },
  columnAlign: {
    slash: { aliases: ["align", "left", "center", "right"] },
    label: "Column alignment",
    title: "Table column alignment (choose)",
    icon: "columnAlign",
    group: "github",
    modes: ["gfm"],
    scopes: ["block"],
    popover: "align",
    options: [
      { value: "left", label: "Left" },
      { value: "center", label: "Center" },
      { value: "right", label: "Right" }
    ]
  },
  kbd: {
    slash: { aliases: ["kbd", "key", "keyboard", "shortcut"] },
    label: "Key",
    title: "Keyboard key (kbd)",
    icon: "kbd",
    group: "github",
    modes: ["gfm"],
    scopes: ["block", "cell"]
  },
  admonition: {
    slash: { aliases: ["callout"], variants: ADMONITION_SLASH },
    label: "Admonition",
    title: "Admonition (choose a type)",
    icon: "admonition",
    group: "myst",
    modes: ["myst"],
    scopes: ["block"],
    popover: "admonition",
    options: ADMONITION_OPTIONS
  },
  deflist: {
    slash: { aliases: ["definition", "dl", "glossary"] },
    label: "Definition list",
    title: "Definition list",
    icon: "deflist",
    group: "myst",
    modes: ["myst"],
    scopes: ["block"]
  },
  math: {
    slash: { aliases: ["equation", "latex", "formula", "katex"] },
    label: "Math",
    title: "Math (choose inline, display or aligned)",
    icon: "math",
    group: "myst",
    modes: ["myst"],
    scopes: ["block"],
    popover: "math",
    options: [
      { value: "inline", label: "Inline $\u2026$" },
      { value: "display", label: "Display $$" },
      { value: "aligned", label: "Aligned equations" }
    ]
  },
  sub: {
    slash: { aliases: ["subscript"] },
    label: "Subscript",
    title: "Subscript",
    icon: "sub",
    group: "myst",
    modes: ["myst"],
    scopes: ["block", "cell"]
  },
  sup: {
    slash: { aliases: ["superscript", "power", "exponent"] },
    label: "Superscript",
    title: "Superscript",
    icon: "sup",
    group: "myst",
    modes: ["myst"],
    scopes: ["block", "cell"]
  },
  label: {
    slash: { aliases: ["anchor", "target"] },
    label: "Label",
    title: "Label (anchor for {ref})",
    icon: "label",
    group: "myst",
    modes: ["myst"],
    scopes: ["block"]
  },
  ref: {
    slash: { aliases: ["reference", "xref", "crossref"] },
    label: "Reference",
    title: "Reference to a label ({ref})",
    icon: "ref",
    group: "myst",
    modes: ["myst"],
    scopes: ["block"],
    popover: "choices",
    hostList: "targets"
  },
  doc: {
    slash: { aliases: ["document", "file", "page"] },
    label: "Document link",
    title: "Link to another document ({doc})",
    icon: "doc",
    group: "myst",
    modes: ["myst"],
    scopes: ["block"],
    hostDialog: "document"
  },
  cite: {
    slash: { aliases: ["cite", "citation", "bibtex", "bibliography"] },
    label: "Citation",
    title: "Citation from the workspace .bib files ({cite})",
    icon: "cite",
    group: "myst",
    modes: ["myst"],
    scopes: ["block"],
    popover: "choices",
    hostList: "citations"
  },
  dropdown: {
    slash: { aliases: ["details", "collapse"] },
    label: "Dropdown",
    title: "Dropdown (collapsible admonition)",
    icon: "dropdown",
    group: "myst",
    modes: ["myst"],
    scopes: ["block"]
  },
  tableCaption: {
    slash: { aliases: ["table", "caption", "list-table"] },
    label: "Table with caption",
    title: "Table with caption (wraps the table at the caret)",
    icon: "tableCaption",
    group: "myst",
    modes: ["myst"],
    scopes: ["block"]
  },
  listTable: {
    slash: { aliases: ["list-table", "table", "convert"] },
    label: "List table",
    title: "Convert the pipe or HTML table at the caret to a {list-table}",
    icon: "listTable",
    group: "myst",
    modes: ["myst"],
    scopes: ["block"]
  },
  pipeTable: {
    slash: { aliases: ["pipe", "table", "convert"] },
    label: "Pipe table",
    title: "Convert the {list-table} or HTML table at the caret to a Markdown pipe table",
    icon: "pipeTable",
    group: "myst",
    modes: ["myst"],
    scopes: ["block"]
  },
  figure: {
    slash: { aliases: ["fig", "image", "picture"] },
    label: "Figure",
    title: "Figure (pick an image file; with the caret in a figure, edit it)",
    icon: "figure",
    group: "myst",
    modes: ["myst"],
    scopes: ["block"],
    hostDialog: "image",
    panelWhenInside: "figure"
  },
  roleKbd: {
    slash: { aliases: ["key", "kbd", "keyboard"] },
    label: "Key (MyST)",
    title: "Keyboard key ({kbd} role)",
    icon: "kbd",
    group: "myst",
    modes: ["myst"],
    scopes: ["block", "cell"]
  }
};
var PALETTE_ACTION_IDS = Object.keys(PALETTE_ACTIONS);
export {
  ADMONITION_TYPES,
  ALERT_TYPES,
  COLUMN_ALIGNMENTS,
  PALETTE_ACTIONS,
  PALETTE_ACTION_IDS
};
