import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rep import rep

os.chdir(sys.argv[1])
S = "docs/cr-lifecycle.svg"
T = "docs/cr-lifecycle-texts.md"

# desc / paragraph, both files
for f in (S, T):
    rep(f, "The Chief of Staff triages it with you:", "The Chief of Staff, or a Griller (optional, another session of yours), triages it with you:")
    rep(f, "start the spec-writer agent in the background,", "start the spec-writer agent, which the Chief of Staff or a Griller starts, in the background,")
    rep(f, "or grill you and record your answers", "or grill you (a Griller may too) and record your answers")

# legend
L = [
    ('<rect x="386" y="103" width="22" height="16" rx="4" fill="#ea580c"/><text x="416" y="116">',
     '<rect x="386" y="103" width="22" height="16" rx="4" fill="#fef9c3" stroke="#ca8a04" stroke-width="1.5" stroke-dasharray="4 3"/><text x="416" y="116">🔥 Griller (optional)</text>\n    <rect x="576" y="103" width="22" height="16" rx="4" fill="#ea580c"/><text x="606" y="116">'),
    ('<rect x="736" y="103" width="22" height="16" rx="4" fill="#ffffff" stroke="#ea580c" stroke-width="2"/><text x="766" y="116">',
     '<rect x="946" y="103" width="22" height="16" rx="4" fill="#ffffff" stroke="#ea580c" stroke-width="2"/><text x="976" y="116">'),
    ('<rect x="871" y="103" width="22" height="16" rx="4" fill="#e0e7ff"/><text x="901" y="116">',
     '<rect x="1060" y="103" width="22" height="16" rx="4" fill="#e0e7ff"/><text x="1090" y="116">'),
    ('<rect x="1096" y="103" width="22" height="16" rx="4" fill="#0f172a"/><text x="1126" y="116">',
     '<rect x="1285" y="103" width="22" height="16" rx="4" fill="#0f172a"/><text x="1315" y="116">'),
    ('<rect x="1271" y="103" width="22" height="16" rx="4" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/><text x="1301" y="116">',
     '<rect x="1440" y="103" width="22" height="16" rx="4" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/><text x="1470" y="116">'),
    ('<rect x="1461" y="103" width="22" height="16" rx="4" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5"/><text x="1491" y="116">',
     '<rect x="1610" y="103" width="22" height="16" rx="4" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5"/><text x="1640" y="116">'),
]
for a, b in L:
    rep(S, a, b)
rep(T, "🤵 Chief of Staff\n👷 Foreman (🤵", "🤵 Chief of Staff\n🔥 Griller (optional)\n👷 Foreman (🤵")

# triage diamond
rep(S, '<text x="690" y="288" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">⚖️ Triage</text>\n  <text x="690" y="308" font-size="13" fill="#475569" text-anchor="middle">with you</text>',
    '<text x="690" y="280" font-size="15" font-weight="700" fill="#0f172a" text-anchor="middle">⚖️ Triage</text>\n  <text x="690" y="299" font-size="13" fill="#475569" text-anchor="middle">🤵 or 🔥</text>\n  <text x="690" y="317" font-size="13" fill="#475569" text-anchor="middle">with you</text>')
rep(T, "## ⚖️ Triage\n\nwith you", "## ⚖️ Triage\n\n🤵 or 🔥\nwith you")

# spec loop and clarification
rep(S, '<text x="985" y="313" font-size="11.5" fill="#1e3a8a" text-anchor="middle">🤵 starts it on your word</text>',
    '<text x="985" y="313" font-size="11" fill="#1e3a8a" text-anchor="middle">🤵 or 🔥 starts it on your word</text>')
rep(T, "🤵 starts it on your word", "🤵 or 🔥 starts it on your word")
rep(S, ">🤵 grills you</text>", ">🤵 or 🔥 grills you</text>")
rep(T, "## 🤵 grills you", "## 🤵 or 🔥 grills you")

# note in the planning lane
rep(S, "  <!-- Planning pills -->",
    '  <!-- Griller note -->\n'
    '  <rect x="300" y="396" width="256" height="62" rx="10" fill="#fef9c3" stroke="#ca8a04" stroke-width="1.5" stroke-dasharray="5 3"/>\n'
    '  <text x="314" y="416" font-size="14" font-weight="700" fill="#0f172a">🔥 Griller, optional</text>\n'
    '  <text x="314" y="434" font-size="12" fill="#475569">another session of yours,</text>\n'
    '  <text x="314" y="449" font-size="12" fill="#475569">same planning, never a batch</text>\n\n'
    "  <!-- Planning pills -->")
rep(T, "## Triage branches (blue pills)",
    "## Griller (optional note in the planning lane)\n\n```md\n## 🔥 Griller, optional\n\nanother session of yours,\nsame planning, never a batch\n```\n\n## Triage branches (blue pills)")
print("ok")
