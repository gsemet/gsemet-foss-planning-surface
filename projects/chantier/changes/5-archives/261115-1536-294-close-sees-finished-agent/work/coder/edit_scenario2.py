p = "C:/Users/gaeta/Projets/chantier.worktrees/batch-18-CR-294/scenario/run_scenario.py"
raw = open(p, "rb").read()
s = raw.decode("utf-8").replace("\r\n", "\n")

i = s.index("    age_sessions(w)\n    os.utime(chief, None)  # the Chief of Staff's own session")
j = s.index("    # a Foreman takes the batch over: the steering switches")
new = '''    os.utime(chief, None)  # the Chief of Staff's own session is written by the very call that closes
    driver_kept = driver.read_text(encoding="utf-8")
    runs(driver, driver_kept)  # a Driver with a step under way is not
    code, _ = w.chantier("close", "--batch", w.name, "--yes", expect=2)
    check("`close` still sees a Driver that runs, on a direct batch, and not the Chief of Staff's "
          "own transcript, which ends on a tool call", "transcript uuid-chief agent-agent-1 "
          "still runs" in w.last_stderr and "transcript uuid-chief still" not in w.last_stderr
          and "transcript uuid-chief cannot" not in w.last_stderr, w.last_stderr)
    driver.write_text(driver_kept, encoding="utf-8")
    os.utime(chief, None)
    code, out = w.chantier("close", "--batch", w.name, "--yes")
    check("`close` is not blocked by the Chief of Staff's own fresh transcript", code == 0
          and not (w.folder() / "batch.json").exists(), str(out))

'''
s = s[:i] + new + s[j:]

# the other age_sessions that only beat the 5-minute bound on a Claude batch
s = s.replace("    age_sessions(w)\n    for extra in ((), (\"--yes\",)):\n        code, out = w.chantier(\"close\", \"--batch\", name, *extra, expect=2)\n        check(f\"`close{' --yes' if extra else ''}` on a running batch where nothing runs",
              "    for extra in ((), (\"--yes\",)):\n        code, out = w.chantier(\"close\", \"--batch\", name, *extra, expect=2)\n        check(f\"`close{' --yes' if extra else ''}` on a running batch where nothing runs", 1)
open(p, "wb").write(s.replace("\n", "\r\n").encode("utf-8"))
print("ok")
