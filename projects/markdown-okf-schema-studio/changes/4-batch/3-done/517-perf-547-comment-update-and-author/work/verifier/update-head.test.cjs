"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// test/page/modules/commentThreadsUpdate.test.ts
var assert = __toESM(require("node:assert/strict"));
var import_node_test = require("node:test");

// src/page/features/hostHandlers.ts
function registerHostHandlers(rt) {
  const { hostMessages, host, context, state, bus } = rt;
  const parts = rt.parts;
  hostMessages.on("previewEditorWatch", (message) => {
    if (state.activeBlockEdit && state.activeBlockEdit.editId === message.editId) state.activeBlockEdit.reportClose = true;
    else rt.blockEditor.postEditClosed(message.editId);
  });
  hostMessages.on("previewContentPatch", (message) => {
    rt.contentPatch.applyContentPatch(message);
  });
  hostMessages.on("previewPropertiesTable", (message) => {
    if (state.activeFrontmatterEdit) {
      rt.diagnostics.editorTrace.record("properties table deferred", "seq " + message.seq);
      state.deferredPropertiesMarkup = message.markup;
      state.deferredPropertiesSeq = message.seq;
      return;
    }
    rt.frontmatter.applyPropertiesMarkup(message.markup, message.seq);
  });
  hostMessages.on("previewEditCommand", (message) => rt.textControls.runEditCommand(message.command));
  hostMessages.on("previewFoldCommand", (message) => {
    if (message.command === "foldAll") parts.headingFold.foldAll();
    else parts.headingFold.unfoldAll();
  });
  hostMessages.on("previewFindCommand", () => parts.find.open());
  hostMessages.on("previewSaveCommand", () => rt.blockEditor.saveDocumentFromKey());
  hostMessages.on("previewExportCommand", () => parts.exportHtml.run(false));
  hostMessages.on("previewShowComments", (message) => {
    parts.chipToggle.setShowComments(message.showComments !== false);
    parts.commentThreads.visibilityChanged();
  });
  hostMessages.on("previewCommentResult", (message) => {
    if (!parts.commentCompose?.result(message)) parts.commentThreads.result(message);
  });
  hostMessages.on("previewComments", (message) => {
    if (parts.commentThreads.setThreads(message.threads)) rt.scroll.measure();
  });
  hostMessages.on("previewIncomingChanges", (message) => {
    parts.incomingChanges.setEnabled(message.enabled !== false);
    parts.incomingChanges.setRanges(message.ranges, message.removed);
  });
  hostMessages.on("previewBaselineDiff", (message) => {
    parts.sideBySide.setBaseline({ html: message.html, hunks: message.hunks, revision: message.revision });
  });
  hostMessages.on("previewFlushEdit", (message) => {
    const flushId = message.flushId;
    rt.blockEditor.flushOpenEditorsThen((flushed) => host.postMessage({
      type: "previewEditFlushed",
      documentId: context.documentId,
      revision: context.revision,
      requestId: context.requestId,
      flushId,
      flushed
    }));
  });
  hostMessages.on("previewHistoryState", (message) => {
    parts.historyControls.apply(message);
  });
  hostMessages.on("navigateAnchor", (message) => {
    rt.scroll.navigateToAnchor(message);
  });
  hostMessages.on("previewLabelRenameResult", (message) => parts.labelRename.receive(message));
  hostMessages.on("previewLinkTargets", (message) => {
    parts.linkNavigation.applyTargets(message);
  });
  hostMessages.on("previewPlantUmlIncludeResult", (message) => parts.plantUmlFileRequests.receive(message));
  hostMessages.on("previewPlantUmlIncludesChanged", () => bus.emit("plantUmlIncludesChanged", void 0));
  hostMessages.on("previewBlocksResult", (message) => {
    rt.selection.receiveBlocksResult(message);
  });
  hostMessages.on("previewBlockMoveResult", (message) => {
    rt.blockMoves.receiveBlockMoveResult(message);
  });
  hostMessages.on("previewEditSource", (message) => {
    rt.blockSourceEditor.receiveBlockEditSource(message);
  });
  hostMessages.on("previewFrontmatterResult", (message) => {
    rt.frontmatter.receiveFrontmatterResult(message);
  });
  hostMessages.on("previewRevealLine", (message) => rt.lineMarker.reveal(message.line, message.scroll ?? "reading-line"));
  hostMessages.on("previewLineMarkerClear", () => rt.lineMarker.clear());
  hostMessages.on("sourceScroll", (message) => {
    rt.scroll.followSourceScroll(message);
  });
}

// src/page/modules/commentThreadData.ts
var MAX_TEXT = 1e4;
var MAX_THREADS = 1e3;
var MAX_COMMENTS = 200;
var text = (value) => typeof value === "string" ? value.slice(0, MAX_TEXT) : "";
var sanitize = (value) => {
  if (!Array.isArray(value)) return [];
  const result = [];
  for (const raw of value.slice(0, MAX_THREADS)) {
    if (!raw || typeof raw !== "object" || typeof raw.id !== "string" || raw.id === "") continue;
    const anchor = raw.anchor;
    if (!anchor || !Number.isSafeInteger(anchor.line) || anchor.line < 1) continue;
    if (!Array.isArray(raw.comments)) continue;
    const comments = [];
    for (const comment of raw.comments.slice(0, MAX_COMMENTS)) {
      if (!comment || typeof comment !== "object") continue;
      comments.push({
        id: text(comment.id),
        author: text(comment.author),
        createdAt: text(comment.createdAt),
        body: text(comment.body)
      });
    }
    result.push({
      id: text(raw.id),
      anchor: {
        line: anchor.line,
        endLine: Number.isSafeInteger(anchor.endLine) && anchor.endLine >= anchor.line ? anchor.endLine : anchor.line,
        quote: text(anchor.quote),
        prefix: text(anchor.prefix),
        suffix: text(anchor.suffix)
      },
      resolved: raw.resolved === true,
      createdAt: text(raw.createdAt),
      comments,
      ...typeof raw.orphaned === "boolean" ? { orphaned: raw.orphaned } : {}
    });
  }
  return result;
};
var locate = (value, variant, from) => {
  const words = variant.split(/\s+/u).filter((word) => word !== "");
  const source = words.map((word) => word.replace(/[\\^$.*+?()[\]{}|]/gu, "\\$&")).join("\\s+");
  const pattern = new RegExp(source, "gu");
  pattern.lastIndex = from;
  const match = words.length > 0 ? pattern.exec(value) : null;
  return match ? { index: match.index, length: match[0].length } : void 0;
};

// src/page/modules/commentEditorBehaviour.ts
var DISCARD = "data-okf-comment-discard";
var DISCARD_YES = "data-okf-comment-discard-yes";
var DISCARD_KEEP = "data-okf-comment-discard-keep";
var GAP = 6;
var EDGE = 8;
function floatingTop(editor, anchor, viewportHeight) {
  const height = editor.getBoundingClientRect?.().height ?? 0;
  const below = anchor.bottom + GAP;
  if (anchor.bottom < 0 || anchor.top > viewportHeight) return below;
  if (below + height <= viewportHeight - EDGE) return below;
  const above = anchor.top - GAP - height;
  if (above >= EDGE) return above;
  return Math.max(EDGE, viewportHeight - height - EDGE);
}
function discardQuestion(document, label) {
  const row = document.createElement("div");
  row.setAttribute(DISCARD, "true");
  row.setAttribute("role", "group");
  row.setAttribute("aria-label", label);
  const ask = document.createElement("span");
  ask.textContent = label;
  row.appendChild(ask);
  for (const [attribute, text2] of [[DISCARD_YES, "Discard"], [DISCARD_KEEP, "Keep editing"]]) {
    const button = document.createElement("button");
    button.setAttribute("type", "button");
    button.setAttribute(attribute, "true");
    button.textContent = text2;
    row.appendChild(button);
  }
  return row;
}

