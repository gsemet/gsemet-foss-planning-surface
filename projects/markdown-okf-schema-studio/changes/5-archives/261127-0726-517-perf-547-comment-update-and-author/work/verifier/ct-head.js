"use strict";
var CT = (() => {
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

  // src/page/modules/commentThreads.ts
  var commentThreads_exports = {};
  __export(commentThreads_exports, {
    installCommentThreads: () => installCommentThreads
  });

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
    const highlight = (thread) => {
      const quote = thread.anchor.quote;
      if (quote === "") return void 0;
      const block = blockFor(thread.anchor.line);
      if (!block && thread.orphaned === false) return void 0;
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
    const badge = (thread) => {
      const block = blockFor(thread.anchor.line);
      if (!block) return void 0;
      return { kind: "badge", block, after: block.matches(SKIP) || NEXT_TO.has(block.tagName.toUpperCase()) };
    };
    return threads.map((thread) => (thread.orphaned === true ? void 0 : highlight(thread) ?? badge(thread)) ?? { kind: "orphan" });
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
        const thread = threads[index];
        const old = before.get(thread.id);
        return [{ place, thread, mark: old && sitsAt(old, place) ? take(before, thread.id) : void 0 }];
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
      marks = wanted.map(({ mark, thread }) => {
        paintResolved(mark, thread.resolved);
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
        const thread = threads[index];
        const old = take(before, thread.id);
        const button = old && old.getAttribute(AFTER) !== null === place.after ? old : newBadge(thread.id, place.after);
        paintResolved(button, thread.resolved);
        const count = thread.comments.length;
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
      const entries = listed.map((thread) => {
        const entry = take(before, thread.id) ?? newEntry(thread.id);
        paintResolved(entry.element, thread.resolved);
        paintText(entry.quote, thread.anchor.quote !== "" ? thread.anchor.quote : "(no quoted text)");
        const first = thread.comments[0];
        const count = thread.comments.length;
        paintText(entry.meta, `${first ? first.author + ": " + first.body.slice(0, 120) : ""} (${count} comment${count === 1 ? "" : "s"}${thread.resolved ? ", resolved" : ""})`);
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
      const thread = threads.find((candidate) => candidate.id === openId);
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
          row.appendChild(actionButton(thread?.resolved ? "Reopen" : "Resolve", "data-okf-comment-resolve", busy));
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
      const thread = threads.find((candidate) => candidate.id === reopen);
      if (holder && thread) {
        open(thread, holder);
        const input = replyInput();
        if (input && typeof draft === "string") input.value = draft;
        confirming = asking === reopen ? asking : void 0;
        discarding = discardAsked === reopen ? discardAsked : void 0;
        paintReply();
        paintActions();
      } else {
        trace?.("comment popover closed", `re-apply without ${thread ? "a holder" : "the thread"}, thread ${reopen}, ${threads.length} thread(s)`);
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
    const open = (thread, target) => {
      close();
      const root = document.createElement("div");
      root.setAttribute(POPOVER, thread.id);
      root.setAttribute("role", "dialog");
      root.setAttribute("aria-label", "Comment thread");
      if (thread.resolved) root.setAttribute("data-okf-comment-resolved", "true");
      if (thread.resolved) {
        const state = document.createElement("div");
        state.setAttribute("data-okf-comment-state", "resolved");
        state.textContent = "Resolved";
        root.appendChild(state);
      }
      for (const comment of thread.comments) {
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
      openId = thread.id;
      position(target);
      paintReply();
    };
    const holderOf = (target) => target.closest(`[${MARK}], [${BADGE}], [${ORPHAN}]`);
    const idOf = (holder) => holder.getAttribute(MARK) ?? holder.getAttribute(BADGE) ?? holder.getAttribute(ORPHAN);
    const toggle = (holder) => {
      const id = idOf(holder);
      const thread = threads.find((candidate) => candidate.id === id);
      if (!thread) return false;
      if (openId === thread.id) closeOrAsk("toggled");
      else if (draftChanged()) closeOrAsk("switched");
      else open(thread, holder);
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
        const thread = threads.find((candidate) => candidate.id === openId);
        if (thread) startAction("resolve", (threadId) => resolveHook(threadId, !thread.resolved));
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
  return __toCommonJS(commentThreads_exports);
})();
