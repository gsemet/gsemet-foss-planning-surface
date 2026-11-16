$ uv run -I two.py (calls status._rows_markdown of the worktree module, one call per table)
module: C:\Users\gaeta\Projets\chantier.worktrees\batch-folder-CR-114\skills\chantier\scripts\cli\src\chantier\status.py

## batch-01 (one GitLab merge request, one other link)
| CR | Subject | Status | Branch | MR | Cost |
| --- | --- | --- | --- | --- | ---: |
| [101](s.md) | t | [Working](STATUS.md) | `b101` | [MR](https://gitlab.example.com/a/b/-/merge_requests/7) | - |
| [102](s.md) | t | [Working](STATUS.md) | `b102` | [MR](https://github.com/a/b/pull/8) | - |

## batch-02 (links all other than merge requests)
| CR | Subject | Status | Branch | PR | Cost |
| --- | --- | --- | --- | --- | ---: |
| [201](s.md) | t | [Working](STATUS.md) | `b201` | [PR](https://github.com/a/b/pull/9) | - |
| [202](s.md) | t | [Working](STATUS.md) | `b202` | [PR](https://github.com/a/b/pull/10) | - |

## batch-03 (no link yet)
| CR | Subject | Status | Branch | PR/MR | Cost |
| --- | --- | --- | --- | --- | ---: |
| [301](s.md) | t | [Working](STATUS.md) | `b301` | - | - |

## batch-04 (all GitLab)
| CR | Subject | Status | Branch | MR | Cost |
| --- | --- | --- | --- | --- | ---: |
| [401](s.md) | t | [Working](STATUS.md) | `b401` | [MR](https://gitlab.example.com/a/b/-/merge_requests/1) | - |