// src/page/modules/commentPlan.ts
var MARK = "data-okf-comment-thread";
var BADGE = "data-okf-comment-badge";
var ORPHAN = "data-okf-comment-orphan";
var POPOVER = "data-okf-comment-popover";
var SKIP = `pre, code, script, style, textarea, svg, .katex, .math, .math-inline, .math-display, .myst-mermaid-figure, .myst-plantuml-figure, .myst-vega-figure, [data-okf-properties], .okf-comment, .okf-chip, [data-sphinx-preview-block-editor], [data-sphinx-preview-editing], [data-sphinx-preview-included], [${MARK}], [${BADGE}], [${POPOVER}]`;
var EDITING = "[data-sphinx-preview-block-editor], [data-sphinx-preview-editing]";
var NEXT_TO = /* @__PURE__ */ new Set(["TABLE", "THEAD", "TBODY", "TR", "UL", "OL", "DL", "PRE", "DETAILS", "IMG", "HR", "SVG"]);
var MIN_MOVED_QUOTE = 12;
var spanOf = (element) => {
  const start = Number(element.getAttribute("data-line"));
  if (!Number.isFinite(start)) return void 0;
  const endValue = Number(element.getAttribute("data-end-line"));
  return [start, Number.isFinite(endValue) && endValue >= start ? endValue : start];
};
var eligible = (element) => {
  if (element.closest(EDITING) || element.closest("[data-okf-properties]")) return false;
  if (element.closest("[data-sphinx-preview-included]")) return false;
  const container = element.parentNode;
  return !(container && container.nodeType === 1 && container.closest(SKIP));
};
var readBlocks = (document) => {
  const blocks = [];
  document.querySelectorAll("[data-line]").forEach((element) => {
    if (eligible(element)) blocks.push({ element, span: spanOf(element) });
  });
  return blocks;
};
var runOf = (members) => {
  const offsets = /* @__PURE__ */ new Map();
  let text2 = "";
  for (const node of members) {
    offsets.set(node, text2.length);
    text2 += node.textContent ?? "";
  }
  return { head: members[0], text: text2, offsets, free: text2 === "" ? [] : [[0, text2.length]] };
};
function planThreads(document, threads, marks) {
  let read;
  const blocks = () => read ??= readBlocks(document);
  const blockFor = (line) => {
    let best;
    let bestSize = Infinity;
    for (const { element, span } of blocks()) {
      if (!span || line < span[0] || line > span[1]) continue;
      const size = span[1] - span[0];
      if (size <= bestSize) {
        best = element;
        bestSize = size;
      }
    }
    return best;
  };
  const known = /* @__PURE__ */ new Map();
  const walked = /* @__PURE__ */ new Map();
  const runsOf = (block) => {
    const cached = walked.get(block);
    if (cached) return cached;
    const found = [];
    const walk = (node) => {
      let members = [];
      const end = () => {
        if (members.length === 0) return;
        const run = known.get(members[0]) ?? runOf(members);
        known.set(run.head, run);
        found.push(run);
        members = [];
      };
      for (let child = node.firstChild; child; child = child.nextSibling) {
        const mark = marks.has(child);
        if (mark || child.nodeType === 3) {
          const last = members[members.length - 1];
          if (last && !mark && !marks.has(last)) end();
          members.push(child);
        } else {
          end();
          if (child.nodeType === 1 && !child.matches(SKIP)) walk(child);
        }
      }
      end();
    };
    if (!block.matches(SKIP)) walk(block);
    walked.set(block, found);
    return found;
  };
  const highlight = (thread2) => {
    const quote = thread2.anchor.quote;
    if (quote === "") return void 0;
    const block = blockFor(thread2.anchor.line);
    if (!block && thread2.orphaned === false) return void 0;
    const searched = block ? [block] : blocks().map((candidate) => candidate.element);
    const runs = new Set(searched.flatMap(runsOf));
    const variants = [quote];
    const collapsed = quote.replace(/\s+/gu, " ");
    if (collapsed !== quote) variants.push(collapsed);
    if (!block) {
      if (collapsed.trim().length < MIN_MOVED_QUOTE) return void 0;
      let total = 0;
      for (const run of runs) {
        for (const [from, to] of run.free) {
          const value = run.text.slice(from, to);
          for (const variant of variants) {
            let found = locate(value, variant, 0);
            if (!found) continue;
            while (found) {
              total += 1;
              found = locate(value, variant, found.index + found.length);
            }
            break;
          }
        }
      }
      if (total !== 1) return void 0;
    }
    for (const run of runs) {
      for (const [index, [from, to]] of run.free.entries()) {
        const value = run.text.slice(from, to);
        for (const variant of variants) {
          const found = locate(value, variant, 0);
          if (!found) continue;
          const offset = from + found.index;
          const rest = [[from, offset], [offset + found.length, to]];
          run.free.splice(index, 1, ...rest.filter(([start, end]) => end > start));
          return { kind: "mark", run, offset, length: found.length };
        }
      }
    }
    return void 0;
  };
  const badge = (thread2) => {
    const block = blockFor(thread2.anchor.line);
    if (!block) return void 0;
    return { kind: "badge", block, after: block.matches(SKIP) || NEXT_TO.has(block.tagName.toUpperCase()) };
  };
  return threads.map((thread2) => (thread2.orphaned === true ? void 0 : highlight(thread2) ?? badge(thread2)) ?? { kind: "orphan" });
}

