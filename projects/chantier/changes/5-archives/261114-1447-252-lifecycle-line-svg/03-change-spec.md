# Change Specification: lifecycle-line, a CR's life in one line of steps

## Goal

The user (2026-11-14): "Je pense qu'il faut un autre SVG sur le lifecycle sans (on en a un avec les
états / dossier) mais un plus simple avec juste : Intent -> grill -> spec -> spec critic -> driver
-> verifier -... -> PR prête à merger".

Today both lifecycle diagrams of the README (`docs/cr-lifecycle-simple.svg`, `docs/cr-lifecycle.svg`)
draw the folders (`1-inbox/` … `5-archives/`), the lanes and the loops. A reader who opens the
README's CR lifecycle section first wants the plain sequence: what happens to a request, in order,
and who acts at each step. This CR adds one new diagram that shows only that: one line of steps,
from the intent to your merge, with one small line under each step naming who acts. It changes no
behaviour: docs only.

## Decisions carried (`02-answers.md`)

| # | Decision | Where in this spec |
| --- | --- | --- |
| 1 | Where it goes: at the head of README.md's CR lifecycle section, just before `cr-lifecycle-simple.svg`, which stays for the details. Rejected: replacing `cr-lifecycle-simple.svg` in the README; docs only | Area 3 |
| 2 | The steps: Intent → Grill → Spec → Spec critic → Driver (Coder · Inspector · gate · CI, small under its box) → Verifier → … → ready to merge → you merge. Rejected: the user's words only | Area 1, "The steps" |
| 3 | Who acts: one small line under each step naming who does it, with the icons the other diagrams use. Rejected: the steps alone | Area 1, "The steps" and "Legend" |
| 4 | The PR's states: the three states of CR-248 as the line's last steps, 🟣 ready locally → 🟤 PR in draft → ready to merge (they fill decision 2's "…"); its 🔵 replaced by 🟢 per decision 10. Rejected: only the ready-to-merge state at the end | Area 1, "The steps" |
| 5 | Grilled enough; P2; no spec critic (a docs diagram that changes no behaviour); added to batch-17 after spec-critic and CR-248 | "Order in batch-17" |
| 6 | The spec critic's icon: 🧐, used by no other role; spec-critic adopts it too. Rejected: 🔍 | Area 1, "Legend" and "The steps"; "Order in batch-17" |
| 7 | 🟣 ready locally: drawn dashed with a second line "rare: no PR yet", in its place in the line. Rejected: a solid box like the other states | Area 1, "The steps" |
| 8 | Exact place in the README: just before `cr-lifecycle-simple.svg`, after the paragraph that follows the section's heading. Rejected: directly under the heading | Area 3 |
| 9 | The user's decision points: not drawn, the line stays minimal; `cr-lifecycle-simple.svg` just below shows the four points. Rejected: "you approve" under Spec and a "go" step | Area 1, "Not drawn" |
| 10 | Follows from CR-248's ready-wording-Q12: the line's last state is 🟢 ready to merge, in a green box, as everywhere else; 🔵 marks no state any more | Area 1, "The steps" and notes; Evidence |

## What changes

Three files: one new SVG, its new `-texts.md` companion, and README.md. No CLI, card, hook, agent
file, test or CI change; no version edit.

### Area 1: `docs/cr-lifecycle-line.svg` (new)

**Style:** match the existing diagrams, notably `docs/cr-lifecycle-simple.svg`:

- the same root element pattern: `xmlns`, a `viewBox` with matching `width`/`height`, and
  `font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji,
  Noto Color Emoji"`;
- a `<title>` and a `<desc>` (the `<desc>` says the whole diagram in prose, for screen readers,
  as the other diagrams do);
- background `#f8fafc`; title 30px bold `#0f172a`; subtitle 16px `#475569`; legend line 13.5px
  `#334155`; boxes `rx="12"`, white fill, stroke `#64748b` width 2; step titles 17px bold
  `#0f172a` centred; small lines 13.5px (never under 12.5px) `#475569`; the arrow marker `#arrow`
  (`#334155`) between steps;
- a step that does not always run is drawn as the optional boxes are (`stroke="#94a3b8"`,
  `stroke-dasharray="6 4"`).

**Header:**

- Title: `🔄 Life of a change request, in one line`
- Subtitle: `From your request to your merge, step by step, and who acts at each step.`

**Legend** (one line, in the form of `cr-lifecycle-simple.svg`'s line 18):
`👤 you · 🤵 Chief of Staff · 🔥 Griller (optional) · ✍️ spec-writer · 🧐 spec critic · 🚜 driver ·
🔨 worker · 🧱 stack driver` (🧐 for the spec critic: decision 6).

**The steps**, left to right in one row, joined by arrows, each box with its title and, under it,
one small line naming who acts. Exactly these ten, in this order:

| # | Title | Small line (who acts) | Box |
| --- | --- | --- | --- |
| 1 | `Intent` | `👤 you` | plain |
| 2 | `Grill` | `🤵 or 🔥, with 👤 you` | plain |
| 3 | `Spec` | `✍️ spec-writer` | plain |
| 4 | `Spec critic` | `🧐 spec critic` and a second small line `when impactful` | dashed (does not always run) |
| 5 | `Driver` | `🚜 CR driver`, and inside the box, smaller, `🔨 Coder · 📏 Inspector · gate · 🧪 CI` | plain, wider to hold its small line |
| 6 | `Verifier` | `✅ Verifier` | plain |
| 7 | `🟣 Ready locally` | `🚜 hands back` and a second small line `rare: no PR yet` | violet, dashed (fill `#f5f3ff`, stroke `#7c3aed`, `stroke-dasharray="6 4"`; decision 7) |
| 8 | `🟤 PR in draft` | `🚜 opens the PR` | brown (fill `#fdf8f6`, stroke `#92400e`) |
| 9 | `🟢 Ready to merge` | `🚜 or 🧱, out of draft` | green (fill `#f0fdf4`, stroke `#16a34a`; decision 10) |
| 10 | `👤 you merge` | `the PR/MR` | green, as `cr-lifecycle-simple.svg`'s merge box (fill `#f0fdf4`, stroke `#16a34a`) |

Notes on the steps:

- **Spec critic, dashed and "when impactful":** this follows from the spec-critic item's answers
  (`2-backlog/P1/spec-critic/02-answers.md`, decisions 1 and 5): the critic runs only on the CRs
  the one who grills judges impactful, and the user can ask for it or cancel it. The diagram draws
  the target (the diagrams in `docs/` are what chantier should be), so the step is drawn even
  though spec-critic may still be in flight; this CR runs after it in batch-17 (decision 5). Its
  icon is 🧐 (decision 6), which spec-critic adopts too; if spec-critic's merged text names the
  agent otherwise ("critic", "spec critic"), the Driver uses that name here and in the legend.
- **🟣 Ready locally, dashed and "rare: no PR yet":** in today's flow (CR-248, decision 9) the PR
  opens before the long gate, so a CR is almost never ready locally; the box keeps its place in the
  line (decision 7) and says so.
- **The three states' words and icons** are CR-248's exactly (`4-batch/1-pending/248-ready-wording/03-change-spec.md`,
  "Goal", "Words used below" and decisions 6, 8, 10, 12 to 14): **ready locally** 🟣, **PR in
  draft** 🟤, **ready to merge** 🟢 (decision 10). As box titles their first letter is capitalised;
  no other wording ("ready" alone, "mergeable") appears in the diagram, and no 🔵 anywhere in it.
- **Two green boxes side by side:** step 9 (🟢 Ready to merge) and step 10 (👤 you merge) share
  the green of `cr-lifecycle-simple.svg`'s merge box: the "go" light, then the merge. Their titles
  and icons tell them apart; the Driver adds no other colour.
- **Who acts on the states** comes from CR-248: the Driver hands back (`handback <cr> ready`), the
  Driver opens its PR as a draft and records it (`ship --draft`), a PR leaves draft by the Driver
  on the default branch or by the stack driver for a stack (`stack --out-of-draft`).
- **Capitalisation and icons of the actors** are those of the other diagrams: 🔨 Coder, 📏
  Inspector, 🧪 CI, ✅ Verifier (`cr-lifecycle-simple.svg`, `cr-lifecycle.svg`); `gate` has no
  icon, as in `cr-lifecycle-simple.svg`'s `rebase · gate · ship`.
- **Size:** one row, no wrap (the user asked for one line). The `viewBox` width is the Driver's
  choice (wider than 1040 if needed); every text stays legible on GitHub's README render (no text
  under 12.5px in the SVG's own units at the chosen width, and the image not so wide that GitHub's
  scaling makes it smaller than that on a 1000-pixel column; the Driver checks it on the PR's
  rendered README).

**Not drawn:** no folders (`1-inbox/` … `6-trash/`), no stages or states of the record (`queued`,
`working`, `blocked`…), no lanes or phase bands, no loops (no red "new round", no findings back
to the intake), no triage branches, no backlog or batch, no Investigator, QA driver or Release
driver, no CLI commands, and none of your decision points beyond what the who-lines say (no
"👤 you approve" under Spec, no "go" step: decision 9). Those stay in `cr-lifecycle-simple.svg` and `cr-lifecycle.svg`.

### Area 2: `docs/cr-lifecycle-line-texts.md` (new)

The companion every diagram of `docs/` has (`cr-lifecycle-simple-texts.md` is the model): a `#`
title equal to the SVG's `<title>` (`Life of a change request, in one line`), a first paragraph
equal to the SVG's `<desc>`, then `## Header`, `## Legend` and `## Steps` sections, each text of
the SVG in a fenced `md` block, in the order drawn. Every text of the SVG is in it and nothing
else; the two stay in line.

### Area 3: `README.md`

In the section `## Change Requests Lifecycle` (today line 115), insert the new image just before
`cr-lifecycle-simple.svg`, after the paragraph that follows the heading (decision 8): between the
line "Chantier turns each request into a folder in the planning folder, …" (today line 124) and
`![docs/cr-lifecycle-simple.svg](docs/cr-lifecycle-simple.svg)` (today line 126), as its own
paragraph:

```md
![A change request's life in one line: who acts at each step](docs/cr-lifecycle-line.svg)
```

`![docs/cr-lifecycle-simple.svg](docs/cr-lifecycle-simple.svg)` stays right after it,
unchanged, as do the rest of the section, `cr-folder-lifecycle.svg` and the "Detailed
lifecycle" section. No other README text changes.

## Out of scope

- Changing `cr-lifecycle-simple.svg`, `cr-lifecycle.svg` or any other diagram (CR-248 and
  spec-critic change those for their own words and step).
- Placing the diagram anywhere else than the README (docs pages, the tour, the tutorial).
- Any behaviour: the Spec critic step, the three states and who acts are drawn as spec-critic and
  CR-248 define them; this CR decides none of them.
- A check that each SVG has its `-texts.md` (none exists today; not asked).

## Order in batch-17

After spec-critic (`2-backlog/P1/spec-critic`, which draws the critic in the existing diagrams)
and CR-248 (`4-batch/1-pending/248-ready-wording`, which gives the three states' words), per
decision 5, and written against their merged text: the critic's name and icon as spec-critic
leaves it (its icon 🧐 in any case, decision 6), the states' words and icons as CR-248 leaves them. They share no file with this CR
(this CR only adds two files and one README line, near but not on the lines CR-248 may edit), so
no `depends.json`; its place after them is enough.

## Evidence

**Checks:** `just check` passes (Linux, macOS, Windows). No scenario: a change to the docs alone
needs none (`AGENTS.md`). No `just mod` (no `hooks/` or `types/` change).

**In the PR's Test plan:**

1. `docs/cr-lifecycle-line.svg` parses as XML (`uv run python -c "import xml.etree.ElementTree as
   E; E.parse('docs/cr-lifecycle-line.svg')"`), and its `viewBox` matches its `width`/`height`.
2. The ten steps are there, in the order of Area 1, each with its small line; the Spec critic box
   is dashed and says `🧐 spec critic` and `when impactful`; the three states read `🟣 Ready locally`, `🟤 PR in draft`,
   `🟢 Ready to merge` (its box green, fill `#f0fdf4`, stroke `#16a34a`), and `rg -n "🔵"
   docs/cr-lifecycle-line.svg docs/cr-lifecycle-line-texts.md` finds none; in the `<text>` elements, `ready` appears only in the
   two state titles `Ready locally` and `Ready to merge` (and the `<desc>` uses the same three
   words), `mergeable` nowhere; no folder name (`rg -n "inbox/|backlog/|batch/|done/|archives/|trash/" docs/cr-lifecycle-line.svg` finds none).
3. Every `<text>` of the SVG appears in `docs/cr-lifecycle-line-texts.md`, and its title and first
   paragraph equal the SVG's `<title>` and `<desc>` (checked by eye or with a one-off script, not
   committed).
4. README.md shows the new image in `## Change Requests Lifecycle`, after the paragraphs under the
   heading and directly before `cr-lifecycle-simple.svg`, which is unchanged.
5. The 🟣 box is dashed and says `rare: no PR yet`; the legend and step 4 use 🧐; no "you approve"
   or "go" text.

**In the PR's Deliverables:** a link to the README as rendered on the PR's head branch on the
forge (the diagram as a reader sees it, legible in one row), and a link to the SVG file itself.

No CI job is added or changed.

## Self-containment for the Driver

Files: create `docs/cr-lifecycle-line.svg` and `docs/cr-lifecycle-line-texts.md`; edit
`README.md` (one image line in `## Change Requests Lifecycle`). Read, for the style:
`docs/cr-lifecycle-simple.svg` and `docs/cr-lifecycle-simple-texts.md`; for the words:
CR-248's specification and spec-critic's folder (above), as merged below this CR. Repository text
in English.
