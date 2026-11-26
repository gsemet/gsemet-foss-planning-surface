"""Round 9, run once: replace the topic rows of the sibling-card edits table.

Run: python -I siblings_rows.py <host-and-shared inventory>
Keeps the file's line endings. Rows given here replace the row of the same topic file, or of
the split file the old name became; new rows are added; the topic rows are sorted by name.
"""

import pathlib
import re
import sys

NEW = [
    ("batch-close-p1.md:3", "`close` does not judge a running critic, so the offer follows it", "review"),
    ("batch-close-p2.md:3, 4", "at a batch's end it is said to stay open while a CR is held; `status`'s second line names the last closed batch", "review"),
    ("batch-plan-cut-p1.md:3, 4", "`batch-plan-cut.md` split in two: the night example, a chain cut after any CR, where the rest stays, the user chooses, the floor said with no time given, when `depends.json` is written and what a CR without it depends on", "review"),
    ("batch-plan-cut-p2.md:3, 4", "the second part: which specifications are read, why waiting helps, a shared file alone no reason, the reason per queued CR, no threshold, the limits in both steering modes, then the go", "review"),
    ("batch-plan-mode-p1.md:1, 3", "three parts now; the question is asked at every opening, `--mode` as answered, `parallel` only the CLI's default", "review"),
    ("batch-plan-mode-p2.md:1, 3, 4, 5", "the three modes; the invocation's word and how a forced mode holds; the no-argument rule; the plan's line and the forced `foreman` moved to part 3 (no separate yes for the mode, `batch-plan-mode-p3.md`)", "review"),
    ("config-p1.md:1, 3", "three parts now; nothing else is configured, the layers' merge and `default`, the keys, `ci.beside_gate` and `hosts.<host>.timing` among them, and when a change counts", "review"),
    ("config-p2.md:1, 3, 4", "the roles by name, the four ways a role starts; the rest moved to part 3", "review"),
    ("delivery-time-p2.md:3, 6", "which CI runs time the floor, the unreadable causes, the floor line's example", "review"),
    ("drop.md:4", "the draft turn comes before the order's `order done`", "review"),
    ("forge-permissions-p1.md:3, 4, 5, 6, 8", "`forge-permissions.md` split in two: what P9 checks and when, a CLI not logged in still fails P9, the scopes, the permissions and the branch rules in full", "review"),
    ("forge-permissions-p2.md:3, 4", "the second part: the stacks API and the default branch's rules and merge methods in full", "review"),
    ("grill-critic-steps.md:6, 7", "review again after the fixes; the full list comes from the critic's reply, written nowhere", "review"),
    ("main-checkout-p1.md:3", "`main-checkout.md` split in two: on by default, the last merge's attempt, the order of the other steps unchanged", "review"),
    ("main-checkout-p2.md:3, 4, 6, 8, 9", "the second part: the steps in full; only the Chief of Staff syncs", "review"),
    ("merge-recorded.md:5, 6", "a parallel batch's merge order; a GitLab fold keeps its precedence over the forge check", "review"),
    ("merge-series-stack-p1.md:5", "a series keeps its order; when the next CR and a CR with a dependency start", "review"),
    ("mode-switch-p1.md:3, 5, 7, 8", "`mode-switch.md` split in two: the switch is on the user's word, the record's new order, what the stack driver does", "review"),
    ("mode-switch-p2.md:3, 4, 5, 6", "the second part: the switches out of a stack in full; the release redo closes its PR and keeps its branch", "review"),
    ("project-rules-p1.md:3, 5, 6", "`project-rules.md` split in two: the preflight message, a missing tool said with what to install, nothing blocks the request; the no-long-gate and brief lines moved here", "review"),
    ("project-rules-p2.md:3, 4", "the second part: the long gate proposed and written on the user's yes, in full", "review"),
    ("refused-push-chief-p2.md:3", "a protected-branch rejection is handled as a failed lease and told as information, with git's text and what it means, never retried", "review"),
    ("steering-reports-p2.md:4", "the stack check before a Progress report holds in direct mode too", "review"),
    ("ticket-summary-p1.md:7", "the demo file is not the batch's demo", "review"),
    ("wakes.md:3, 4, 5, 6, 7", "a stopped batch sends nothing more, then says it stopped; no long command in a turn; the rest reworded so they fit", "review; trim"),
    ("watcher-events.md:6", "a `specifying.parallel` or role-key line takes no tool call", "review"),
]


def key(cell):
    name = cell.split("/", 1)[1].split(":", 1)[0]
    return name


def main():
    path = pathlib.Path(sys.argv[1])
    text = path.read_bytes().decode("utf-8")
    end = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(end)
    start = lines.index("## Sibling-card edits")
    stop = lines.index("## Behaviour changes on purpose")
    rows = [i for i in range(start, stop) if lines[i].startswith("| topics/")]
    assert rows == list(range(rows[0], rows[-1] + 1)), "topic rows are not contiguous"
    old = {key(lines[i].split("|")[1].strip()): lines[i] for i in rows}
    for stale in ("forge-permissions.md", "main-checkout.md", "project-rules.md"):
        assert stale in old, stale
        del old[stale]
    for place, what, why in NEW:
        cell = f"topics/{place}"
        old[key(cell)] = f"| {cell} | {what} | {why} |"
    lines[rows[0] : rows[-1] + 1] = [old[name] for name in sorted(old)]
    for i, line in enumerate(lines):
        if line.startswith("| topics.json | this CR's"):
            before = "the `paths` text names the reading forms"
            assert before in line
            lines[i] = line.replace(
                before,
                before
                + "; the split topics list their parts; `ready-asks` serves the Foreman and the Chief of Staff",
            )
    path.write_bytes(end.join(lines).encode("utf-8"))
    print(len(rows), "rows before,", len(old), "after")


if __name__ == "__main__":
    main()
