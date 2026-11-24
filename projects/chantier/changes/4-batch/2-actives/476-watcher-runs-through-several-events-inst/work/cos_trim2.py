from pathlib import Path
subs = {
    "skills/chantier/references/hosts/claude-code.md": [
        ("The `no event for <name> in 2 h` line, like the `still running` line, names the restart command: run as is, nothing told to the user.",
         "The `no event for <name> in 2 h` line: start again at once as printed, nothing told."),
    ],
    "skills/chantier/references/hosts/copilot.md": [
        ("The `no event for <name> in 2 h` line, like the `still running` line, names the restart command: run as is, nothing told to the user; it comes only with no batch in flight.",
         "The `no event for <name> in 2 h` line (no batch in flight): start again at once as printed, nothing told."),
    ],
    "skills/chantier/references/session-start-chief-of-staff.md": [
        ("\n- `watch: <name> told up to cursor <n>; still watching ...`: nothing to start.", ""),
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