// src/page/modules/commentPlacements.ts
var BADGED = "data-okf-comment-badged";
var AFTER = "data-okf-comment-badge-after";
var RESOLVED = "data-okf-comment-resolved";
var byThread = (elements, attribute) => new Map(elements.map((element) => [element.getAttribute(attribute), element]));
var take = (from, id) => {
  const found = from.get(id);
  from.delete(id);
  return found;
};
var paintResolved = (element, resolved) => {
  const shown = element.getAttribute(RESOLVED) !== null;
  if (resolved && !shown) element.setAttribute(RESOLVED, "true");
  else if (!resolved && shown) element.removeAttribute(RESOLVED);
};
var paintAttribute = (element, name, value) => {
  if (element.getAttribute(name) !== value) element.setAttribute(name, value);
};
var paintText = (element, value) => {
  if (element.textContent !== value) element.textContent = value;
};
var holdsElement = (block) => Array.from(block.childNodes).some((child) => child.nodeType === 1 && !child.hasAttribute(BADGE));
var sitsAt = (mark, place) => place.run.offsets.get(mark) === place.offset && (mark.textContent ?? "").length === place.length && mark.firstChild?.nodeType === 3 && !mark.firstChild.nextSibling;
function createCommentPlacements(document, paintMark) {
  let marks = [];
  let badges = [];
  let badgedBlocks = /* @__PURE__ */ new Set();
  let orphans;
  const unwrap = (mark) => {
    const parent = mark.parentNode;
    if (!parent) return void 0;
    let merged = document.createTextNode(mark.textContent ?? "");
    parent.replaceChild(merged, mark);
    const before = merged.previousSibling;
    if (before && before.nodeType === 3) {
      before.nodeValue = (before.nodeValue ?? "") + (merged.nodeValue ?? "");
      parent.removeChild(merged);
      merged = before;
    }
    const after = merged.nextSibling;
    if (after && after.nodeType === 3) {
      merged.nodeValue = (merged.nodeValue ?? "") + (after.nodeValue ?? "");
      parent.removeChild(after);
    }
    return merged;
  };
  const wrap = (place, id) => {
    let node = place.run.head;
    let start = 0;
    while (start + (node.textContent ?? "").length <= place.offset) {
      start += (node.textContent ?? "").length;
      node = node.nextSibling;
    }
    const value = node.nodeValue ?? "";
    const index = place.offset - start;
    const parent = node.parentNode;
    const mark = document.createElement("mark");
    mark.setAttribute(MARK, id);
    mark.textContent = value.slice(index, index + place.length);
    if (index === 0) {
      parent.replaceChild(mark, node);
    } else {
      node.nodeValue = value.slice(0, index);
      parent.insertBefore(mark, node.nextSibling);
    }
    const rest = value.slice(index + place.length);
    if (rest !== "") parent.insertBefore(document.createTextNode(rest), mark.nextSibling);
    return mark;
  };
  const updateMarks = (threads, places) => {
    const before = byThread(marks, MARK);
    const heads = /* @__PURE__ */ new Map();
    const wanted = places.flatMap((place, index) => {
      if (place.kind !== "mark") return [];
      heads.set(place.run.head, place.run);
      const thread2 = threads[index];
      const old = before.get(thread2.id);
      return [{ place, thread: thread2, mark: old && sitsAt(old, place) ? take(before, thread2.id) : void 0 }];
    });
    const kept = new Set(wanted.map((entry) => entry.mark));
    let changed = false;
    for (const mark of marks) {
      if (kept.has(mark)) continue;
      changed = true;
      const text2 = unwrap(mark);
      const run = heads.get(mark);
      if (run && text2) run.head = text2;
    }
    for (const entry of [...wanted].sort((a, b) => b.place.offset - a.place.offset)) {
      if (entry.mark) continue;
      changed = true;
      entry.mark = wrap(entry.place, entry.thread.id);
    }
    marks = wanted.map(({ mark, thread: thread2 }) => {
      paintResolved(mark, thread2.resolved);
      paintMark(mark);
      return mark;
    });
    return changed;
  };
  const newBadge = (id, after) => {
    const button = document.createElement("button");
    button.setAttribute("type", "button");
    button.setAttribute(BADGE, id);
    button.setAttribute("aria-haspopup", "dialog");
    if (after) button.setAttribute(AFTER, "true");
    return button;
  };
  const updateBadges = (threads, places) => {
    const before = byThread(badges, BADGE);
    const below = /* @__PURE__ */ new Map();
    const inside = /* @__PURE__ */ new Map();
    const next = [];
    places.forEach((place, index) => {
      if (place.kind !== "badge") return;
      const thread2 = threads[index];
      const old = take(before, thread2.id);
      const button = old && old.getAttribute(AFTER) !== null === place.after ? old : newBadge(thread2.id, place.after);
      paintResolved(button, thread2.resolved);
      const count = thread2.comments.length;
      paintAttribute(button, "aria-label", `Comment thread, ${count} comment${count === 1 ? "" : "s"}`);
      const side = place.after ? below : inside;
      side.set(place.block, [...side.get(place.block) ?? [], button]);
      next.push(button);
    });
    let moved = false;
    const kept = new Set(next);
    const badgedNow = new Set(badges.flatMap((button) => button.getAttribute(AFTER) === null && button.parentNode ? [button.parentNode] : []));
    for (const old of badges) {
      if (kept.has(old)) continue;
      if (old.getAttribute(AFTER) !== null) moved = true;
      old.remove();
    }
    badges = next;
    for (const [block, buttons] of below) {
      const parent = block.parentNode;
      if (!parent) continue;
      let previous = block;
      for (const button of [...buttons].reverse()) {
        if (button.parentNode !== parent || previous.nextSibling !== button) {
          parent.insertBefore(button, previous.nextSibling);
          moved = true;
        }
        previous = button;
      }
    }
    for (const [block, buttons] of inside) {
      paintAttribute(block, BADGED, "true");
      let following = null;
      for (const button of [...buttons].reverse()) {
        if (button.parentNode !== block || button.nextSibling !== following) block.insertBefore(button, following);
        following = button;
      }
    }
    for (const block of badgedBlocks) if (!inside.has(block)) block.removeAttribute(BADGED);
    badgedBlocks = new Set(inside.keys());
    for (const block of /* @__PURE__ */ new Set([...badgedNow, ...inside.keys()])) {
      if (badgedNow.has(block) !== inside.has(block) && holdsElement(block)) moved = true;
    }
    return moved;
  };
  const newEntry = (id) => {
    const element = document.createElement("button");
    element.setAttribute("type", "button");
    element.setAttribute(ORPHAN, id);
    element.setAttribute("aria-haspopup", "dialog");
    const quote = document.createElement("span");
    quote.setAttribute("data-okf-orphan-quote", "true");
    const meta = document.createElement("span");
    meta.setAttribute("data-okf-orphan-meta", "true");
    element.appendChild(quote);
    element.appendChild(meta);
    return { element, quote, meta };
  };
  const newBox = () => {
    const box = document.createElement("div");
    box.setAttribute("data-okf-orphans", "true");
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Orphaned comments");
    const title = document.createElement("div");
    title.setAttribute("data-okf-orphans-title", "true");
    title.textContent = "Orphaned comments";
    box.appendChild(title);
    return { box, title, entries: [] };
  };
  const updateOrphans = (listed) => {
    if (listed.length === 0) {
      orphans?.box.remove();
      orphans = void 0;
      return;
    }
    orphans ??= newBox();
    const { box, title } = orphans;
    const before = new Map(
      orphans.entries.map((entry) => [entry.element.getAttribute(ORPHAN), entry])
    );
    const entries = listed.map((thread2) => {
      const entry = take(before, thread2.id) ?? newEntry(thread2.id);
      paintResolved(entry.element, thread2.resolved);
      paintText(entry.quote, thread2.anchor.quote !== "" ? thread2.anchor.quote : "(no quoted text)");
      const first = thread2.comments[0];
      const count = thread2.comments.length;
      paintText(entry.meta, `${first ? first.author + ": " + first.body.slice(0, 120) : ""} (${count} comment${count === 1 ? "" : "s"}${thread2.resolved ? ", resolved" : ""})`);
      return entry;
    });
    const kept = new Set(entries);
    for (const old of orphans.entries) if (!kept.has(old)) old.element.remove();
    orphans.entries = entries;
    let previous = title;
    for (const { element } of entries) {
      if (element.parentNode !== box || previous.nextSibling !== element) box.insertBefore(element, previous.nextSibling);
      previous = element;
    }
    const main = document.getElementById?.("sphinx-myst-preview-content");
    const parent = main?.parentNode ?? document.body;
    if (box.parentNode !== parent || (main ? main.nextSibling !== box : box.nextSibling !== null)) {
      parent.insertBefore(box, main ? main.nextSibling : null);
    }
  };
  return {
    // @implements_req SwRS-MDOKFSTUDIO-REVIEW-224
    update(threads) {
      const places = planThreads(document, threads, new Set(marks));
      const marked = updateMarks(threads, places);
      const badged = updateBadges(threads, places);
      updateOrphans(threads.filter((_thread, index) => places[index].kind === "orphan"));
      return marked || badged;
    },
    marks: () => marks,
    holders: () => [...marks, ...badges, ...orphans?.entries.map((entry) => entry.element) ?? []]
  };
}

