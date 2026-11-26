import collections
import sys

import inv

for name in inv.NAMES:
    rs = [d for _, d in inv.rows(name)]
    a = [d for d in rs if d["kind"].startswith("a")]
    print(name, "rows", len(rs), "a", len(a), "header", list(rs[0]))
    homes = collections.Counter(d["new home"] for d in a)
    print("  distinct a homes:", len(homes))
