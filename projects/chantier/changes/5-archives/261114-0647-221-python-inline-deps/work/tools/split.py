"""One-shot mechanical split of the old chantier modules into the new package layout."""
import ast
import io
import subprocess
import sys
import tokenize
from collections import defaultdict
from pathlib import Path

REPO = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-17-CR-221")
PKG = REPO / "skills/chantier/scripts/cli/src/chantier"
OLDFILES = ["state", "commands", "lifecycle", "status", "costs", "playbook", "board",
            "rails", "procs", "forge_stack", "cli"]

# newmod -> list of (oldfile, [names]); "*" is every name not listed elsewhere
MAP = {
    "core/errors": [("state", ["EXIT_USAGE", "ChantierError"])],
    "core/files": [("state", ["If25", "LOCK_TIMEOUT_S", "_try_lock", "_unlock", "_retry", "read_text",
                             "_read_json", "write_file", "write_json", "IGNORED", "_IGNORE_HEAD",
                             "_ignored_done", "ensure_gitignore"])],
    "core/clock": [("state", ["now", "stamp", "age_minutes"])],
    "core/git": [("state", ["git", "default_branch"])],
    "core/records": [("state", ["read_batch_json", "LIVE", "chief_sessions", "round_limit",
                               "read_events", "normalize_batch", "normalize_cr"])],
    "core/repo": [("state", ["CHANGES", "DEFAULT_CONFIG", "SETTINGS", "project_path", "read_keyed",
                            "PROJECT", "surface_projects", "SurfaceChoice", "Repo"])],
    "core/batch": [("state", ["move_directory", "apply_batch_settings", "Batch", "resolve_batch",
                             "check_epoch", "read_batch", "find_cr_batch", "RESTORED_NUMBER_FILE",
                             "next_cr_number"])],
    "core/seat": [("commands", ["_read_seat"])],
    "lifecycle/stages": [("lifecycle", ["PRIORITIES", "STATE_FOLDERS", "stage_layout", "changes_lock",
                                       "PreparedCR", "prepared_cr", "ensure_unclaimed", "cr_directory",
                                       "_relocate", "start_cr", "done_cr", "_delivery", "trash_cr",
                                       "archive_name", "move_backlog_item"])],
    "lifecycle/convert": [("lifecycle", ["*"])],
    "rails": [("rails", ["*"])],
    "procs": [("procs", ["*"])],
    "playbook/models": [("playbook", ["Model", "MODELS", "SETS_MODEL_AT_START", "ESCALATION", "normalise",
                                     "_shown", "resolve", "_contains"])],
    "playbook/yaml_subset": [("playbook", ["YamlError", "Node", "_Token", "_KEY", "_strip_comment",
                                          "_tokens", "_is_item", "_scalar", "_double", "_flow_list",
                                          "_inline", "_block", "_list", "_map", "parse"])],
    "playbook/lines": [("playbook", ["_model_text", "_fields", "playbook_lines", "escalate_line",
                                    "team_lines"])],
    "playbook/config": [("playbook", ["*"])],
    "costs/transcripts": [("costs", ["CACHE_5M", "PRICE", "projects_dir", "transcript_path", "_price",
                                    "_transcript_lines", "_wakes", "_when", "GRILL_NAMES", "WRITE_PATHS",
                                    "_grill_use", "_new_row", "_add", "usage"])],
    "costs/sessions": [("costs", ["_held", "session_costs", "without_spec_writers", "is_spec_writer",
                                 "idle_seconds", "agent_records", "agent_context"])],
    "costs/copilot": [("costs", ["*"])],
    "status/words": [("status", ["ASKING", "ENDED", "step", "forge_word", "severity", "_round", "waits",
                                "_waits_on", "can_start", "icon", "label", "_no_start", "steering_word",
                                "shape_word"])],
    "status/markdown": [("status", ["_step_line", "cr_markdown", "_rows_markdown", "_budget",
                                   "batch_markdown", "dashboard_markdown"])],
    "status/write": [("status", ["_write", "write_batch", "write_final_pages", "write_dashboard"])],
    "status/views": [("status", ["*"])],
    "plugin_files": [("commands", ["HOSTS", "AGENT_VERSION", "INSTRUCTIONS", "skill_dir", "plugin_root",
                                  "cli_command", "detect_host", "project_instructions",
                                  "surface_instructions", "archive_path", "_skill_version",
                                  "_agent_files", "plugin_roles", "read_playbook", "_agent_problems"])],
    "commands/permissions": [("commands", ["_SHA", "_BRANCH", "_TREE", "_SAMPLES", "RECOMMENDED_ALLOW",
                                          "_SETTINGS_SHOWN", "_DROPPED", "_RULE", "_glob", "rule_matches",
                                          "_counts_as_allow", "_settings_rules", "_sample_groups",
                                          "commands_not_allowed"])],
    "commands/preflight": [("commands", ["preflight"])],
    "commands/intake": [("commands", ["init", "file_cr", "triage", "abandon", "restore"])],
    "commands/crs": [("commands", ["_shown", "_slug", "_new_request", "_batch_cr", "_work", "_worktree",
                                  "_cr_events", "same_head", "_short", "_dirty", "gate_passed",
                                  "last_verdict", "grant_line", "filed_fix"])],
    "commands/opening": [("commands", ["add_cr", "cr_slug", "read_depends", "archived_merged",
                                      "declare_dependencies", "check_series_order", "_release_tag",
                                      "release_waits_for_all", "check_cycles", "open_batch"])],
    "commands/seat": [("commands", ["foreman", "_own_transcript", "seat"])],
    "commands/orders": [("commands", ["ORDER_KINDS", "CR_ORDERS", "_cr_arg", "_apply_order", "order",
                                     "_order_done"])],
    "commands/orders_release": [("commands", ["_release_cr", "_refused", "_started", "_add_release",
                                             "_join_release", "_check_release_open"])],
    "commands/batch_status": [("commands", ["_activity", "_stop_heartbeat", "_refresh", "_record_costs",
                                           "status", "asks", "agents"])],
    "commands/facts": [("commands", ["_chain", "_top_cr", "_start_base", "_stack_base", "_ref", "_base_of",
                                    "_stack_ref", "_facts", "handoff", "_stack_lines"])],
    "commands/driver": [("commands", ["_reopen", "_check_release_branch", "take", "round_",
                                     "_context_line", "handback", "note", "log"])],
    "commands/rules": [("commands", ["MD_LINK", "_linked", "playbook", "rules"])],
    "commands/gate_lock": [("commands", ["LONG_GATE_WAIT_S", "_lock_holder", "_LongGateLock"])],
    "commands/gate": [("commands", ["_run_file", "_stop_file", "_stop_asked", "_run_read", "_run_write",
                                   "_gate_stop", "gate"])],
    "commands/delivery": [("commands", ["VERDICTS", "verdict", "_stale_body_shas", "ship", "stack"])],
    "commands/release": [("commands", ["release", "cancel"])],
    "commands/closing": [("commands", ["pause", "_close_target", "_retro_target", "_batch_files", "close",
                                      "_archive_and_delete", "_final_rows", "_final_pages"])],
    "commands/cost/pricing": [("commands", ["TO_DATE", "_prices", "_unpriced", "_add_unpriced",
                                           "_sum_unpriced", "_minus", "_spend", "_hints", "_cost_rows",
                                           "_window"])],
    "commands/cost/sessions": [("commands", ["_claimed", "_foreman_uuid", "OWN_CHIEF", "OWN_FOREMAN",
                                            "STEER_OUT", "GRILL_OUT", "WHOLE", "_chief_unknown",
                                            "_chief_line"])],
    "commands/cost/breakdown": [("commands", ["CR_IN_NAME", "_cost_groups", "_apportion", "COMPACTION_USD",
                                             "_kind", "STEERING", "UNSPLIT", "_label", "_steers",
                                             "_breakdown", "_restarted", "_explain", "EXPIRY_NOTE",
                                             "_cost_summary", "_orchestration"])],
    "commands/cost/command": [("commands", ["cost"])],
    "commands/forge_stack": [("forge_stack", ["*"])],
    "board/collect": [("board", ["DEFAULT_HOST", "EVENTS_SHOWN", "_tail_events", "collect", "settings"])],
    "board/render": [("board", ["REFRESH_S", "_e", "_file_link", "_url_link", "subject", "_money", "_ago",
                               "_details", "_cr_row", "_batch_section", "_item_rows", "_past_rows",
                               "render_body", "project_name", "page", "STYLE"])],
    "board/server": [("board", ["*"])],
}
DOCS = {
    "core/errors": "The error every command raises, and the exit codes it carries.",
    "core/files": "Reading and writing files: atomic writes, the OS locks, the planning folder's .gitignore.",
    "core/clock": "The clock: UTC stamps and ages.",
    "core/git": "Running git, and the remote's default branch.",
    "core/records": "The JSON records chantier keeps (`batch.json`, `events.jsonl`), and the ids of batches and CRs.",
    "core/repo": "The repository and the planning folder: where chantier reads and writes.",
    "core/batch": "The locked, read-modify-write view of the batch's record; every change is one event.",
    "core/seat": "The repository's Chief of Staff seat (`seat.json`).",
    "lifecycle/stages": "The stage folders of a CR and the moves between them.",
    "lifecycle/convert": "The conversion of a planning tree of the old layout, once.",
    "rails": "The refusals: what a command checks before it changes the record.",
    "procs": "Finding and stopping the processes of a worktree.",
    "playbook/models": "The models each role can run and how a name resolves to one.",
    "playbook/yaml_subset": "The subset of YAML that `chantier.yaml` accepts.",
    "playbook/lines": "The playbook, the team and the escalation as printed lines.",
    "playbook/config": "`chantier.yaml`: loading and validating the project's configuration.",
    "costs/transcripts": "A Claude transcript and its prices: tokens, cache writes, wakes.",
    "costs/sessions": "The cost of a batch's sessions and agents, from the transcripts on disk.",
    "costs/copilot": "The cost of a Copilot session, through the `copilot-session-usage` helper.",
    "status/words": "The words and icons of a CR's status.",
    "status/views": "The views of the record: a CR, a batch and the dashboard, as data.",
    "status/markdown": "The Markdown of the STATUS files.",
    "status/write": "Writing the STATUS files and the dashboard.",
    "plugin_files": "The plugin's own files: the skill, the host, the agents, the project's instructions.",
    "commands/permissions": "The allow rules the commands need and the check of a user's settings.",
    "commands/preflight": "`chantier preflight`: the checks before a batch.",
    "commands/intake": "The inbox: `init`, `file`, `triage`, `abandon` and `restore`.",
    "commands/crs": "The facts of a CR that several commands share.",
    "commands/opening": "`chantier open`: the batch's frame, its CRs and their dependencies.",
    "commands/seat": "`chantier foreman` and `chantier seat`.",
    "commands/orders": "`chantier order`: the user's word, recorded at once.",
    "commands/orders_release": "The orders of the release CR and of its fixes.",
    "commands/batch_status": "`chantier status`, `asks` and `agents`.",
    "commands/facts": "The facts of a CR for any agent: `chantier handoff`.",
    "commands/driver": "The Driver's commands: `take`, `round`, `handback`, `note` and `log`.",
    "commands/rules": "`chantier rules` and `chantier playbook`.",
    "commands/gate_lock": "The long gate's lock: first come first served.",
    "commands/gate": "`chantier gate`: the long gate, run alone in the repository.",
    "commands/delivery": "The delivery of a CR: `verdict`, `ship` and `stack`.",
    "commands/release": "`chantier release` and `chantier cancel`.",
    "commands/closing": "`chantier pause` and `chantier close`.",
    "commands/cost/pricing": "The spend of a batch: prices, unpriced calls and the window.",
    "commands/cost/sessions": "The sessions a cost line belongs to.",
    "commands/cost/breakdown": "The breakdown of the cost by role or by CR.",
    "commands/cost/command": "`chantier cost`.",
    "commands/forge_stack": "`chantier forge-stack`: the native stack on the forge.",
    "board/collect": "What the board shows: the data read from the record.",
    "board/render": "What the board draws: the HTML page.",
    "board/server": "The board's HTTP server and its command.",
}
OVERRIDES = {("commands", "_prices"): "price_table", ("board", "_e"): "esc",
             ("commands", "_slug"): "slugify", ("commands", "_worktree"): "cr_worktree",
             ("commands", "_short"): "short_head", ("commands", "_dirty"): "dirty_files",
             ("commands", "_facts"): "cr_facts", ("commands", "_unpriced"): "unpriced_of",
             ("commands", "_window"): "steering_window", ("commands", "_claimed"): "claimed_transcripts",
             ("commands", "_restarted"): "restarted_drivers", ("commands", "_explain"): "explain_line",
             ("commands", "_kind"): "cost_kind", ("commands", "_label"): "cost_label"}
