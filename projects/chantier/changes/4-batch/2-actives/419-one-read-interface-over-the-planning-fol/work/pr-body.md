## Summary

The board, the forge hub and `chantier status` each read the planning folder (the Markdown and JSON files that hold the plan) directly with `pathlib` and `os`. That makes it hard to put an index (SQLite, Dolt) behind the plan later. This PR gives the plan's store (`PlanStore`) its read half and moves those readers onto it, so there is one way to read the plan. No index is built and no behaviour or output changes.

## Deliverables

The store gains nine reads, checked by the same guard as a write; the modules listed in a new structure test read the planning folder only through it.

```python
class PlanStore(Protocol):
    def read_text(self, rel: str, errors: str = "strict") -> str: ...
    def read_bytes(self, rel: str, limit: int | None = None) -> bytes: ...
    def exists(self, rel: str) -> bool: ...
    def is_file(self, rel: str) -> bool: ...
    def is_dir(self, rel: str) -> bool: ...
    def listdir(self, rel: str) -> list[str]: ...
    def glob(self, rel: str, pattern: str) -> list[str]: ...
    def stat(self, rel: str) -> tuple[int, int] | None: ...   # size, mtime_ns
    def walk(self, rel: str) -> Iterator[tuple[str, list[str], list[str]]]: ...
```

```mermaid
flowchart LR
  board --> store
  hub --> store
  status --> store
  records["record readers (core/records, seat, waits, batch_records, summaries)"] --> store
  repo["core/repo, surface_batches"] --> store
  store --> files[(planning folder)]
```

| | before (CR-418 at `58df3be`) | after (head) |
| --- | --- | --- |
| `chantier status`, median of 5 | 0.585 s | 0.590 s (+1 %) |
| one board state, median of 5 | 0.833 s | 0.891 s (+7 %) |
| `status` text and board state JSON | - | identical |

Measured on a prepared planning folder with 240 backlog items, same machine, back to back.

## Blast radius

Grade: **2**. Many modules of `board/`, `hub/`, `status/` and `core/` change how they read; the files on disk and every printed output stay the same. Revert restores the previous readers.

## Autonomous decisions

- The record readers take the store first and keep their path argument (`read_batch_json(store, path)`), computing the store-relative name with a new `rel_in` helper: callers and printed paths stay as they are.
- A read resolves the store's root once and checks each component below it with `lstat` (a symlink or junction goes to the full guard); a board state opens a scope (`PlanStore.reading()`) in which an already-checked component is not checked again, because resolving root and path on each of about 5,700 reads made a board state three times slower on Windows. The scope ends with the call; no file content or listing is kept, only the link check of a folder, for one pass. Writes keep the full guard.
- `tests/test_code_targets.py` ignores `if TYPE_CHECKING:` imports, as the type-only import of the store in `core/` would otherwise count as a cycle.

## Known gaps

- A link swapped into an already-checked folder during one board-state pass is not seen until the pass ends (writes are unaffected).
- `status`'s file count of a CR folder no longer enters a symlinked folder on Python before 3.13 (it did, through `rglob`).
- Work-note order in `status` is by name with a plain sort: notes that differ only by case may order differently on Windows.
- The modules outside the list (`lifecycle/`, `core/batch.py`, `gate_queue.py`, the rest of `summaries/`, `commands/`, configuration files) still read directly; the run-time proof that the board, `status` and the hub open nothing outside the store is left for a follow-up.

<details>
<summary>Details</summary>

## Changes

- `store/base.py`, `store/folder.py`: the nine reads; `core/files.py`: `rel_in`.
- `board/`, `hub/`, `status/`, `core/repo.py`, `core/surface_batches.py`: reads go through the store; kept direct reads are marked `# direct:` with their reason.
- `core/records.py`, `core/seat.py`, `core/waits.py`, `core/batch_records.py`, `summaries/`: readers take the store; callers in `commands/`, `lifecycle/`, `core/` updated.
- `tests/test_store_reads.py` (new): static check, with a prepared source that must fail it; `tests/test_store_conformance.py` extended on both backends.
- `CONTRIBUTING.md`: one sentence for the rule.

## Impacts

No visual change; developers read the planning folder through `Repo.store`.

## Test plan

- [x] New or changed tests (conformance and structure tests fail on the previous code)
- [x] Local gates at `b3fbfa3`: `just check` (its suite, 1493 passed), `just eval-dry-run` (18 of 18); `just test` added no measurable time when measured before the restack: 72.5 s at the old base, 72.6 s at the head, same machine, back to back (24 more tests)
- [x] Evidence: speed and golden-output comparison, before at CR-418 `58df3be`, re-measured at the restacked head
- [x] Review: approved on the same code before the restack; the restack's caller fixes approved by the inspector (commit `3e22340d`, rebased as `868761b`) and the head `b3fbfa3` differs only by an import-order line
- [x] Verified at `b3fbfa3`
- [x] CI green at `b3fbfa3` (check on three systems, eval-dry-run, scenario)

## Internal references

CR-419 the plan's store reads the planning folder (stacked on CR-418).

</details>
