R = "C:/Users/gaeta/Projets/chantier.worktrees/batch-18-CR-294/"


def edit(path, pairs):
    raw = open(R + path, "rb").read().decode("utf-8")
    crlf = "\r\n" in raw
    s = raw.replace("\r\n", "\n")
    for a, b in pairs:
        assert a in s, (path, a[:60])
        s = s.replace(a, b, 1)
    open(R + path, "wb").write((s.replace("\n", "\r\n") if crlf else s).encode("utf-8"))


edit("skills/chantier/references/chief-of-staff.md", [
    (
        """an order is open, a stack agent is recorded, or a session file of the Foreman or of any of its
  agents was written in the last 5 minutes (on Copilot, the session's file time; `not measured`
  refuses too). It refuses too,""",
        """an order is open, a stack agent is recorded, an agent of the Foreman, or the Foreman itself,
  has a transcript that shows it still runs (a tool call with no result, or a step under way: the
  CLI reads the end of each transcript, never the file's age), or a transcript cannot be read
  (missing, cut or undecodable; on Copilot, a session file written in the last 5 minutes, and
  `not measured` refuses too). It refuses too,""",
    ),
    (
        """Report a refusal to the user with its cause, do not retry in
  a loop, and do not `close --yes`; a Driver""",
        """Report a refusal to the user with its cause, do not retry in
  a loop, and do not `close --yes`. When the refusal names an agent that still runs, wait for that
  agent's hand-back (its notification), then run `close` again, never on a timer. When you know
  the agent will not hand back, or the user says so, ask the user: ways to know are an app restart
  that cut it, the user's stop, or its hand-back that already reached you while its transcript
  reads as running. In the question quote each agent's name, cause and file, as the refusal gives
  them; ask the agent itself only as a last resort (a finished subagent cannot be messaged). On
  the user's yes, in that turn, run `close --batch <batch> --stopped <name> ...` (the check; the
  name is the subagent's file stem, `agent-<id>`, or an earlier Foreman's session id), show the
  bilan with its "declared stopped" lines and ask for the close as above; on that second yes run
  `close --batch <batch> --stopped <name> ... --yes`. Never pass `--stopped` without the user's
  yes for each named agent, and never to get past a transcript that cannot be read: the CLI
  refuses a name that is not a running agent of the batch, and keeps the declaration in the
  batch's record. A Driver""",
    ),
    (
        """  `$CHANTIER cancel`."
- **Putting back:**""",
        """  `$CHANTIER cancel`." The old Foreman's session and its Drivers stay in the batch's
  transcripts and read as running at `close`: that is the case for `close --stopped`, on the
  user's yes.
- **Putting back:**""",
    ),
])

edit("skills/chantier/references/concepts.md", [
    (
        """a stack agent, or a session file of the
  Foreman or of any of its agents (on a direct batch, of the Chief of Staff's own transcript: its subagents only) written in the last 5 minutes (on Copilot the session file's
  time; `not measured` refuses).""",
        """a stack agent, an agent of the
  Foreman, or the Foreman itself, whose transcript shows it still runs (a tool call with no
  result, or a step under way; on a direct batch the Chief of Staff's own transcript is not
  read, its subagents are), or a transcript that cannot be read (on Copilot, a session file
  written in the last 5 minutes; `not measured` refuses). The CLI reads the end of each
  transcript, never the file's age. An agent that stopped without its hand-back passes only on
  the user's word (`close --stopped <name>`), recorded in the batch's record.""",
    ),
])

edit("docs/planning-folder.md", [
    (
        "a session\nwritten in the last 5 minutes)",
        "an agent whose\ntranscript shows it still runs; one that stopped without handing back passes on your word, and\nthe batch's record keeps it)",
    ),
])

edit("scenario/README.md", [
    (
        """- closing on the user's word: `close` refusing, with and without `--yes`, a CR not merged, an
  open order, a stack agent, and a session file (any agent's, a Copilot one's, or one whose
  time is not measured) written in the last 5 minutes; a pricing failure and a missing
  Foreman transcript refused the same way;""",
        """- closing on the user's word: `close` refusing, with and without `--yes`, a CR not merged, an
  open order, a stack agent, a Foreman whose last call waits on a tool (its file aged 10
  minutes), an agent whose last record is a tool's result, an agent whose last line is cut
  JSON, a missing Foreman transcript, and a Copilot session file written in the last 5 minutes
  or whose time is not measured; passing an agent that handed back or ended its turn though
  its file was just written; `--stopped` passing a running agent on its stem or its bare id
  (writing nothing without `--yes`), refused for an unknown name, an ended agent or a
  transcript that cannot be read, and never past another running agent or a record cause; a
  pricing failure refused the same way; the declaration kept in the record
  (`stopped_agents`), under Cost in `batch-NN.md` and in what `close --yes` prints, and absent
  from a record closed without the flag;""",
    ),
])

edit("docs/tutorial-claude-code.md", [
    (
        "which refuses while anything\nstill runs or nothing at all can be priced (it names the cause)",
        "which refuses while anything\nstill runs (an agent stopped without handing back passes on your word) or nothing at all can be priced (it names the cause)",
    ),
])

edit("docs/use-cases-foreman.md", [
    (
        "an agent of the batch still runs, or nothing at all",
        "an agent of the batch still runs (one stopped without handing back passes on your word), or nothing at all",
    ),
])
