"""One-time freeze of the six real use cases into test/site/requirementsViewer/metroShapes.ts (run from the worktree root)."""
import glob, json, re, sys

SHAPES = ["BLOCK-003", "FMSCHEMA-014", "BLOCK-014", "MYST-006", "REVIEW-012", "MYST-009"]
ID = re.compile(r"SwRS-MDOKFSTUDIO-[A-Z]+-\d+")


def read(path):
    return open(path, encoding="utf-8", newline="").read().replace("\r\n", "\n")


def front(text, key):
    m = re.search(r"^" + key + r": (.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def tested(text):
    m = re.search(r"^tested_in_files:\n((?:- .*\n)*)", text, re.M)
    return len(m.group(1).splitlines()) if m else 0


def find(req_id):
    return glob.glob("requirements/tiers/*/*/" + req_id + ".md")[0]


out = []
swrs = {}
for short in SHAPES:
    sid = "StRS-MDOKFSTUDIO-" + short
    text = read(find(sid))
    start = text.index("### Main paths")
    rest = text[start:]
    end = re.search(r"\n(?:#{1,3} |<!--)", rest[5:])
    section = rest[: end.start() + 5] if end else rest
    section = section.rstrip("\n") + "\n"
    scope = find(sid).replace("\\", "/").split("/")[-2]
    out.append((sid, scope, section))
    for cited in dict.fromkeys(ID.findall(section)):
        if cited in swrs:
            continue
        body = read(find(cited))
        kinds = re.findall(r"^### Scenario \((\w+)\)", body, re.M)
        swrs[cited] = (find(cited).replace("\\", "/").split("/")[-2], kinds, tested(body))

lines = [
    "/**",
    " * Six real use cases of the requirements bundle, frozen at the head of CR-441 (the Main paths sections as they were",
    " * then, and every SwRS they cite with its scenario kinds and its number of test files), so the map checks keep the",
    " * shapes they were designed on: one path with three other outcomes, a path that splits early, three paths of which two",
    " * join and one stands alone, a short one, long captions, and a path that splits mid-way.",
    " */",
    'import { requirement } from "./fixture";',
    "",
    "interface FrozenUseCase {",
    "  readonly id: string;",
    "  readonly scope: string;",
    "  readonly mainPaths: string;",
    "}",
    "",
    "/** The use cases, in the order of the shapes above. */",
    "export const FROZEN_USE_CASES: readonly FrozenUseCase[] = [",
]
for sid, scope, section in out:
    lines.append("  {")
    lines.append("    id: %s," % json.dumps(sid))
    lines.append("    scope: %s," % json.dumps(scope))
    lines.append("    mainPaths: %s," % json.dumps(section, ensure_ascii=False))
    lines.append("  },")
lines += [
    "];",
    "",
    "/** The SwRS the use cases cite: scope, scenario kinds and number of test files at the freeze. */",
    "const FROZEN_BEHAVIOURS: Readonly<Record<string, { readonly scope: string; readonly kinds: readonly string[]; readonly tests: number }>> = {",
]
for k, (scope, kinds, n) in swrs.items():
    lines.append("  %s: { scope: %s, kinds: %s, tests: %d }," % (json.dumps(k), json.dumps(scope), json.dumps(kinds), n))
lines += [
    "};",
    "",
    "const scenarioText = (kind: string, index: number): string => `### Scenario (${kind}): Frozen ${index + 1}\\n\\n- GIVEN a box\\n- WHEN it is used\\n- THEN it works\\n\\n`;",
    "",
    "/** A requirements report of the frozen use cases and behaviours, in the shape of `fixtureReport`. */",
    "export function frozenReport(): string {",
    "  const requirements: unknown[] = FROZEN_USE_CASES.map((useCase) => requirement(useCase.id, \"StRS\", useCase.scope, {",
    "    text: `## Frozen\\n\\n${useCase.mainPaths}\\n<!-- okf:links:start -->\\n`,",
    "  }));",
    "  for (const [id, behaviour] of Object.entries(FROZEN_BEHAVIOURS)) {",
    "    const parents = FROZEN_USE_CASES.filter((useCase) => useCase.mainPaths.includes(id)).map((useCase) => useCase.id);",
    "    requirements.push(requirement(id, \"SwRS\", behaviour.scope, {",
    "      derivesFrom: parents,",
    "      text: behaviour.kinds.map(scenarioText).join(\"\"),",
    "      testedIn: Array.from({ length: behaviour.tests }, (_, index) => `test/frozen/${id}-${index + 1}.test.ts`),",
    "    }));",
    "  }",
    "  return JSON.stringify({ generated_at: \"2026-11-21T10:00:00+00:00\", totals: { combined_coverage_percent: 100 }, scopes: {}, requirements });",
    "}",
    "",
]
open("test/site/requirementsViewer/metroShapes.ts", "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print(len(swrs), "behaviours")
