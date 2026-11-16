p = "C:/Users/gaeta/Projets/chantier.worktrees/batch-18-CR-294/scenario/run_scenario.py"
raw = open(p, "rb").read()
s = raw.decode("utf-8").replace("\r\n", "\n")

old = '''    report_file.unlink()
    _, out = w.chantier("close", "--batch", name, "--yes")
    check("`close --yes` deletes the batch's own files,'''
new = '''    report_file.unlink()
    # one agent stopped without its hand-back: the user's word passes it, and the record keeps it
    slug = "".join(ch if ch.isalnum() else "-" for ch in str(w.work.resolve()))
    stopped = sorted((w.root / "claude-projects" / slug / "uuid-foreman" / "subagents")
                     .glob("agent-*.jsonl"))[0]
    runs(stopped, stopped.read_text(encoding="utf-8"))
    _, out = w.chantier("close", "--batch", name, "--stopped", stopped.stem, "--yes")
    check("`close --yes` deletes the batch's own files,'''
assert old in s
s = s.replace(old, new, 1)

old = '''    check("`batch-NN.json` is closed with its dates,'''
new = '''    said = f"declared stopped on the user's word: {stopped.stem}: "
    entry = (rec.get("stopped_agents") or [{}])[0]
    cost_part = report_file.read_text(encoding="utf-8").split("## Cost")[1].split("## Retro")[0]
    check("`close --stopped <agent> --yes` keeps the declaration: `stopped_agents` in the record "
          "with the agent, its transcript, the cause and the close time, a line under Cost in "
          "batch-NN.md, and the same line in what `close` prints",
          len(rec.get("stopped_agents", [])) == 1 and entry.get("agent") == stopped.stem
          and entry.get("transcript") == str(stopped)
          and entry.get("cause") == "its last record is a tool's result with no answer yet"
          and entry.get("declared") == rec["closed"]
          and f"- Declared stopped on the user's word: {stopped.stem} ({entry.get('cause')})"
          in cost_part and any(ln.startswith(said) and str(stopped) in ln for ln in out),
          f"{rec.get('stopped_agents')} {out}")
    check("`batch-NN.json` is closed with its dates,'''
assert old in s
s = s.replace(old, new, 1)

# a record closed without the flag has no key
old = '''        _, out = w.chantier("close", "--batch", w.name, "--yes")
        previous = w.name  # the last closed from here on
'''
new = '''        _, out = w.chantier("close", "--batch", w.name, "--yes")
        previous = w.name  # the last closed from here on
        check(f"{label}: a record closed without `--stopped` has no `stopped_agents` key",
              "stopped_agents" not in json.loads(
                  (archives / "batches" / f"{previous}.json").read_text(encoding="utf-8"))
              and "Declared stopped" not in report.read_text(encoding="utf-8"), "")
'''
assert old in s
s = s.replace(old, new, 1)
open(p, "wb").write(s.replace("\n", "\r\n").encode("utf-8"))
print("ok")