// src/page/modules/commentThreads.ts
function installCommentThreads(document, window, hooks, trace) {
  const REPLY_INPUT = "data-okf-comment-reply-input";
  const REPLY_SEND = "data-okf-comment-reply-send";
  const ACTIONS = "data-okf-comment-thread-actions";
  const ACTION_ERROR = "data-okf-comment-action-error";
  let threads = [];
  let popover;
  let openId;
  const ANSWER_TIMEOUT_MS = 15e3;
  let sent;
  let act;
  let confirming;
  let discarding;
  let openTarget;
  const hidden = () => {
    const root = document.documentElement;
    return root?.getAttribute("data-sphinx-preview-comments") === "off" || root?.getAttribute("data-okf-show-comments") === "false";
  };
  const paintFocus = (mark) => {
    const shown = !hidden();
    for (const [name, value] of [["tabindex", "0"], ["role", "button"], ["aria-haspopup", "dialog"]]) {
      if (!shown) mark.removeAttribute(name);
      else if (mark.getAttribute(name) !== value) mark.setAttribute(name, value);
    }
  };
  const placements = createCommentPlacements(document, paintFocus);
  const replyInput = () => popover?.querySelector(`[${REPLY_INPUT}]`) ?? void 0;
  const paintReply = () => {
    paintReplyContent();
    if (popover && openTarget) position(openTarget);
  };
  const paintReplyContent = () => {
    if (!popover) return;
    paintActions();
    paintDiscard(false);
    const reply = popover.querySelector("[data-okf-comment-reply]");
    const send = popover.querySelector(`[${REPLY_SEND}]`);
    if (!reply || !send) return;
    const mine = sent !== void 0 && sent.threadId === openId;
    if (pendingFor(openId)) send.setAttribute("disabled", "true");
    else send.removeAttribute("disabled");
    let line = popover.querySelector("[data-okf-comment-error]");
    const text2 = mine ? sent.error : "";
    if (text2 === "") {
      line?.remove();
      return;
    }
    if (!line) {
      line = document.createElement("div");
      line.setAttribute("data-okf-comment-error", "true");
      line.setAttribute("role", "alert");
      reply.insertBefore(line, send);
    }
    line.textContent = text2;
  };
  const pendingFor = (threadId) => act !== void 0 && act.threadId === threadId && act.timer !== void 0 || sent !== void 0 && sent.threadId === threadId && sent.timer !== void 0;
  const actionButton = (label, attribute, disabled) => {
    const element = document.createElement("button");
    element.setAttribute("type", "button");
    element.setAttribute(attribute, "true");
    element.textContent = label;
    if (disabled) element.setAttribute("disabled", "true");
    return element;
  };
  const paintActions = () => {
    if (!popover) return;
    const row = popover.querySelector(`[${ACTIONS}]`);
    if (!row) return;
    const thread2 = threads.find((candidate) => candidate.id === openId);
    row.textContent = "";
    const busy = pendingFor(openId);
    if (confirming !== void 0 && confirming === openId) {
      const ask = document.createElement("span");
      ask.setAttribute("data-okf-comment-confirm", "true");
      ask.textContent = "Delete thread?";
      row.appendChild(ask);
      row.appendChild(actionButton("Yes", "data-okf-comment-delete-yes", busy));
      row.appendChild(actionButton("No", "data-okf-comment-delete-no", busy));
    } else {
      if (hooks?.resolve) {
        row.appendChild(actionButton(thread2?.resolved ? "Reopen" : "Resolve", "data-okf-comment-resolve", busy));
      }
      if (hooks?.remove) row.appendChild(actionButton("Delete", "data-okf-comment-delete", busy));
    }
    const message = act !== void 0 && act.threadId === openId ? act.error : "";
    if (message !== "") {
      const line = document.createElement("div");
      line.setAttribute(ACTION_ERROR, "true");
      line.setAttribute("role", "alert");
      line.textContent = message;
      row.appendChild(line);
    }
    if (openTarget) position(openTarget);
  };
  const startAction = (kind, send) => {
    const threadId = openId;
    if (threadId === void 0 || pendingFor(threadId)) return;
    if (act?.timer !== void 0) window.clearTimeout(act.timer);
    const mine = {
      threadId,
      kind,
      waiting: true,
      error: "",
      timer: window.setTimeout(() => {
        if (act !== mine) return;
        mine.timer = void 0;
        confirming = void 0;
        mine.error = "No answer from the editor. Nothing changed here: try again.";
        paintReply();
      }, ANSWER_TIMEOUT_MS)
    };
    act = mine;
    paintReply();
    send(threadId);
  };
  const close = (why) => {
    if (why !== void 0 && popover) trace?.("comment popover closed", `${why}, thread ${openId ?? "none"}`);
    popover?.remove();
    popover = void 0;
    openId = void 0;
    confirming = void 0;
    discarding = void 0;
    openTarget = void 0;
  };
  const paintDiscard = (focusKeep) => {
    if (!popover) return;
    const shown = popover.querySelector(`[${DISCARD}]`);
    const wanted = discarding !== void 0 && discarding === openId;
    if (shown && wanted) return;
    shown?.remove();
    if (!wanted) return;
    const row = discardQuestion(document, "Discard this reply?");
    popover.appendChild(row);
    if (focusKeep) row.querySelector(`[${DISCARD_KEEP}]`)?.focus?.();
  };
  const keepEditing = () => {
    discarding = void 0;
    paintDiscard(false);
    if (openTarget) position(openTarget);
    replyInput()?.focus?.();
  };
  const draftChanged = () => {
    const field = replyInput();
    return popover !== void 0 && typeof field?.value === "string" && field.value.trim() !== "";
  };
  const closeOrAsk = (why) => {
    if (!draftChanged()) {
      close(why);
      return true;
    }
    discarding = openId;
    paintDiscard(true);
    if (openTarget) position(openTarget);
    return false;
  };
  const place = (afresh) => {
    const reopen = hidden() ? void 0 : openId;
    const draft = replyInput()?.value;
    const asking = confirming;
    const discardAsked = discarding;
    close();
    if (afresh) placements.update([]);
    const moved = placements.update(threads);
    if (reopen === void 0) return moved;
    if (threads.length === 0) {
      trace?.("comment popover closed", `re-apply without threads, thread ${reopen}`);
      return moved;
    }
    const holder = placements.holders().find((candidate) => idOf(candidate) === reopen);
    const thread2 = threads.find((candidate) => candidate.id === reopen);
    if (holder && thread2) {
      open(thread2, holder);
      const input = replyInput();
      if (input && typeof draft === "string") input.value = draft;
      confirming = asking === reopen ? asking : void 0;
      discarding = discardAsked === reopen ? discardAsked : void 0;
      paintReply();
      paintActions();
    } else {
      trace?.("comment popover closed", `re-apply without ${thread2 ? "a holder" : "the thread"}, thread ${reopen}, ${threads.length} thread(s)`);
    }
    return moved;
  };
  const formatDate = (iso) => {
    const time = Date.parse(iso);
    if (Number.isNaN(time)) return iso;
    try {
      return new Date(time).toLocaleString();
    } catch {
      return iso;
    }
  };
  const position = (target) => {
    if (!popover) return;
    openTarget = target;
    const rectangle = target.getBoundingClientRect();
    const width = Math.min(360, Math.max(200, (window.innerWidth || 800) - 16));
    const left = Math.max(8, Math.min(rectangle.left, (window.innerWidth || 800) - width - 8));
    const top = floatingTop(popover, rectangle, window.innerHeight || 600);
    popover.style.setProperty("width", `${width}px`);
    popover.style.setProperty("left", `${left}px`);
    popover.style.setProperty("top", `${top}px`);
  };
  const open = (thread2, target) => {
    close();
    const root = document.createElement("div");
    root.setAttribute(POPOVER, thread2.id);
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-label", "Comment thread");
    if (thread2.resolved) root.setAttribute("data-okf-comment-resolved", "true");
    if (thread2.resolved) {
      const state = document.createElement("div");
      state.setAttribute("data-okf-comment-state", "resolved");
      state.textContent = "Resolved";
      root.appendChild(state);
    }
    for (const comment of thread2.comments) {
      const item = document.createElement("div");
      item.setAttribute("data-okf-comment-entry", "true");
      const head = document.createElement("div");
      head.setAttribute("data-okf-comment-head", "true");
      const author = document.createElement("strong");
      author.textContent = comment.author;
      const date = document.createElement("span");
      date.textContent = formatDate(comment.createdAt);
      head.appendChild(author);
      head.appendChild(date);
      const body = document.createElement("div");
      body.setAttribute("data-okf-comment-body", "true");
      body.textContent = comment.body;
      item.appendChild(head);
      item.appendChild(body);
      root.appendChild(item);
    }
    if (hooks && (typeof hooks.resolve === "function" || typeof hooks.remove === "function")) {
      const row = document.createElement("div");
      row.setAttribute(ACTIONS, "true");
      root.appendChild(row);
    }
    if (hooks && typeof hooks.reply === "function") {
      const reply = document.createElement("div");
      reply.setAttribute("data-okf-comment-reply", "true");
      const input = document.createElement("textarea");
      input.setAttribute(REPLY_INPUT, "true");
      input.setAttribute("maxlength", String(MAX_TEXT));
      input.setAttribute("rows", "2");
      input.setAttribute("aria-label", "Reply to this thread");
      input.setAttribute("placeholder", "Reply");
      const send = document.createElement("button");
      send.setAttribute("type", "button");
      send.setAttribute(REPLY_SEND, "true");
      send.textContent = "Reply";
      reply.appendChild(input);
      reply.appendChild(send);
      root.appendChild(reply);
    }
    document.body.appendChild(root);
    popover = root;
    openId = thread2.id;
    position(target);
    paintReply();
  };
  const holderOf = (target) => target.closest(`[${MARK}], [${BADGE}], [${ORPHAN}]`);
  const idOf = (holder) => holder.getAttribute(MARK) ?? holder.getAttribute(BADGE) ?? holder.getAttribute(ORPHAN);
  const toggle = (holder) => {
    const id = idOf(holder);
    const thread2 = threads.find((candidate) => candidate.id === id);
    if (!thread2) return false;
    if (openId === thread2.id) closeOrAsk("toggled");
    else if (draftChanged()) closeOrAsk("switched");
    else open(thread2, holder);
    return true;
  };
  const intercept = (event) => {
    const target = event.target;
    const holder = target instanceof Element ? holderOf(target) : null;
    if (!holder || hidden()) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    if (event.type === "click") toggle(holder);
  };
  const sendReply = (input) => {
    const field = input;
    const body = typeof field.value === "string" ? field.value.trim() : "";
    if (body === "" || body.length > MAX_TEXT || openId === void 0 || !hooks?.reply) return;
    if (pendingFor(openId)) return;
    const threadId = openId;
    sent = {
      threadId,
      body,
      waiting: true,
      error: "",
      timer: window.setTimeout(() => {
        if (!sent || sent.threadId !== threadId) return;
        sent.timer = void 0;
        sent.error = "No answer from the editor. Your text is kept: try Reply again.";
        paintReply();
      }, ANSWER_TIMEOUT_MS)
    };
    paintReply();
    hooks.reply(threadId, body);
  };
  document.addEventListener("click", (event) => {
    const target = event.target;
    const send = target instanceof Element ? target.closest(`[${REPLY_SEND}]`) : null;
    if (!send) return;
    event.preventDefault();
    const input = popover?.querySelector(`[${REPLY_INPUT}]`);
    if (input) sendReply(input);
  }, true);
  document.addEventListener("click", (event) => {
    const target = event.target;
    const hit = (attribute) => target instanceof Element && target.closest(`[${attribute}]`) !== null;
    const resolveHook = hooks?.resolve;
    const removeHook = hooks?.remove;
    if (hit("data-okf-comment-resolve") && resolveHook) {
      event.preventDefault();
      const thread2 = threads.find((candidate) => candidate.id === openId);
      if (thread2) startAction("resolve", (threadId) => resolveHook(threadId, !thread2.resolved));
    } else if (hit("data-okf-comment-delete") && removeHook) {
      event.preventDefault();
      if (openId !== void 0 && !pendingFor(openId)) {
        confirming = openId;
        if (act !== void 0 && act.threadId === openId) act.error = "";
        paintActions();
      }
    } else if (hit("data-okf-comment-delete-no")) {
      event.preventDefault();
      if (!pendingFor(openId)) {
        confirming = void 0;
        paintActions();
      }
    } else if (hit("data-okf-comment-delete-yes") && removeHook) {
      event.preventDefault();
      if (confirming === openId) startAction("delete", (threadId) => removeHook(threadId));
    } else if (popover && target instanceof Element && hit(DISCARD_YES) && target.closest(`[${POPOVER}]`)) {
      event.preventDefault();
      close("discarded");
    } else if (popover && target instanceof Element && hit(DISCARD_KEEP) && target.closest(`[${POPOVER}]`)) {
      event.preventDefault();
      keepEditing();
    }
  }, true);
  document.addEventListener("click", intercept, true);
  document.addEventListener("dblclick", intercept, true);
  document.addEventListener("keydown", (event) => {
    const target = event.target;
    if (event.key === "Escape") {
      if (!popover) return;
      if (discarding !== void 0) {
        keepEditing();
      } else {
        closeOrAsk("Escape");
      }
      event.stopImmediatePropagation();
      return;
    }
    const field = target instanceof Element ? target.closest(`[${REPLY_INPUT}]`) : null;
    if (field) {
      if (event.key === "Enter" && (event.metaKey || event.ctrlKey) && !event.isComposing) {
        event.preventDefault();
        sendReply(field);
      }
      event.stopImmediatePropagation();
      return;
    }
    const holder = target instanceof Element ? holderOf(target) : null;
    if (event.key !== "Enter" && event.key !== " " || !holder || hidden()) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    toggle(holder);
  }, true);
  const pressOutside = (event) => {
    const target = event.target;
    if (!popover || discarding !== void 0) return;
    if (target instanceof Element && (target.closest(`[${POPOVER}]`) || holderOf(target))) return;
    closeOrAsk(`pointerdown outside on ${target instanceof Element ? target.tagName.toLowerCase() : "no element"}`);
  };
  document.addEventListener("pointerdown", pressOutside, true);
  document.addEventListener("mousedown", pressOutside, true);
  document.addEventListener("scroll", () => {
    if (openTarget) position(openTarget);
  }, { capture: true, passive: true });
  return {
    result(message) {
      if ((message.kind === "resolve" || message.kind === "delete") && act !== void 0) {
        if (!act.waiting || act.kind !== message.kind || message.threadId !== act.threadId) return false;
        if (act.timer !== void 0) window.clearTimeout(act.timer);
        act.timer = void 0;
        act.waiting = false;
        if (message.ok === true) {
          act = void 0;
        } else {
          act.error = typeof message.reason === "string" && message.reason !== "" ? message.reason.slice(0, 500) : "The change was not saved.";
        }
        confirming = void 0;
        paintReply();
        return true;
      }
      if (message.kind !== "reply" || !sent || !sent.waiting || message.threadId !== sent.threadId) return false;
      if (sent.timer !== void 0) window.clearTimeout(sent.timer);
      sent.timer = void 0;
      sent.waiting = false;
      if (message.ok === true) {
        const answered = sent;
        sent = void 0;
        const input = replyInput();
        if (input && openId === answered.threadId && input.value.trim() === answered.body) input.value = "";
      } else {
        sent.error = typeof message.reason === "string" && message.reason !== "" ? message.reason.slice(0, 500) : "The reply was not saved.";
      }
      paintReply();
      return true;
    },
    setThreads(next) {
      threads = sanitize(next);
      return place(false);
    },
    apply: () => {
      place(true);
    },
    close: () => close("closed by the page"),
    // @implements_req SwRS-MDOKFSTUDIO-REVIEW-152
    visibilityChanged() {
      if (hidden()) close("comments hidden");
      placements.marks().forEach(paintFocus);
    },
    openThread(id) {
      if (hidden()) return false;
      const holder = Array.from(document.querySelectorAll(`[${MARK}], [${BADGE}], [${ORPHAN}]`)).find((candidate) => idOf(candidate) === id);
      return holder ? toggle(holder) : false;
    }
  };
}

