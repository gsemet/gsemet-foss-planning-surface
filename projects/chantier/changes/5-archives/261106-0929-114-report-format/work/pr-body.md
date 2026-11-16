The Chief of Staff reports a batch with the same two tables and a current spend.

- `chief-of-staff.md`: a "Reports" item with the Progress and Completion shapes, the icons and the
  forge's word; `$CHANTIER status --refresh`, with no epoch, before a report.
- `SKILL.md`: the "status?" row follows.
- `status.py`: `STATUS.md` takes its word from the recorded links: `/merge_requests/` gives "MR",
  any other link "PR", no link yet "PR/MR". It still never reads the forge; the CLI's help and the
  JSON keys stay as they are.
- `README.md`: the Chief of Staff's own session is priced apart, no longer "not counted" (false
  since CR-113).

`concepts.md` and `routing.md` were read and do not contradict this.

`just check` and `just scenario` pass (204/204 checks on each of github and gitlab).
