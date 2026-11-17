# 174 — review-threads stress flake — report (PARTIAL: diagnostics only)

Landed 2026-10-28. PR https://github.com/gsemet/markdown-okf-schema-studio/pull/189 merged by the
user (while its normal run 40781646061 and heavy run 40781647461 were still running).

- Cause NOT proven. The popover (or page) vanished about 1 s after Resolve and never came back.
  Toolbar/tooltip motion and the table-menu change cleared by code reading.
- Delivered: the comment popover records why it closed (outside press + target, Escape, toggle,
  closed by page, re-apply without the thread) in the page trace; the scenario's last wait keeps its
  condition but dumps sidecar threads, host loads/patches/posts, page trace with close reason and
  stack, popover markup, marks and focus on failure (10 s wait instead of 30 s). One new unit test.
- The flake is NOT fixed: backlog P1 review-threads-resolve-popover-stress-flake stays open with a
  note. The next failure's dump should tell a page reload, a page-side close and a missing host
  post apart.
- Related (filed P2 comments-post-hash-before-staleness): CommentsController.post() stores its
  text hash before its last staleness check, so an overtaken post can make a newer one skip posting.
