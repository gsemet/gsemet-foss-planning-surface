"""Fill COST-REPORT.template.md with the generated tables and totals.

Usage: python3 -I assemble_cost.py <scratchpad> <template> <out>
"""
import json, re, sys

S, tpl, out = sys.argv[1:4]
tables = open(f"{S}/tables.md").read()
d = json.load(open(f"{S}/cost2.json"))


def section(title):
    m = re.search(r"### " + re.escape(title) + r"\n\n(.*?)(?=\n### |\n<!--|\Z)", tables, re.S)
    return m.group(1).strip()


text = open(tpl).read()
text = text.replace("<!-- TABLE-MODEL -->", section("Tokens and cost by model"))
text = text.replace("<!-- TABLE-WHO -->", section("Who spent it"))
text = text.replace("<!-- TABLE-PHASE -->", "Orchestrator cost by phase (Opus):\n\n" + section("Orchestrator (main session, Opus) by phase"))
text = text.replace("<!-- TABLE-HS -->", section("Haiku and Sonnet implementers, per task"))

PR = {"opus": (4, 8, 0.2, 20), "sonnet": (2, 4, 0.1, 10)}
cw = cr = outp = inp = 0.0
for fam, c in d["by_model"].items():
    if fam == "haiku":
        # Haiku is tiny; split it with its average blended price from cost2 (input side) and output.
        inp_side = c["usd_in"]
        outp += c["usd_out_est"]
        tot_in_tokens = c["cw"] + c["cr"] + c["in"]
        cw += inp_side * c["cw"] * 20 / max(1, c["cw"] * 20 + c["cr"] + c["in"] * 10)
        cr += inp_side - inp_side * c["cw"] * 20 / max(1, c["cw"] * 20 + c["cr"] + c["in"] * 10)
        continue
    pi, pw, pr, po = PR[fam]
    cw += c["cw"] * pw / 1e6
    cr += c["cr"] * pr / 1e6
    inp += c["in"] * pi / 1e6
    outp += c["usd_out_est"]
total = cw + cr + outp + inp
split = (f"cache writes about ${cw:,.0f} ({100 * cw / total:.0f} %), cache reads about ${cr:,.0f} "
         f"({100 * cr / total:.0f} %), generated output about ${outp:,.0f} ({100 * outp / total:.0f} %)")
text = text.replace("<!-- SPLIT -->", split)

main_total = sum(c["usd_in"] + c["usd_out_est"] for c in d["by_model"].values())
side = 5.49 + 0.28 + 1.76
text = text.replace("<!-- GRAND -->", f"about ${main_total + side:,.0f}")
text = text.replace("<!-- NAGENTS -->", str(len(d["agents"])))
firsts = [a["first"] for a in d["agents"] if a["first"]]
text = text.replace("<!-- FIRST -->", "2026-10-08")
text = text.replace("<!-- LAST -->", max(a["last"] for a in d["agents"] if a["last"])[:10])
open(out, "w").write(text)
print(f"total ${main_total:,.2f}; {split}; grand ${main_total + side:,.2f}")