FORCE = {("commands", "_SAMPLES"), ("commands", "_kind"), ("commands", "_label"),
         ("commands", "_breakdown")}


def git_show(old):
    p = subprocess.run(["git", "show", f"HEAD:skills/chantier/scripts/cli/src/chantier/{old}.py"],
                       cwd=REPO, capture_output=True, check=True)
    return p.stdout.decode("utf-8")


class Seg:
    pass


def node_key(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        return n.name, {n.name}
    if isinstance(n, ast.Assign):
        names = []
        for t in n.targets:
            if isinstance(t, ast.Name):
                names.append(t.id)
            elif isinstance(t, ast.Tuple):
                names += [e.id for e in t.elts if isinstance(e, ast.Name)]
        if not names:
            return None, set()
        return names[0], set(names)
    if isinstance(n, ast.AnnAssign):
        return n.target.id, {n.target.id}
    if isinstance(n, ast.If):
        return f"If{n.lineno}", set()
    return None, set()


def load():
    src, segs, imports, stdlib, modalias = {}, {}, {}, {}, {}
    for old in OLDFILES:
        text = git_show(old)
        src[old] = text
        lines = text.split("\n")
        tree = ast.parse(text)
        std = []
        for n in tree.body:
            key, names = node_key(n)
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                if isinstance(n, ast.ImportFrom) and n.level >= 1:
                    for a in n.names:
                        local = a.asname or a.name
                        if n.module is None:
                            if a.name == "__version__":
                                imports[(old, local)] = ("*", "__version__", None)
                            else:
                                modalias[(old, local)] = a.name
                        else:
                            imports[(old, local)] = (n.module, a.name, a.asname)
                elif isinstance(n, ast.ImportFrom) and n.module == "__future__":
                    pass
                else:
                    std.append(ast.get_source_segment(text, n))
                continue
            if key is None:
                continue
            start = min([n.lineno] + [d.lineno for d in getattr(n, "decorator_list", [])])
            while start > 1 and lines[start - 2].lstrip().startswith("#"):
                start -= 1
            s = Seg()
            s.old, s.key, s.names = old, key, names or {key}
            s.start, s.end = start, n.end_lineno
            s.text = "\n".join(lines[start - 1:n.end_lineno])
            segs.setdefault(old, []).append(s)
        stdlib[old] = std
    return src, segs, imports, stdlib, modalias


def main():
    src, segs, imports, stdlib, modalias = load()
    home = {}
    bymod = defaultdict(list)
    assigned = set()
    for newmod, parts in MAP.items():
        for old, names in parts:
            if names != ["*"]:
                for key in names:
                    cand = [s for s in segs[old] if s.key == key]
                    if not cand:
                        sys.exit(f"missing {old}.{key} for {newmod}")
                    assert (old, key) not in assigned, (old, key)
                    assigned.add((old, key))
                    bymod[newmod].append(cand[0])
    for newmod, parts in MAP.items():
        for old, names in parts:
            if names == ["*"]:
                for s in segs[old]:
                    if (old, s.key) not in assigned:
                        assigned.add((old, s.key))
                        bymod[newmod].append(s)
    for old in segs:
        for s in segs[old]:
            if (old, s.key) not in assigned and old != "cli":
                print("UNASSIGNED", old, s.key)
    for newmod, ss in bymod.items():
        ss.sort(key=lambda s: (s.old, s.start))
        for s in ss:
            s.newmod = newmod
            for nm in s.names:
                home[(s.old, nm)] = newmod
    split_old = {old: len({s.newmod for s in segs[old] if hasattr(s, "newmod")}) > 1 for old in segs}

    def resolve(old, name):
        if (old, name) in home:
            return (old, name)
        imp = imports.get((old, name))
        if imp and imp[0] != "*":
            return resolve(imp[0], imp[1]) if imp[0] in segs else None
        return None

    def alias_target(old, alias):
        m = modalias.get((old, alias))
        if m == "playbook" or alias == "pb":
            return "playbook"
        return m

    def tokens_of(text):
        return list(tokenize.generate_tokens(io.StringIO(text).readline))

    def scan(s):
        toks = tokens_of(s.text)
        out = []
        i = 0
        depth = 0
        while i < len(toks):
            t = toks[i]
            if t.type == tokenize.OP and t.string in "([{":
                depth += 1
            elif t.type == tokenize.OP and t.string in ")]}":
                depth -= 1
            if t.type == tokenize.NAME:
                prev = toks[i - 1] if i else None
                nxt = toks[i + 1] if i + 1 < len(toks) else None
                after_dot = prev is not None and prev.type == tokenize.OP and prev.string == "."
                is_kw = nxt is not None and nxt.type == tokenize.OP and nxt.string == "=" and depth > 0
                if not after_dot and not is_kw:
                    tgt = alias_target(s.old, t.string)
                    if (tgt and nxt is not None and nxt.string == "." and i + 2 < len(toks)
                            and toks[i + 2].type == tokenize.NAME and split_old.get(tgt)):
                        out.append(("alias", i, tgt, toks[i + 2].string))
                        i += 3
                        continue
                    if tgt and not split_old.get(tgt):
                        out.append(("modref", i, tgt))
                    else:
                        out.append(("name", i, t.string))
            i += 1
        return toks, out

    scans = {}
    refs = defaultdict(set)
    for ss in bymod.values():
        for s in ss:
            toks, out = scan(s)
            scans[id(s)] = (toks, out)
            for o in out:
                if o[0] == "alias":
                    r = resolve(o[2], o[3])
                elif o[0] == "name":
                    r = resolve(s.old, o[2])
                else:
                    r = None
                if r and home[r] != s.newmod:
                    refs[r].add(s.newmod)
    renames = {}
    for k in FORCE:
        refs[k].add("test")
    for (old, name), users in refs.items():
        if name.startswith("_") and not name.startswith("__"):
            renames[(old, name)] = OVERRIDES.get((old, name), name.lstrip("_"))
    allids = defaultdict(set)
    for old in segs:
        for s in segs[old]:
            for t in tokens_of(s.text):
                if t.type == tokenize.NAME:
                    allids[old].add(t.string)
    for (old, name), new in sorted(renames.items()):
        if new in allids[old] and (old, name) not in OVERRIDES:
            print(f"COLLISION {old}.{name} -> {new}")
    for newmod, ss in bymod.items():
        parts = []
        needs = defaultdict(set)
        modimports = set()
        olds = sorted({s.old for s in ss})
        for s in ss:
            toks, out = scans[id(s)]
            repl = {}
            for o in out:
                if o[0] == "alias":
                    r = resolve(o[2], o[3])
                    if r is None:
                        print("UNRESOLVED alias", s.old, o[2], o[3])
                        continue
                    new = renames.get(r, r[1])
                    repl[o[1]] = (new, 3)
                    if home[r] != newmod:
                        needs[home[r]].add(new)
                elif o[0] == "name":
                    r = resolve(s.old, o[2])
                    if r is None:
                        imp = imports.get((s.old, o[2]))
                        if imp and imp[0] == "*":
                            needs["__root__"].add("__version__")
                        continue
                    new = renames.get(r, r[1])
                    imp = imports.get((s.old, o[2]))
                    aliased = imp is not None and imp[2] is not None and imp[0] != "*"
                    if aliased:
                        if home[r] != newmod:
                            needs[home[r]].add(f"{renames.get(r, r[1])} as {o[2]}")
                        else:
                            repl[o[1]] = (renames.get(r, r[1]), 1)
                    else:
                        if new != o[2]:
                            repl[o[1]] = (new, 1)
                        if home[r] != newmod:
                            needs[home[r]].add(new)
                elif o[0] == "modref":
                    modimports.add(o[2])
            lines = s.text.split("\n")
            edits = []
            for idx, (new, ntok) in repl.items():
                t = toks[idx]
                last = toks[idx + ntok - 1]
                edits.append((t.start, last.end, new))
            for (sl, sc), (el, ec), new in sorted(edits, reverse=True):
                assert sl == el
                ln = lines[sl - 1]
                lines[sl - 1] = ln[:sc] + new + ln[ec:]
            parts.append("\n".join(lines))
        std = []
        for old in olds:
            for line in stdlib[old]:
                if line not in std:
                    std.append(line)
        imp_lines = []
        for mod in sorted(needs):
            names = sorted(needs[mod])
            target = "chantier" if mod == "__root__" else "chantier." + mod.replace("/", ".")
            imp_lines.append(f"from {target} import {', '.join(names)}")
        for m in sorted(modimports):
            imp_lines.append(f"from chantier import {m}")
        body = "\n\n\n".join(parts)
        out = f'"""{DOCS[newmod]}"""\n\nfrom __future__ import annotations\n\n'
        out += "\n".join(std) + "\n" + "\n".join(imp_lines) + "\n\n\n" + body + "\n"
        path = PKG / (newmod + ".py")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(out, encoding="utf-8", newline="\n")
        init = path.parent / "__init__.py"
        if path.parent != PKG and not init.exists():
            init.write_text('"""' + path.parent.name + '"""\n', encoding="utf-8", newline="\n")
    print("renames:", {f"{o}.{n}": v for (o, n), v in sorted(renames.items())})


main()