// test/page/modules/fakeDom.ts
var FakeNode = class {
  parentNode = null;
  get nodeType() {
    return this instanceof FakeElement ? 1 : 3;
  }
  get previousSibling() {
    const list = this.parentNode?.childNodes ?? [];
    return list[list.indexOf(this) - 1] ?? null;
  }
  get nextSibling() {
    const list = this.parentNode?.childNodes ?? [];
    return list[list.indexOf(this) + 1] ?? null;
  }
  remove() {
    this.parentNode?.removeChild(this);
  }
};
var FakeText = class extends FakeNode {
  constructor(nodeValue) {
    super();
    this.nodeValue = nodeValue;
  }
  nodeValue;
  get textContent() {
    return this.nodeValue;
  }
};
var FakeElement = class _FakeElement extends FakeNode {
  constructor(tagName, attrs = {}) {
    super();
    this.tagName = tagName;
    for (const [key, value] of Object.entries(attrs)) this.attrs.set(key, value);
  }
  tagName;
  attrs = /* @__PURE__ */ new Map();
  childNodes = [];
  listeners = /* @__PURE__ */ new Map();
  styles = /* @__PURE__ */ new Map();
  get firstChild() {
    return this.childNodes[0] ?? null;
  }
  get style() {
    return { setProperty: (name, value) => this.styles.set(name, value) };
  }
  get textContent() {
    return this.childNodes.map((child) => child.textContent).join("");
  }
  set textContent(value) {
    this.childNodes.forEach((child) => {
      child.parentNode = null;
    });
    this.childNodes = [];
    if (value !== "") this.appendChild(new FakeText(value));
  }
  setAttribute(name, value) {
    this.attrs.set(name, String(value));
  }
  getAttribute(name) {
    return this.attrs.get(name) ?? null;
  }
  removeAttribute(name) {
    this.attrs.delete(name);
  }
  hasAttribute(name) {
    return this.attrs.has(name);
  }
  detach(node) {
    node.parentNode?.childNodes.splice(node.parentNode.childNodes.indexOf(node), 1);
  }
  appendChild(node) {
    return this.insertBefore(node, null);
  }
  insertBefore(node, reference) {
    this.detach(node);
    node.parentNode = this;
    const index = reference ? this.childNodes.indexOf(reference) : this.childNodes.length;
    this.childNodes.splice(index, 0, node);
    return node;
  }
  removeChild(node) {
    this.detach(node);
    node.parentNode = null;
    return node;
  }
  replaceChild(node, old) {
    this.insertBefore(node, old);
    this.removeChild(old);
    return old;
  }
  matchesToken(token) {
    if (token.startsWith(".")) return (this.attrs.get("class") ?? "").split(/\s+/u).includes(token.slice(1));
    if (token.startsWith("[")) return this.attrs.has(token.slice(1, -1));
    return this.tagName.toLowerCase() === token.toLowerCase();
  }
  matches(selector) {
    return selector.split(",").map((token) => token.trim()).some((token) => this.matchesToken(token));
  }
  closest(selector) {
    for (let node = this; node; node = node.parentNode) if (node.matches(selector)) return node;
    return null;
  }
  contains(node) {
    for (let current = node; current; current = current.parentNode) if (current === this) return true;
    return false;
  }
  descendants() {
    const found = [];
    const walk = (node) => {
      for (const child of node.childNodes) if (child instanceof _FakeElement) {
        found.push(child);
        walk(child);
      }
    };
    walk(this);
    return found;
  }
  querySelectorAll(selector) {
    return this.descendants().filter((element) => element.matches(selector));
  }
  querySelector(selector) {
    return this.querySelectorAll(selector)[0] ?? null;
  }
  getBoundingClientRect() {
    return { left: 10, top: 10, right: 50, bottom: 30, width: 40, height: 20 };
  }
  addEventListener(type, listener) {
    this.listeners.set(type, [...this.listeners.get(type) ?? [], listener]);
  }
  fire(type, event = {}) {
    const calls = { prevented: 0, stopped: 0 };
    let halted = false;
    const full = {
      type,
      target: this,
      preventDefault: () => calls.prevented++,
      stopImmediatePropagation: () => {
        calls.stopped++;
        halted = true;
      },
      ...event
    };
    for (const listener of this.ownerDocument?.listeners.get(type) ?? []) {
      if (halted) break;
      listener(full);
    }
    return calls;
  }
  ownerDocument;
};
var FakeDocument = class extends FakeElement {
  body = new FakeElement("body");
  content = new FakeElement("main");
  constructor() {
    super("html");
    this.appendChild(this.body);
    this.body.appendChild(this.content);
    this.ownerDocument = this;
  }
  createElement(tag) {
    const element = new FakeElement(tag);
    element.ownerDocument = this;
    return element;
  }
  createTextNode(text2) {
    return new FakeText(text2);
  }
  add(tag, attrs, parent = this.content, text2) {
    const element = this.createElement(tag);
    for (const [key, value] of Object.entries(attrs)) element.setAttribute(key, value);
    if (text2 !== void 0) element.appendChild(new FakeText(text2));
    parent.appendChild(element);
    return element;
  }
};
function provideGlobalElement(element) {
  globalThis.Element = element;
}

