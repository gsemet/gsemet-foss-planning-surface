"""Usage: rep.py <root> <edits.py-style module path>. Helper: rep(f, old, new, count=1)."""
import os, sys


def rep(f, old, new, count=1):
    with open(f, encoding="utf-8", newline="") as fh:
        t = fh.read()
    crlf = "\r\n" in t
    if crlf:
        old = old.replace("\r\n", "\n").replace("\n", "\r\n")
        new = new.replace("\r\n", "\n").replace("\n", "\r\n")
    n = t.count(old)
    if n != count:
        raise SystemExit(f"{f}: expected {count} of {old!r}, found {n}")
    with open(f, "w", encoding="utf-8", newline="") as fh:
        fh.write(t.replace(old, new))
