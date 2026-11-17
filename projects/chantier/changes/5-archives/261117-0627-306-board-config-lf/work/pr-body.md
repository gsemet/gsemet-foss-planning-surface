## Summary

The board's Configuration page is meant to write the planning surface's project file as UTF-8 with LF line endings. When the existing file had CRLF endings, a save turned the whole file back to CRLF. A save now writes LF only, whatever the file had.

## Deliverables

The write step no longer re-applies CRLF (`playbook/edit_text.py`):

```python
def file_bytes(text: str, old: bytes | None) -> bytes:
    """The text in UTF-8 with LF line endings only, and with the file's byte-order mark if it had one."""
    return (BOM if old is not None and old.startswith(BOM) else b"") + text.encode("utf-8")
```

Before: a CRLF file saved from the page stayed CRLF. After: the saved bytes hold no `\r`, the edited key is changed and the comments and order are kept. The only caller of this write step is the Configuration page's save, so the CRLF branch is removed rather than kept for another caller. The backlog's Markdown editor, which keeps a file's CRLF, is a separate path and is unchanged.

## Blast radius

Grade: 1. Local to one function with one caller; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The CRLF branch is removed outright, since the Configuration page is the function's only caller.
- A leading byte-order mark is still kept when the file had one, as before: the change is about line endings only.

## Known gaps

None

<details>
<summary>Details</summary>

## Changes

- `playbook/edit_text.py`: `file_bytes` writes the text with LF only; module and function docstrings updated.
- `tests/test_playbook_edit.py`: a parametrized test (with and without a byte-order mark) saves through the page's write path onto a CRLF file, reads back no `\r`, the edited key changed and the comment kept, then saves again with the returned hash, which the next save accepts: the returned hash is that of the bytes on disk.

## Impacts

No visual change. A project file that had CRLF endings becomes LF at the next save from the page.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `d15df0b`: `just check` (369 passed)
- [x] Evidence: no visual change; the test above is the evidence
- [x] Review: approved at `d15df0b` (reviewed before the commit at `51a3c8e` plus the change)
- [x] Verified at `d15df0b`
- [x] CI green at `d15df0b`: all five jobs, including `just scenario (ubuntu-latest)`

## Internal references

CR-306 board-config-lf (specification `03-change-spec.md`; its path named `lifecycle/` wrongly, the code is in `playbook/edit_text.py`).

</details>
