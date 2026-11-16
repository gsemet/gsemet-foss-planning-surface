    batches = w.state / "5-archives" / "batches"
    record_file, report_file = batches / f"{w.name}.json", batches / f"{w.name}.md"
    retro_lines = [ln for ln in out if ln.startswith("retro:")]
    record_lines = [ln for ln in out if ln.startswith("record:")]
    check("`close` alone prints the `retro:` and `record:` lines naming the batch's record, and "
          "touches no byte of the record, the retro or the archives",
          len(retro_lines) == 1 and f"5-archives/batches/{w.name}.md" in retro_lines[0]
          and "4-batch/retro.md" in retro_lines[0] and len(record_lines) == 1
          and f"5-archives/batches/{w.name}.json" in record_lines[0]
          and retro.read_bytes() == retro_bytes and tree_bytes(w.state / "5-archives") == shelf
          and not report_file.exists(), str(out))
    shown = [float(m[1]) for m in (re.match(r"Total: \$(\d+\.\d\d)", ln) for ln in out) if m]
    check("`close` prints the final cost, with a call made after the last `pause` in it",
          shown and shown[0] > w.paused_total and "Not final" not in "\n".join(out)
          and "To date" not in "\n".join(out), f"{out} (last pause: {w.paused_total})")
    first = w.cr("CR-101")
    stamp = datetime.strptime(first["merged_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%y%m%d-%H%M")
    collision = w.state / "5-archives" / f"{stamp}-{Path(first['path']).name}"
    collision.mkdir(parents=True)
    (collision / "sentinel.txt").write_text("do not overwrite")
    code, _ = w.chantier("close", "--batch", name, "--yes", expect=3)
    check("an archive collision refuses the close and puts everything back",
          code == 3 and (collision / "sentinel.txt").read_text() == "do not overwrite"
          and (w.state / first["path"] / "03-change-spec.md").is_file()
          and (folder / "batch.json").is_file() and (folder / "events.jsonl").is_file()
          and len(list((folder / "3-done").iterdir())) == 4
          and not (w.state / f".closing-{name}").exists(), w.last_stderr)
    check("the archive collision leaves 4-batch/retro.md, the record and no Markdown in place",
          retro.read_bytes() == retro_bytes and record_file.read_bytes() == running
          and not report_file.exists())
    shutil.rmtree(collision)
    report_file.write_text("planted\n")
    code, _ = w.chantier("close", "--batch", name, "--yes", expect=3)
    check("a planted batch-NN.md refuses the close (exit 3), every rename put back, the record "
          "and the retro unchanged byte for byte",
          code == 3 and report_file.read_text() == "planted\n" and retro.read_bytes() == retro_bytes
          and record_file.read_bytes() == running
          and (folder / "batch.json").is_file() and len(list((folder / "3-done").iterdir())) == 4
          and not (w.state / f".closing-{name}").exists(), w.last_stderr)
    report_file.unlink()
    _, out = w.chantier("close", "--batch", name, "--yes")
    check("`close --yes` deletes the batch's own files, keeps the empty state folders, and "
          "repeats what is left to remove",
          sorted(p.name for p in folder.iterdir()) == ["1-pending", "2-actives", "3-done"]
          and not any(list(p.iterdir()) for p in folder.iterdir())
          and Path(dropped["worktree"]).is_dir() and out[0].endswith("4 CRs archived")
          and any(dropped["worktree"] in ln for ln in out), str(out))
    retro_lines = [ln for ln in out if ln.startswith("retro:")]
    record_lines = [ln for ln in out if ln.startswith("record:")]
    check("`close --yes` says where the retro is kept and that the record is closed",
          len(retro_lines) == 1 and f"5-archives/batches/{w.name}.md" in retro_lines[0]
          and retro_lines[0].startswith("retro: kept in") and len(record_lines) == 1
          and record_lines[0].endswith(".json closed"), str(out))
    total = [float(m[1]) for m in (re.match(r"Total: (?:at least )?\$(\d+\.\d\d)", ln)
                                   for ln in out) if m]
    rec = json.loads(record_file.read_text(encoding="utf-8"))
    check("`batch-NN.json` is closed with its dates, its shape and the final cost the close printed",
          rec["schema"] == 1 and rec["state"] == "closed" and rec["closed"]
          and rec["opened"] == opened and rec["mode"] == mode and rec["steering"] == steering
          and rec["host"] and total and abs(rec["cost_usd"] - total[0]) < 0.0051
          and rec["report"] == f"{w.name}.md" and rec["backfill"] is None, f"{rec} {total}")
    check("its CRs carry the result, an archive that exists, the PR, the rounds and the cost",
          sorted(c["cr"] for c in rec["crs"]) == crs_before
          and {c["result"] for c in rec["crs"]} == {"merged", "dropped"}
          and all((w.state / c["archive"]).is_dir() for c in rec["crs"])
          and all(c["archive"].startswith("5-archives/") for c in rec["crs"]
                  if c["result"] == "merged")
          and all(c["archive"].startswith("6-trash/") for c in rec["crs"]
                  if c["result"] == "dropped")
          and all(c["pr"] and c["rounds"] is not None and c["cost_usd"] is not None
                  for c in rec["crs"] if c["result"] == "merged"), str(rec["crs"]))
    text = report_file.read_bytes()
    check("`batch-NN.md` holds the table, the cost lines and the retro's two pause sections byte "
          "for byte",
          b"## Completion" in text and b"## Cost" in text and b"- Total: " in text
          and retro_bytes in text and all(c["cr"].encode() in text for c in rec["crs"])
          and not retro.exists(), text.decode("utf-8")[:600])
    check("no retro.md is left in any CR archive, and no <stamp>-batch folder is made",
          not list((w.state / "5-archives").glob("*/retro.md"))
          and not [p for p in (w.state / "5-archives").iterdir()
                   if re.fullmatch(r"\d{6}-\d{4}-batch-\d+", p.name)])
    archived = next((w.state / "5-archives").glob("*-101-fix-login-timeout")) / "STATUS.md"
    check("the merged CRs are in 5-archives, named for their merge time, intact",
          re.fullmatch(rf"{stamp}-101-fix-login-timeout", archived.parent.name)
          and len(list((w.state / "5-archives").glob(f"{stamp[:6]}-*-10[1245]-*"))) >= 4
          and (archived.parent / "03-change-spec.md").is_file(), archived.parent.name)
    page = archived.read_text(encoding="utf-8")
    check("at `close` the archived CR page gives its cost as final, priced to then",
          re.search(r"## Cost\s+\$\d+\.\d\d\.\s*$", page) and "so far" not in page
          and "STATUS.md)" not in page.split("## Documents")[0], page)
    index = json.loads((w.state / "STATUS.json").read_text(encoding="utf-8"))
    cr_archives = [p for p in (w.state / "5-archives").iterdir()
                   if p.is_dir() and p.name != "batches"]
    check("the index does not list `batches` among the merged CRs, nor count it",
          not any("batches" in str(e.get("path")) for e in index["merged"])
          and index["merged_total"] == len(cr_archives), str(index["merged_total"]))
    # the Chief of Staff removes it on the same word, with git
    w.sh("git", "worktree", "remove", "--force", dropped["worktree"])
    w.sh("git", "branch", "-D", dropped["branch"])
    check("the dropped CR's worktree and branch are gone by the Chief of Staff's hands",
          not Path(dropped["worktree"]).exists()
          and not w.sh("git", "branch", "--list", dropped["branch"]))
    board = (w.state / "STATUS.md").read_text(encoding="utf-8")
    check("the archives and the trash stay, and the board forgets the batch",
          name not in board and "No batch." in board
          and (w.state / dropped["path"] / "STATUS.md").is_file(), board)


def opened_record(w: World) -> None:
    """Step 1: `open` reserves the number by writing the batch's record, as running."""
    path = w.state / "5-archives" / "batches" / f"{w.name}.json"
    d = w.batch()
    rec = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    check("`open` writes `5-archives/batches/batch-NN.json`, running, from the batch's settings",
          rec.get("schema") == 1 and rec["state"] == "running" and rec["batch"] == w.name
          and rec["number"] == int(w.name.removeprefix("batch-")) and rec["opened"] == d["created"]
          and rec["mode"] == d["mode"] and rec["steering"] == d["steering"]
          and rec["host"] == d["host"] and rec["budget_usd"] == d["budget_usd"]
          and rec["crs"] == [] and rec["closed"] is None and rec["cost_usd"] is None
          and rec["report"] is None and rec["backfill"] is None, str(rec))
    ignored = (w.state / ".gitignore").read_text(encoding="utf-8").splitlines()
    check("`open` still writes `.batch-number`, and the record is published, not ignored",
          (w.state / ".batch-number").read_text().strip() == str(rec.get("number"))
          and ".batch-number" in ignored and not any("batches" in ln for ln in ignored),
          str(ignored))


def tree_bytes(folder: Path) -> dict[str, bytes]:
    return {p.relative_to(folder).as_posix(): p.read_bytes()
            for p in sorted(folder.rglob("*")) if p.is_file()}


def retro_cases(w: World) -> None:
    note("\n## 11c. The batch's retro in its record, with no CR archived, or no retro")
    archives = w.state / "5-archives"
    previous = w.name  # closed by 11b
    for label, text in (("a batch of cancelled CRs", "# Retro\n\n## Pause 1\n\n- one, fix one\n"),
                        ("no retro.md", None), ("a whitespace-only retro.md", " \n\t\n")):
        _, item = prepare_cr(w, f"Retro {label}")
        w.reset()
        w.start(str(item), *FROM_AGENTS_MD)
        w.env["CHANTIER_BATCH"] = w.name
        _, head = w.chantier("status")
        check(f"{label}: after a close and a new `open`, `status` names the last closed batch on "
              "its second line",
              len(head) > 1 and head[1].startswith(f"last closed: {previous}, closed 20"),
              str(head[:2]))
        previous = w.name
        number = int(w.batch()["crs"][0]["id"].removeprefix("CR-"))
        w.chantier("foreman", "set", "local_foreman_retro", "--epoch", 1)
        w.chantier("cancel", w.batch()["crs"][0]["id"], "--epoch", 1)
        w.chantier("pause", "--epoch", 1)
        priced_foreman(w)
        age_sessions(w)
        retro = w.folder() / "retro.md"
        if text is not None:
            retro.write_text(text, encoding="utf-8", newline="")
        before = sorted(p.name for p in archives.iterdir())
        merged_before = json.loads((w.state / "STATUS.json").read_text(encoding="utf-8")).get(
            "merged_total")
        _, out = w.chantier("close", "--batch", w.name)
        lines = [ln for ln in out if ln.startswith("retro:")]
        report = archives / "batches" / f"{w.name}.md"
        if text is not None and text.strip():
            check(f"{label}: `close` alone says the retro goes into the batch's Markdown, and "
                  "touches nothing",
                  len(lines) == 1 and f"5-archives/batches/{w.name}.md" in lines[0]
                  and retro.is_file() and not report.exists()
                  and sorted(p.name for p in archives.iterdir()) == before, str(out))
        else:
            check(f"{label}: `close` prints `retro: no retro`",
                  lines == ["retro: no retro"], str(out))
        _, out = w.chantier("close", "--batch", w.name, "--yes")
        new = [p for p in archives.iterdir() if p.name not in before]
        body = report.read_text(encoding="utf-8") if report.is_file() else ""
        if text is not None and text.strip():
            check(f"{label}: `close --yes` writes batch-NN.md with the retro, and no folder for "
                  "the batch in 5-archives",
                  text in body and "No retro was written." not in body and not new
                  and any(ln.startswith("retro: kept in") and report.name in ln for ln in out),
                  f"{new} {out}")
            board = json.loads((w.state / "STATUS.json").read_text(encoding="utf-8"))
            check(f"{label}: the board neither counts nor lists the batches' records",
                  board.get("merged_total") == merged_before
                  and not any("batches" in str(r.get("path")) for r in board.get("merged", [])),
                  str(board.get("merged_total")))
            w.env.pop("CHANTIER_BATCH", None)
            w.reset()
            _, item2 = prepare_cr(w, f"After {label}")
            w.start(str(item2), *FROM_AGENTS_MD)
            check(f"{label}: the next CR gets the next number",
                  w.batch()["crs"][0]["id"] == f"CR-{number + 1}",
                  f"{w.batch()['crs'][0]['id']} after CR-{number}")
            previous = w.name  # opened, never closed: the last closed stays the one before
            previous = json.loads((archives / "batches" / f"{previous}.json").read_text())["batch"]
            previous = report.stem
        else:
            check(f"{label}: batch-NN.md says `No retro was written.`, and nothing is created in "
                  "5-archives",
                  "No retro was written." in body and not new and not retro.exists()
                  and "retro: no retro" in out, f"{new} {out}")
        w.env.pop("CHANTIER_BATCH", None)
    w.reset()
    code, _ = w.chantier("status", expect=2)
    check("with no running batch, `status` refuses and names the last closed batch",
          code == 2 and f"; last closed: {previous}" in w.last_stderr, w.last_stderr)


def next_number(w: World) -> None:
    note("\n## 14e. The next number is read from the records")
    keep = w.root / "changes-keep-number"
    shutil.move(str(w.state), str(keep))
    try:
        w.chantier("init")
        (w.state / "5-archives" / "batches").mkdir(parents=True)
        (w.state / "5-archives" / "batches" / "batch-03.json").write_text("{}\n")
        (w.state / ".batch-number").write_text("1\n")
        _, item = prepare_cr(w, "Number from the records")
        w.start(str(item), *FROM_AGENTS_MD)
        check("with `batch-03.json` in the records and `.batch-number` at 1, `open` makes batch-04",
              w.name == "batch-04"
              and (w.state / "5-archives" / "batches" / "batch-04.json").is_file()
              and (w.state / ".batch-number").read_text().strip() == "4", w.name)
    finally:
        shutil.rmtree(w.state, ignore_errors=True)
        shutil.move(str(keep), str(w.state))
        subprocess.run(["git", "worktree", "prune"], cwd=w.work, capture_output=True)


def plant_archive(stage: Path, name: str, status: dict) -> Path:
    folder = stage / name
    folder.mkdir(parents=True)
    (folder / "STATUS.json").write_text(json.dumps(status), encoding="utf-8")
    return folder


def backfill_cases(w: World) -> None:
    note("\n## 14g. The records of the earlier batches are written once, from the archives")
    keep = w.root / "changes-keep-backfill"
    shutil.move(str(w.state), str(keep))
    try:
        w.chantier("init")
        merged = {"state": "merged", "pr": {"url": "https://example.test/pull/1"}, "round": 2,
                  "cost_usd": 1.5, "cost_unpriced": {}}
        plant_archive(w.state / "5-archives", "261101-1000-101-first",
                      {**merged, "cr": "CR-101", "title": "First", "batch": "01-eval-real",
                       "steps": [{"at": "2026-11-01T09:00:00Z"}]})
        third = plant_archive(w.state / "5-archives", "261103-1000-110-third",
                              {**merged, "cr": "CR-110", "title": "Third", "batch": "batch-03"})
        (third / "retro.md").write_text("# Retro of 3\n", encoding="utf-8")
        plant_archive(w.state / "6-trash", "261103-1100-111-dropped",
                      {"cr": "CR-111", "title": "Dropped", "batch": "batch-03",
                       "state": "cancelled", "round": 0})
        (w.state / ".batch-number").write_text("4\n")
        records = w.state / "5-archives" / "batches"
        code, _ = w.chantier("status", expect=2)
        first_stderr = w.last_stderr
        read = {n: json.loads((records / f"batch-0{n}.json").read_text(encoding="utf-8"))
                for n in (1, 2, 3, 4) if (records / f"batch-0{n}.json").is_file()}
        check("the first command writes batch-01 to batch-04, the unknown ones named as such",
              sorted(read) == [1, 2, 3, 4] and read[2]["state"] == "unknown"
              and read[4]["state"] == "unknown" and read[1]["state"] == "closed"
              and read[3]["state"] == "closed" and not (records / "batch-05.json").exists(),
              str(sorted(read)))
        check("batch-01 keeps its former id; batch-03 lists one merged and one dropped CR",
              read[1]["backfill"]["former_id"] == "01-eval-real"
              and read[1]["backfill"]["first_step"] == "2026-11-01T09:00:00Z"
              and read[3]["backfill"]["former_id"] is None
              and sorted(c["result"] for c in read[3]["crs"]) == ["dropped", "merged"]
              and read[3]["opened"] is None and read[3]["cost_usd"] is None
              and read[3]["report"] == "batch-03.md" and read[2]["report"] is None,
              str(read[3]))
        retro = "5-archives/261103-1000-110-third/retro.md"
        text = (records / "batch-03.md").read_text(encoding="utf-8")
        check("batch-03's retro is listed, linked from its Markdown, and still in place",
              read[3]["backfill"]["retros"] == [retro] and retro in text
              and (w.state / retro).is_file()
              and "No trace of this batch" in (records / "batch-02.md").read_text(encoding="utf-8")
              and not (records / "batch-04.md").read_text(encoding="utf-8").count("Completion"),
              text)
        check("the stderr line says it once",
              first_stderr.count("backfilled 5-archives/batches: batch-01 to batch-04") == 1
              and "(2 with no trace)" in first_stderr, first_stderr)
        snap = tree_bytes(records)
        w.chantier("status", expect=2)
        check("a second command writes nothing and says nothing",
              tree_bytes(records) == snap and "backfilled" not in w.last_stderr, w.last_stderr)
    finally:
        shutil.rmtree(w.state, ignore_errors=True)
        shutil.move(str(keep), str(w.state))
        subprocess.run(["git", "worktree", "prune"], cwd=w.work, capture_output=True)
