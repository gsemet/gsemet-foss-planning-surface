p = "C:/Users/gaeta/Projets/chantier.worktrees/batch-18-CR-294/scenario/run_scenario.py"
raw = open(p, "rb").read()
s = raw.decode("utf-8").replace("\r\n", "\n")

a = "def priced_foreman(w: World) -> None:"
helpers = '''def turn_line(kind: str, block: dict, stop: str | None = None) -> str:
    """One `user` or `assistant` record of a Claude transcript, as `close` reads its end."""
    message = {"role": kind, "content": [block]}
    if kind == "assistant":
        message["stop_reason"] = stop
    return json.dumps({"type": kind, "message": message}) + "\\n"


def call_line(name: str, ident: str = "tu-1") -> str:
    return turn_line("assistant", {"type": "tool_use", "id": ident, "name": name, "input": {}},
                     "tool_use")


def result_line(ident: str = "tu-1") -> str:
    return turn_line("user", {"type": "tool_result", "tool_use_id": ident, "content": "ok"})


def runs(f: Path, kept: str) -> None:
    """The agent's transcript `kept`, then a tool's result with no assistant record after it: it
    reads as still running, whatever the file's age. `kept` alone makes it ended."""
    f.write_text(kept + call_line("Bash") + result_line(), encoding="utf-8")


'''
assert a in s
s = s.replace(a, helpers + a, 1)

old = '''    def refused(label: str, text: str, change: dict | None = None, env: dict | None = None) -> None:
        if change is not None:
            state.write_text(json.dumps({**d, **change}))
        for extra in ((), ("--yes",)):
            code, out = w.chantier("close", "--batch", name, *extra, env=env, expect=2)
            check(f"`close{' --yes' if extra else ''}` refuses {label}, naming it and deleting "
                  "nothing", code == 2 and text in w.last_stderr and not out
                  and (w.folder() / "batch.json").is_file(), w.last_stderr)
        state.write_text(base)
'''
new = '''    def refused(label: str, text: str | tuple, change: dict | None = None, env: dict | None = None,
                flags: tuple = ()) -> None:
        if change is not None:
            state.write_text(json.dumps({**d, **change}))
        texts = (text,) if isinstance(text, str) else text
        for extra in ((), ("--yes",)):
            code, out = w.chantier("close", "--batch", name, *flags, *extra, env=env, expect=2)
            check(f"`close{' ' + ' '.join(flags) if flags else ''}{' --yes' if extra else ''}` "
                  f"refuses {label}, naming it and deleting nothing",
                  code == 2 and all(t in w.last_stderr for t in texts) and not out
                  and "Nothing was deleted." in w.last_stderr
                  and (w.folder() / "batch.json").is_file(), w.last_stderr)
        state.write_text(base)
'''
assert old in s
s = s.replace(old, new, 1)

i = s.index('    refused("a transcript written within 5 minutes"')
j = s.index('    crs = [{**c, "status": "ready"} if i == 0 else c')
new = '''    # the transcripts' ends, never their ages (the files are just written, or aged 10 minutes)
    hint = "close --stopped <name> for each"
    foreman_kept = main.read_text()
    main.write_text(foreman_kept + call_line("Bash"))
    age_sessions(w)
    refused("a Foreman whose last call waits on a tool for 10 minutes",
            ("transcript uuid-foreman still runs", "its tool call Bash has no result yet",
             str(main), hint))
    main.write_text(foreman_kept)
    age_sessions(w)
    first, second = sorted(sub.glob("agent-*.jsonl"))[:2]
    kept, kept2 = first.read_text(), second.read_text()
    runs(first, kept)
    refused("an agent whose last record is a tool's result with no answer",
            (f"transcript uuid-foreman {first.stem} still runs",
             "its last record is a tool's result with no answer yet", str(first), hint))
    # 3. the hand-back and its result, the file just written: nothing runs
    first.write_text(kept + call_line("SubagentHandback") + result_line(), encoding="utf-8")
    code, out = w.chantier("close", "--batch", name)
    check("`close` passes an agent that handed back, though its file was just written, and prints "
          "the final cost", code == 0 and any(ln.startswith("Total: ") for ln in out), str(out))
    # 4. a turn ended with a plain message
    first.write_text(kept + turn_line("assistant", {"type": "text", "text": "done"}, "end_turn"),
                     encoding="utf-8")
    code, out = w.chantier("close", "--batch", name)
    check("`close` passes an agent whose last record is an `end_turn` message", code == 0
          and any(ln.startswith("Total: ") for ln in out), str(out))
    # 5. a cut last line cannot be read, and the flag does not pass it
    first.write_text(kept + '{"type": "assistant", "mess', encoding="utf-8")
    refused("an agent whose last line is cut JSON",
            (f"transcript uuid-foreman {first.stem} cannot be read",
             "its last line is not complete JSON", str(first)))
    refused("`--stopped` of a transcript that cannot be read",
            (f"close --stopped {first.stem}: its transcript cannot be read ({first})",),
            flags=("--stopped", first.stem))
    first.write_text(kept, encoding="utf-8")
    # 6. a recorded Foreman transcript that is missing
    gone = main.with_name("uuid-gone.jsonl")
    refused("a recorded Foreman transcript that is missing",
            ("transcript uuid-gone cannot be read", "the file is missing", str(gone)),
            {"foreman_transcript": "uuid-gone", "foreman_transcripts": ["uuid-gone"]})
    # 7. --stopped, on a running agent
    runs(first, kept)
    shelf = [w.folder(), w.state / "5-archives" / "batches"]
    for given in (first.stem, first.stem.removeprefix("agent-")):
        before = [tree_bytes(p) for p in shelf]
        code, out = w.chantier("close", "--batch", name, "--stopped", given)
        at = [i for i, ln in enumerate(out) if ln.startswith("declared stopped")]
        cost = [i for i, ln in enumerate(out) if ln.startswith("Total: ")]
        check(f"`close --stopped {given}` (no --yes) passes the agent the user declared stopped, "
              "says so before the cost, and writes nothing",
              code == 0 and [tree_bytes(p) for p in shelf] == before and at and cost
              and out[at[0]].startswith(f"declared stopped on the user's word: {first.stem}: ")
              and str(first) in out[at[0]] and at[0] < cost[0], str(out))
    refused("`--stopped` of a name that is not in the batch",
            (f"close --stopped nobody: no transcript of {name} by that name; still running: "
             f"{first.stem}",), flags=("--stopped", "nobody"))
    refused("`--stopped` of an agent whose transcript shows it ended",
            (f"close --stopped {second.stem}: its transcript shows it ended; drop the flag",),
            flags=("--stopped", second.stem))
    runs(second, kept2)
    refused("two running agents with one named, the other one",
            (f"transcript uuid-foreman {second.stem} still runs", str(second), hint),
            flags=("--stopped", first.stem))
    second.write_text(kept2, encoding="utf-8")
    refused("an open order, though the running agent is named", "order O-99 (qa) is open",
            {"orders": d["orders"] + [{"id": "O-99", "kind": "qa", "cr": "-", "note": "x",
                                       "sent": d["created"], "done": None}]},
            flags=("--stopped", first.stem))
    first.write_text(kept, encoding="utf-8")
'''
s = s[:i] + new + s[j:]
open(p, "wb").write(s.replace("\n", "\r\n").encode("utf-8"))
print("ok")
