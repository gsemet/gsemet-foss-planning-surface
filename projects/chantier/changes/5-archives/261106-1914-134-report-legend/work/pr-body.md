## What

The Progress report in `skills/chantier/references/chief-of-staff.md` now tells a CR that waits
from a CR that is blocked:

- a legend line of the icons opens the table;
- six icons, each with its word: ⚪ not started, 🟡 working, 🟠 waiting, 🔵 to review, 🔴 blocked,
  ✅ merged;
- 🟠 is a CR that waits for a thing already on its way, named: the stack driver, another CR, a slot;
  🔴 is a CR that nothing moves until someone decides or repairs it;
- rows with one cause get the same words, whatever each Driver wrote;
- under the table, when a CR is 🟠 or 🔴, a short explanation: what it waits for, who unblocks it.

The Chief of Staff judges 🟠 or 🔴 from the `blocked` text and the batch's state; the record does not
change. The Status bullet follows: "A blocked CR is a question for the user" becomes "A 🔴 CR".

## Out of scope

`status.py`, `hooks/register.tsx`, `3-requests/STATUS.md` and the board keep their icons.

## Evidence

From `git diff origin/main...af519c1`, which touches this one file (12 insertions, 5 deletions):

| | Before (`42a1cbd`) | After (`af519c1`) |
| --- | --- | --- |
| Icons | ⚪ waiting, 🟡 working, 🔵 to review, 🔴 blocked, ✅ merged | ⚪ not started, 🟡 working, 🟠 waiting, 🔵 to review, 🔴 blocked, ✅ merged |
| Waiting and blocked | no distinction | 🟠 waits for a thing already on its way, named: the stack driver, another CR, a slot; 🔴 nothing moves until someone decides or repairs it |
| Who judges | not said | "You judge 🟠 or 🔴 from the `blocked` text and the batch's state" |
| Legend | none | "a legend line of the six icons, each with its word, which opens the table" |
| One cause | not said | "rows with one cause get the same words, whatever each Driver wrote" |
| Explanation | none | "under the table, when a CR is 🟠 or 🔴, a short explanation: what it waits for, and who unblocks it" |
| Status bullet | "A blocked CR is a question for the user" | "A 🔴 CR is a question for the user" |

Checks at `af519c1`:

- long gate `just check && just scenario`, local on Windows: 28 tests passed; the scenario passed
  255/255 on the GitHub forge and 255/255 on the GitLab forge;
- CI: `just check` passes on Linux, macOS and Windows, `just scenario` on Linux, none skipped.
