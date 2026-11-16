import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rep import rep

os.chdir(sys.argv[1])
S = "docs/cr-folder-lifecycle.svg"
T = "docs/cr-folder-lifecycle-texts.md"
for f in (S, T):
    rep(f, "03-change-spec.md the spec. chantier triage",
        "03-change-spec.md the spec; they are written with you by the Chief of Staff, or by a Griller (optional, another session of yours). chantier triage")
rep(S, "  <!-- Drop to trash -->",
    '  <!-- Griller note: who writes the planning files -->\n'
    '  <rect x="500" y="392" width="224" height="52" rx="9" fill="#fef9c3" stroke="#ca8a04" stroke-width="1.5" stroke-dasharray="5 3"/>\n'
    '  <g font-size="12" fill="#475569"><text x="510" y="408">written with you by</text><text x="510" y="422">🤵 the Chief of Staff, or a</text><text x="510" y="436">🔥 Griller (optional)</text></g>\n'
    "  <!-- Drop to trash -->")
rep(T, "## Trash (bottom)",
    "## Note under the 1-inbox and 2-backlog folders\n\n```md\nwritten with you by\n🤵 the Chief of Staff, or a\n🔥 Griller (optional)\n```\n\n## Trash (bottom)")
print("ok")
