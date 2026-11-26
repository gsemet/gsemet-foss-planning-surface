from pathlib import Path

from chantier.commands import help as h

W = Path("<worktree>")
base = W / "skills/chantier/cards-next"
print("module under test is the worktree's:", Path(h.__file__).as_posix().startswith(W.as_posix()))
topics = h.load_topics(base / "topics.json")
print("topics loaded:", len(topics))
for host in ("claude", "copilot"):
    errors, empty, total, largest = [], [], 0, (0, "")
    for name, topic in topics.items():
        try:
            out = h._print_topic(topic, host, base)
        except Exception as e:  # report every failure
            errors.append((name, str(e)))
            continue
        body = [x for x in out[1:] if x.strip() and not x.startswith("--- references/")]
        if not body:
            empty.append(name)
        n = len("\n".join(out).encode())
        total += n
        largest = max(largest, (n, name))
    print(f"host {host}: printed {len(topics) - len(errors)}, errors {errors[:5]}, empty {empty[:5]}, "
          f"total bytes {total}, largest {largest[1]} {largest[0]}")
for name, host in (("lost-driver", "claude"), ("refused-push", "claude"), ("host-sessions", "copilot")):
    out = h._print_topic(topics[name], host, base)
    print(f"help {name} ({host}): {len(out)} lines; {out[0][:150]}")
    print("   readings:", [x for x in out if x.startswith("--- references/")])