// test/page/modules/commentThreadsUpdate.test.ts
var PageDocument = class extends FakeDocument {
  constructor() {
    super();
    this.content.setAttribute("id", "sphinx-myst-preview-content");
  }
  get documentElement() {
    return this;
  }
  getElementById(id) {
    return this.querySelectorAll("[id]").find((element) => element.getAttribute("id") === id) ?? null;
  }
};
function page() {
  const document = new PageDocument();
  const first = document.add("p", { "data-line": "1" }, document.content, "alpha beta gamma delta ");
  document.add("em", {}, first, "alpha beta");
  first.appendChild(document.createTextNode(" gamma again, alpha"));
  const quote = document.add("div", { "data-line": "3", "data-end-line": "8" });
  document.add("p", { "data-line": "4" }, quote, "nested paragraph with a few words and words");
  quote.appendChild(document.createTextNode("between the paragraphs "));
  document.add("p", { "data-line": "6" }, quote, "second nested line of text here");
  const list = document.add("ul", { "data-line": "10", "data-end-line": "11" });
  document.add("li", { "data-line": "10" }, list, "list item one");
  document.add("li", { "data-line": "11" }, list, "list item two");
  const pre = document.add("pre", { "data-line": "14" });
  document.add("code", {}, pre, "alpha code");
  document.add("table", { "data-line": "16", "data-end-line": "18" });
  document.add("p", { "data-line": "20" }, document.content, "a sentence that moved somewhere unique in the text");
  const wrapper = document.add("div", { "data-line": "22", "data-end-line": "23" }, document.content, "wrapper words ");
  const inner = document.add("pre", { "data-line": "23" }, wrapper);
  document.add("code", {}, inner, "inner code");
  document.add("footer", {}, document.body, "after the content");
  provideGlobalElement(FakeElement);
  const window = { innerWidth: 800, innerHeight: 600, setTimeout: () => 1, clearTimeout: () => void 0 };
  const comments = installCommentThreads(
    document,
    window,
    { reply: () => void 0, resolve: () => void 0, remove: () => void 0 }
  );
  return { document, comments };
}
var thread = (id, line, quote, overrides = {}) => ({
  id,
  anchor: { line, endLine: line, quote, prefix: "", suffix: "" },
  resolved: false,
  createdAt: "2026-11-27T10:00:00Z",
  comments: [{ id: `${id}-1`, author: "Ada", createdAt: "2026-11-27T10:00:00Z", body: `Comment of ${id}` }],
  ...overrides
});
var POOL = [
  thread("a", 1, "alpha"),
  thread("b", 1, "alpha"),
  thread("c", 1, "beta gamma"),
  thread("d", 1, "gamma delta"),
  thread("e", 1, "alpha beta gamma delta"),
  thread("f", 1, "gamma"),
  thread("g", 4, "words"),
  thread("h", 3, "words"),
  thread("i", 3, "between the paragraphs"),
  thread("j", 6, "second nested"),
  thread("k", 3, "second nested line"),
  thread("l", 10, "list item"),
  thread("m", 11, "item two"),
  thread("n", 10, "not in the list"),
  thread("o", 1, "not in the paragraph"),
  thread("p", 1, ""),
  thread("q", 14, "alpha code"),
  thread("r", 14, "other"),
  thread("s", 16, "cell"),
  thread("t", 16, "row", { resolved: true }),
  thread("u", 99, "moved somewhere unique"),
  thread("v", 99, "words"),
  thread("w", 99, "never written anywhere", { orphaned: false }),
  thread("x", 1, "alpha", { orphaned: true }),
  thread("y", 22, "wrapper words"),
  thread("z", 22, "absent from the wrapper"),
  thread("A", 23, "inner code"),
  thread("B", 1, "again, alpha", { orphaned: false }),
  thread("C", 99, "a sentence that moved"),
  thread("D", 1, "nowhere in the first block")
];
var pick = (...ids) => ids.map((id) => POOL.find((candidate) => candidate.id === id));
var dump = (node) => node instanceof FakeText ? node.nodeValue : [
  node.tagName,
  [...node.attrs].sort(([a], [b]) => a.localeCompare(b)),
  node.childNodes.map(dump)
];
var hide = (document, hidden) => {
  if (hidden) document.setAttribute("data-sphinx-preview-comments", "off");
  else document.removeAttribute("data-sphinx-preview-comments");
};
var assertSame = (actual, expected, what) => {
  assert.equal(actual.length, expected.length, what);
  expected.forEach((object, index) => assert.ok(actual[index] === object, `${what} (number ${index + 1})`));
};
function fromNothing(threads, hidden = false) {
  const fresh = page();
  hide(fresh.document, hidden);
  fresh.comments.setThreads(threads);
  return dump(fresh.document);
}
var holders = (document) => document.querySelectorAll(
  "[data-okf-comment-thread], [data-okf-comment-badge], [data-okf-comment-orphan]"
);
(0, import_node_test.test)("adding one comment keeps the elements of the other threads and reads the mapped blocks once", () => {
  const { document, comments } = page();
  const shown = pick("a", "c", "g", "j", "l", "n", "q", "x");
  comments.setThreads(shown);
  const before = holders(document);
  assert.equal(before.length, shown.length);
  const places = before.map((element) => element.parentNode);
  const written = [];
  for (const element of before) {
    const set = element.setAttribute.bind(element);
    element.setAttribute = (name, value) => {
      written.push(name);
      set(name, value);
    };
    element.removeAttribute = (name) => {
      written.push(name);
      element.attrs.delete(name);
    };
  }
  const untouched = document.querySelectorAll("[data-line]").filter((block) => block.getAttribute("data-line") !== "20").map((block) => ({ block, nodes: [...block.childNodes] }));
  let reads = 0;
  const query = document.querySelectorAll.bind(document);
  document.querySelectorAll = (selector) => {
    if (selector === "[data-line]") reads += 1;
    return query(selector);
  };
  comments.setThreads([...shown, thread("new", 20, "somewhere unique")]);
  document.querySelectorAll = query;
  assert.equal(reads, 1, "one update reads the [data-line] blocks once");
  const after = holders(document);
  assert.equal(after.length, shown.length + 1);
  before.forEach((element, index) => {
    assert.ok(after.includes(element), `the element of thread ${index} is the same element`);
    assert.ok(element.parentNode === places[index], `the element of thread ${index} stays in its place`);
  });
  assert.deepEqual(written, [], "no attribute of an unchanged thread is written");
  for (const { block, nodes } of untouched) {
    assertSame(block.childNodes, nodes, "the other blocks keep their nodes");
  }
});
(0, import_node_test.test)("a reply, a resolve and a delete keep the elements of the threads that did not change", () => {
  const { document, comments } = page();
  const [a, g, x, n] = pick("a", "g", "x", "n");
  comments.setThreads([a, g, x, n]);
  const [markA, markG, badgeN, entryX] = holders(document);
  const replied2 = { ...a, comments: [...a.comments, { id: "r", author: "Bo", createdAt: "", body: "Yes" }] };
  comments.setThreads([replied2, { ...g, resolved: true }, x, n]);
  assertSame(holders(document), [markA, markG, badgeN, entryX], "after a reply and a resolve");
  assert.equal(markG.getAttribute("data-okf-comment-resolved"), "true");
  comments.setThreads([x, n]);
  assertSame(holders(document), [badgeN, entryX], "after two threads are deleted");
});
var SEQUENCES = [
  { name: "two threads in one block, the first deleted", lists: [pick("a", "b"), pick("b"), pick("a", "b")] },
  { name: "overlapping quotes", lists: [pick("c", "d", "e"), pick("d", "e"), pick("e"), pick("e", "c", "d", "f")] },
  { name: "nested blocks", lists: [pick("g", "h", "i", "j", "k"), pick("h", "i", "k"), pick("k", "j", "h", "g")] },
  {
    name: "a badge becomes a highlight and a highlight a badge",
    lists: [[{ ...pick("a")[0], anchor: { line: 1, quote: "absent" } }], pick("a"), [{ ...pick("a")[0], orphaned: true }]]
  },
  { name: "several badges below one block", lists: [pick("q", "r"), pick("q", "r", "s", "t"), pick("r", "t"), pick("t", "r")] },
  { name: "badges below a nested block and inside the block around it", lists: [pick("z"), pick("z", "A"), pick("A", "z", "y"), pick("A"), pick("z")] },
  { name: "the last badge of a block removed", lists: [pick("n", "o"), pick("o"), []] },
  { name: "several badges inside one block change order", lists: [pick("o", "p"), pick("p", "o"), pick("D", "p", "o"), pick("o", "D")] },
  { name: "orphan box order and removal", lists: [pick("x", "w", "v"), pick("w", "v"), pick("v", "x", "w"), pick("a"), pick("x")] },
  { name: "an orphan placed after a delete", lists: [[...pick("u"), thread("copy", 20, "moved somewhere unique")], pick("u"), pick("C", "u")] },
  { name: "an orphan resolved", lists: [pick("x"), [{ ...pick("x")[0], resolved: true }], pick("x")] },
  { name: "one id twice", lists: [[...pick("a"), ...pick("a"), ...pick("n", "n", "x", "x")], pick("a", "n", "x"), [...pick("x", "x")]] },
  { name: "text before and after a highlight", lists: [pick("f"), pick("a", "f"), pick("f", "B"), pick("B", "c", "a"), []] }
];
for (const { name, lists } of SEQUENCES) {
  (0, import_node_test.test)(`updated in place, the page is the page of a fresh render: ${name}`, () => {
    for (const hidden of [false, true]) {
      const { document, comments } = page();
      hide(document, hidden);
      lists.forEach((list, step) => {
        comments.setThreads(list);
        assert.deepEqual(dump(document), fromNothing(list, hidden), `list ${step + 1}, comments ${hidden ? "hidden" : "shown"}`);
      });
      comments.apply();
      assert.deepEqual(dump(document), fromNothing(lists.at(-1), hidden), "placed again after a content change");
    }
  });
}
(0, import_node_test.test)("updated in place, the page is the page of a fresh render: seeded random lists", () => {
  let seed = 517;
  const random = (below) => {
    seed = seed * 48271 % 2147483647;
    return seed % below;
  };
  for (let run = 0; run < 250; run += 1) {
    const { document, comments } = page();
    let list = [];
    let hidden = false;
    for (let step = 0; step < 14; step += 1) {
      const at = random(list.length || 1);
      const change = list.length < 4 ? 0 : random(8);
      const candidate = POOL[random(POOL.length)];
      if (change <= 1) {
        if (!list.some((one) => one.id === candidate.id)) list.splice(change === 0 ? list.length : at, 0, candidate);
      } else if (change === 2) list.splice(at, 1);
      else if (change === 3) list = list.map((one, index) => index === at ? { ...one, resolved: !one.resolved } : one);
      else if (change === 4) {
        list = list.map((one, index) => index === at ? { ...one, comments: [...one.comments, { id: `${step}`, author: "Bo", body: "Reply" }] } : one);
      } else if (change === 5) {
        list = list.map((one, index) => index === at ? { ...candidate, id: one.id } : one);
      } else if (change === 6) list = [...list.slice(at), ...list.slice(0, at)];
      else {
        hidden = !hidden;
        hide(document, hidden);
        comments.visibilityChanged();
      }
      comments.setThreads(list);
      assert.deepEqual(
        dump(document),
        fromNothing(list, hidden),
        `run ${run}, step ${step}: ${JSON.stringify(list.map((one) => [one.id, one.anchor]))}`
      );
    }
  }
});
(0, import_node_test.test)("an update keeps two text nodes side by side apart, as placing from nothing does", () => {
  const { document, comments } = page();
  const block = document.add("p", { "data-line": "30" }, document.content, "split in ");
  const second = block.appendChild(document.createTextNode("two text nodes"));
  const inSecond = thread("second", 30, "nodes");
  comments.setThreads([inSecond]);
  comments.setThreads([inSecond, thread("across", 30, "in two"), thread("first", 30, "split")]);
  assert.deepEqual(
    holders(document).map((element) => [element.tagName, element.textContent]),
    [["mark", "split"], ["mark", "nodes"], ["button", ""]],
    "a quote is found inside one text node only"
  );
  comments.setThreads([]);
  assert.deepEqual(block.childNodes.map((node) => node.nodeValue), ["split in ", "two text nodes"]);
  assert.ok(block.childNodes[1] === second);
});
(0, import_node_test.test)("an update repairs what changed in the page since the last one", () => {
  const list = pick("a", "g", "n", "q", "y", "z", "x");
  const { document, comments } = page();
  const fresh = page();
  comments.setThreads(list);
  const change = (target) => {
    const blocks = target.querySelectorAll("[data-line]");
    blocks.find((block) => block.getAttribute("data-line") === "4").setAttribute("data-sphinx-preview-editing", "true");
    blocks.find((block) => block.getAttribute("data-line") === "1").textContent = "alpha rewritten";
  };
  change(document);
  change(fresh.document);
  document.querySelector("[data-okf-comment-badge]").remove();
  document.querySelector("[data-okf-orphans]").remove();
  comments.setThreads(list);
  fresh.comments.setThreads(list);
  assert.deepEqual(dump(document), dump(fresh.document));
});
(0, import_node_test.test)("an open popover keeps its draft and its Delete question when the threads are posted again", () => {
  for (const id of ["a", "n", "x"]) {
    const { document, comments } = page();
    comments.setThreads(pick("a", "n", "x"));
    assert.equal(comments.openThread(id), true);
    document.querySelector("[data-okf-comment-reply-input]").value = "half a reply";
    document.querySelector("[data-okf-comment-delete]").fire("click");
    assert.ok(document.querySelector("[data-okf-comment-confirm]"), "the question is asked");
    comments.setThreads([...pick("a", "n", "x"), ...pick("g")]);
    const popovers = document.querySelectorAll("[data-okf-comment-popover]");
    assert.equal(popovers.length, 1);
    assert.equal(popovers[0].getAttribute("data-okf-comment-popover"), id);
    assert.equal(document.querySelector("[data-okf-comment-reply-input]").value, "half a reply");
    assert.ok(document.querySelector("[data-okf-comment-confirm]"), "the question stays");
    comments.setThreads(pick("g"));
    assert.equal(document.querySelectorAll("[data-okf-comment-popover]").length, 0, "the thread is gone");
  }
});
function measuredPage() {
  const opened = page();
  let receive;
  let measures = 0;
  registerHostHandlers({
    hostMessages: { on: (type, handler) => {
      if (type === "previewComments") receive = handler;
    } },
    parts: { commentThreads: opened.comments },
    scroll: { measure: () => {
      measures += 1;
    } }
  });
  const measured = (threads) => {
    measures = 0;
    receive({ threads });
    return measures;
  };
  return { ...opened, measured };
}
var replied = (one) => ({
  ...one,
  comments: [...one.comments, { id: "r", author: "Bo", createdAt: "", body: "Reply" }]
});
var inLine1 = thread("o", 1, "not in the paragraph");
var alsoInLine1 = thread("D", 1, "nowhere in the first block");
var inText = thread("n", 10, "not in the list");
var alsoInText = thread("n2", 10, "not in the item either");
for (const hidden of [false, true]) {
  const shown = hidden ? "hidden" : "shown";
  (0, import_node_test.test)(`the host's threads measure the page again when a highlight changes, comments ${shown}`, () => {
    const { document, measured } = measuredPage();
    hide(document, hidden);
    assert.equal(measured(pick("a")), 1, "a highlight added");
    assert.equal(measured(pick("a", "g")), 1, "one highlight more");
    assert.equal(
      measured([...pick("a"), { ...pick("g")[0], anchor: { line: 6, quote: "second nested" } }]),
      1,
      "a highlight moved to other words"
    );
    assert.equal(measured(pick("a")), 1, "a highlight removed");
  });
  (0, import_node_test.test)(`the host's threads measure the page again when a badge can move a block, comments ${shown}`, () => {
    const { document, measured } = measuredPage();
    hide(document, hidden);
    assert.equal(measured([inLine1]), 1, "the first badge inside a block that holds an element");
    assert.equal(measured([]), 1, "the last badge inside that block removed");
    measured(pick("a"));
    assert.equal(measured([...pick("a"), inLine1]), 1);
    assert.equal(measured(pick("a")), 1, "the last badge inside that block removed");
    assert.equal(measured([...pick("a"), inLine1]), 1);
    assert.equal(measured([...pick("a"), inText]), 1, "a badge goes from a block with an element to a text block");
    assert.equal(measured(pick("a", "q")), 1, "a badge below a block added");
    assert.equal(measured(pick("a", "q", "r")), 1, "a second badge below the block");
    assert.equal(measured(pick("a", "r", "q")), 1, "the two badges change places");
    assert.equal(
      measured([...pick("a"), { ...pick("r")[0], anchor: { line: 16, quote: "other" } }, ...pick("q")]),
      1,
      "a badge below a block moved to another block"
    );
    assert.equal(measured(pick("a", "q")), 1, "a badge below a block removed");
    assert.equal(measured(pick("a")), 1, "the last badge below the block removed");
  });
}
for (const hidden of [false, true]) {
  (0, import_node_test.test)(`the host's threads do not measure the page when no block can have moved, comments ${hidden ? "hidden" : "shown"}`, () => {
    const { document, measured } = measuredPage();
    hide(document, hidden);
    const [a, o, q] = [...pick("a"), inLine1, ...pick("q")];
    measured([a, o, q]);
    assert.equal(measured([a, o, q]), 0, "the same list again");
    assert.equal(measured([replied(a), replied(o), replied(q)]), 0, "replies");
    assert.equal(measured([{ ...a, resolved: true }, { ...o, resolved: true }, { ...q, resolved: true }]), 0, "resolved");
    assert.equal(measured([a, o, q]), 0, "reopened");
    assert.equal(measured([a, o, alsoInLine1, q]), 0, "a second badge inside a block");
    assert.equal(measured([a, alsoInLine1, o, q]), 0, "the badges inside the block change places");
    assert.equal(measured([a, o, q]), 0, "one of the two badges removed");
    assert.equal(measured([a, o, q, inText]), 0, "a badge inside a block that holds text only");
    assert.equal(measured([a, o, q, inText, alsoInText]), 0);
    assert.equal(measured([a, o, q]), 0, "the badges of the text block removed");
    assert.equal(measured([a, o, q, ...pick("x", "w")]), 0, "orphan entries added");
    assert.equal(measured([a, o, q, ...pick("w", "x")]), 0, "orphan entries change places");
    assert.equal(measured([a, o, q]), 0, "the orphan box removed");
  });
}
