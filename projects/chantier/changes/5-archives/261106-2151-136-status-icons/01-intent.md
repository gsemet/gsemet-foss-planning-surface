# Intent

The user reads a CR's state in two places, the Chief of Staff's report and the CR board, and the
icons differ: a CR waiting for a slot is 🟠 in the report and 🟡 on the board. They want one set of
icons everywhere.

The report's icons live in `chief-of-staff.md`. The board, `STATUS.md` and `STATUS.json` take theirs
from `label()` in `status.py`, so the board needs no change of its own.

| State | Report | `status.py` |
| --- | --- | --- |
| queued | ⚪ or 🟠 | 🟡 |
| working | 🟡 | 🟡 |
| blocked | 🔴 or 🟠 | 🔴 |
| ready | 🔵 | 🟢 |
| merged | ✅ | 🟢 |
| dropped | none | ⚪ |

This reverses the "Out of scope" of CR-134, which kept the two sets apart.
