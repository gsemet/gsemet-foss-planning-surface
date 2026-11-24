from pathlib import Path
subs = {
    "skills/chantier/references/chief-of-staff.md": [
        ("| a watcher's notification or end (a block that ends with its `still watching` line, or its background task ended) | read its output, act on each line as in [The watcher](session-start-chief-of-staff.md#the-watcher); a `still watching` line needs no restart (the watcher runs on); a last line `watch: <batch> still running: …`, or `watch: no event for <name> in 2 h; ended …`, names the restart:",
         "| a watcher's notification or end | read its output, act on each line as in [The watcher](session-start-chief-of-staff.md#the-watcher); a `still watching` last line needs no restart; a last line `watch: <batch> still running: …`, or `watch: no event for <name> in 2 h; ended …`, names the restart:"),
        ("a `forge saw merged` line in `status` or in a watcher's notification or end;",
         "a `forge saw merged` line in `status` or at a watcher's end;"),
        ("a move that clears a running-batch mark: act as at a watcher's notification or end |",
         "a move that clears a running-batch mark: act as at a watcher's end |"),
    ],
    "skills/chantier/references/session-start-chief-of-staff.md": [
        ("- `watch: no event for <name> in 2 h; ended ...` (it comes only while no batch is in flight: none\n  running, none paused with a PR the record holds neither merged nor cancelled): start it again at\n  once with the printed command, saying nothing to the user.\n- `watch: <name> told up to cursor <n>; still watching ...` (the streaming form's notification):\n  act on the lines above it; the watcher runs on, nothing to start.",
         "- `watch: no event for <name> in 2 h; ended ...` (only with no batch in flight): start it again at\n  once with the printed command, saying nothing to the user.\n- `watch: <name> told up to cursor <n>; still watching ...`: nothing to start."),
        ("says a watcher's end or notification does not wake the session", "says a watcher's end does not wake the session"),
    ],
}
for name, pairs in subs.items():
    p = Path(name)
    raw = p.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    t = raw.replace("\r\n", "\n")
    for a, b in pairs:
        assert t.count(a) == 1, a
        t = t.replace(a, b)
    p.write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))
