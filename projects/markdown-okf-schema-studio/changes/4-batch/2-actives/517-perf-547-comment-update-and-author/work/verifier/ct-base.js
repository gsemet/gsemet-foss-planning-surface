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

  // ../../gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/517-perf-547-comment-update-and-author/work/verifier/base-tree/src/page/modules/commentThreads.ts
  var commentThreads_exports = {};
  __export(commentThreads_exports, {
    installCommentThreads: () => installCommentThreads
  });

  // ../../gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/517-perf-547-comment-update-and-author/work/verifier/base-tree/src/page/modules/commentThreadData.ts
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

  // ../../gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/517-perf-547-comment-update-and-author/work/verifier/base-tree/src/page/modules/commentEditorBehaviour.ts
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

  // ../../gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/517-perf-547-comment-update-and-author/work/verifier/base-tree/src/page/modules/commentThreads.ts
  function installCommentThreads(document, window, hooks, trace) {
    const MARK = "data-okf-comment-thread";
    const BADGE = "data-okf-comment-badge";
    const BADGED = "data-okf-comment-badged";
    const POPOVER = "data-okf-comment-popover";
    const REPLY_INPUT = "data-okf-comment-reply-input";
    const REPLY_SEND = "data-okf-comment-reply-send";
    const ORPHAN = "data-okf-comment-orphan";
    const ORPHANS = "data-okf-orphans";
    const ACTIONS = "data-okf-comment-thread-actions";
    const ACTION_ERROR = "data-okf-comment-action-error";
    const SKIP = `pre, code, script, style, textarea, svg, .katex, .math, .math-inline, .math-display, .myst-mermaid-figure, .myst-plantuml-figure, .myst-vega-figure, [data-okf-properties], .okf-comment, .okf-chip, [data-sphinx-preview-block-editor], [data-sphinx-preview-editing], [data-sphinx-preview-included], [${MARK}], [${BADGE}], [${POPOVER}]`;
    const EDITING = "[data-sphinx-preview-block-editor], [data-sphinx-preview-editing]";
    const NEXT_TO = /* @__PURE__ */ new Set(["TABLE", "THEAD", "TBODY", "TR", "UL", "OL", "DL", "PRE", "DETAILS", "IMG", "HR", "SVG"]);
    const MIN_MOVED_QUOTE = 12;
    let threads = [];
    let popover;
    let openId;
    const ANSWER_TIMEOUT_MS = 15e3;
    let sent;
    let act;
    let confirming;
    let discarding;
    let openTarget;
    let orphanBox;
    let addedOrphans = [];
    const hidden = () => {
      const root = document.documentElement;
      return root?.getAttribute("data-sphinx-preview-comments") === "off" || root?.getAttribute("data-okf-show-comments") === "false";
    };
    const paintFocus = (mark) => {
      if (hidden()) {
        for (const name of ["tabindex", "role", "aria-haspopup"]) mark.removeAttribute(name);
        return;
      }
      mark.setAttribute("tabindex", "0");
      mark.setAttribute("role", "button");
      mark.setAttribute("aria-haspopup", "dialog");
    };
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
    const unwrap = (mark) => {
      const parent = mark.parentNode;
      if (!parent) return;
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
    };
    let addedMarks = [];
    let addedBadges = [];
    let badgedBlocks = [];
    const clear = () => {
      addedMarks.forEach(unwrap);
      addedBadges.forEach((badge2) => badge2.remove());
      badgedBlocks.forEach((block) => block.removeAttribute(BADGED));
      addedMarks = [];
      addedBadges = [];
      badgedBlocks = [];
      orphanBox?.remove();
      orphanBox = void 0;
      addedOrphans = [];
    };
    const spanOf = (element) => {
      const start = Number(element.getAttribute("data-line"));
      if (!Number.isFinite(start)) return void 0;
      const endValue = Number(element.getAttribute("data-end-line"));
      return [start, Number.isFinite(endValue) && endValue >= start ? endValue : start];
    };
    const eligible = (element) => {
      if (element.closest(EDITING) || element.closest("[data-okf-properties]")) return false;
      if (element.closest("[data-sphinx-preview-included]")) return false;
      const container = element.parentNode;
      return !(container && container.nodeType === 1 && container.closest(SKIP));
    };
    const blockFor = (line) => {
      let best;
      let bestSize = Infinity;
      document.querySelectorAll("[data-line]").forEach((element) => {
        const span = spanOf(element);
        if (!span || line < span[0] || line > span[1]) return;
        if (!eligible(element)) return;
        const size = span[1] - span[0];
        if (size <= bestSize) {
          best = element;
          bestSize = size;
        }
      });
      return best;
    };
    const textNodesOf = (block) => {
      const found = [];
      const walk = (node) => {
        for (let child = node.firstChild; child; child = child.nextSibling) {
          if (child.nodeType === 3) {
            found.push(child);
          } else if (child.nodeType === 1 && !child.matches(SKIP)) {
            walk(child);
          }
        }
      };
      if (!block.matches(SKIP)) walk(block);
      return found;
    };
    const attach = (thread) => {
      const quote = thread.anchor.quote;
      if (quote === "") return false;
      const block = blockFor(thread.anchor.line);
      if (!block && thread.orphaned === false) return false;
      const blocks = block ? [block] : [];
      if (!block) {
        document.querySelectorAll("[data-line]").forEach((element) => {
          if (eligible(element)) blocks.push(element);
        });
      }
      const variants = [quote];
      const collapsed = quote.replace(/\s+/gu, " ");
      if (collapsed !== quote) variants.push(collapsed);
      const seen = /* @__PURE__ */ new Set();
      const nodes = [];
      for (const candidate of blocks) {
        for (const node of textNodesOf(candidate)) {
          if (!seen.has(node)) {
            seen.add(node);
            nodes.push(node);
          }
        }
      }
      if (!block) {
        if (collapsed.trim().length < MIN_MOVED_QUOTE) return false;
        let total = 0;
        for (const node of nodes) {
          const value = node.nodeValue ?? "";
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
        if (total !== 1) return false;
      }
      for (const node of nodes) {
        const value = node.nodeValue ?? "";
        for (const variant of variants) {
          const found = locate(value, variant, 0);
          if (!found) continue;
          const { index, length } = found;
          const parent = node.parentNode;
          if (!parent) continue;
          const mark = document.createElement("mark");
          mark.setAttribute(MARK, thread.id);
          if (thread.resolved) mark.setAttribute("data-okf-comment-resolved", "true");
          paintFocus(mark);
          mark.textContent = value.slice(index, index + length);
          if (index === 0) {
            parent.replaceChild(mark, node);
          } else {
            node.nodeValue = value.slice(0, index);
            parent.insertBefore(mark, node.nextSibling);
          }
          addedMarks.push(mark);
          const rest = value.slice(index + length);
          if (rest !== "") parent.insertBefore(document.createTextNode(rest), mark.nextSibling);
          return true;
        }
      }
      return false;
    };
    const badge = (thread) => {
      const block = blockFor(thread.anchor.line);
      if (!block) return false;
      const button = document.createElement("button");
      button.setAttribute("type", "button");
      button.setAttribute(BADGE, thread.id);
      if (thread.resolved) button.setAttribute("data-okf-comment-resolved", "true");
      button.setAttribute("aria-haspopup", "dialog");
      button.setAttribute("aria-label", `Comment thread, ${thread.comments.length} comment${thread.comments.length === 1 ? "" : "s"}`);
      if (block.matches(SKIP) || NEXT_TO.has(block.tagName.toUpperCase())) {
        button.setAttribute("data-okf-comment-badge-after", "true");
        block.parentNode?.insertBefore(button, block.nextSibling);
      } else {
        block.setAttribute(BADGED, "true");
        badgedBlocks.push(block);
        block.appendChild(button);
      }
      addedBadges.push(button);
      return true;
    };
    const renderOrphans = (orphans) => {
      if (orphans.length === 0) return;
      const box = document.createElement("div");
      box.setAttribute(ORPHANS, "true");
      box.setAttribute("role", "region");
      box.setAttribute("aria-label", "Orphaned comments");
      const title = document.createElement("div");
      title.setAttribute("data-okf-orphans-title", "true");
      title.textContent = "Orphaned comments";
      box.appendChild(title);
      for (const thread of orphans) {
        const item = document.createElement("button");
        item.setAttribute("type", "button");
        item.setAttribute(ORPHAN, thread.id);
        item.setAttribute("aria-haspopup", "dialog");
        if (thread.resolved) item.setAttribute("data-okf-comment-resolved", "true");
        const quote = document.createElement("span");
        quote.setAttribute("data-okf-orphan-quote", "true");
        quote.textContent = thread.anchor.quote !== "" ? thread.anchor.quote : "(no quoted text)";
        const first = thread.comments[0];
        const meta = document.createElement("span");
        meta.setAttribute("data-okf-orphan-meta", "true");
        const count = thread.comments.length;
        meta.textContent = `${first ? first.author + ": " + first.body.slice(0, 120) : ""} (${count} comment${count === 1 ? "" : "s"}${thread.resolved ? ", resolved" : ""})`;
        item.appendChild(quote);
        item.appendChild(meta);
        box.appendChild(item);
        addedOrphans.push(item);
      }
      const main = document.getElementById?.("sphinx-myst-preview-content");
      const parent = main?.parentNode ?? document.body;
      parent.insertBefore(box, main ? main.nextSibling : null);
      orphanBox = box;
    };
    const apply = () => {
      const reopen = hidden() ? void 0 : openId;
      const draft = replyInput()?.value;
      const asking = confirming;
      const discardAsked = discarding;
      close();
      clear();
      if (threads.length === 0) {
        if (reopen !== void 0) trace?.("comment popover closed", `re-apply without threads, thread ${reopen}`);
        return;
      }
      const orphans = [];
      for (const thread of threads) {
        if (thread.orphaned === true || !attach(thread) && !badge(thread)) orphans.push(thread);
      }
      renderOrphans(orphans);
      if (reopen !== void 0) {
        const holder = [...addedMarks, ...addedBadges, ...addedOrphans].find((candidate) => idOf(candidate) === reopen);
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
      }
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
        apply();
      },
      apply,
      close: () => close("closed by the page"),
      // @implements_req SwRS-MDOKFSTUDIO-REVIEW-152
      visibilityChanged() {
        if (hidden()) close("comments hidden");
        addedMarks.forEach(paintFocus);
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
