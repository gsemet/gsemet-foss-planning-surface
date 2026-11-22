## Summary

The web board had no place that explains chantier itself. This adds a **Help** page in the sidebar, right after Home (and the Inbox when present): two groups of cards, **Concepts** (12) and **Roles** (13), each a name and one sentence. A click or Enter opens a short detail on the same page, with one "Read more" link to the documentation on GitHub. All text ships in English and French.

## Deliverables

The Help page is one card grid per group; the open card is marked, and its detail opens right after its group:

```text
Help
  Concepts   [card][card][card]...        <- grid, one column on a narrow screen
             [ detail of the open card ]  <- name, text, "Read more", close button
  Roles      [card][card][card]...
```

Choices: the page needs no project data (registry flag `offline`) and calls no server operation; the open topic is the address's `&h=<topic>`; Escape, the close button, a second click or Back closes it, and a close adds no history entry (the router's `closeTopic()`), so Back never reopens a closed detail; cards and detail are the board's own card component, tokens only, no picture.

On a phone the bottom bar holds one more item, so it scrolls sideways when its items no longer fit (`overflow-x: auto`).

Taken at 60aacc1 from the branch's own code, on a demo project with made-up paths:

English, "Batch and slots" open:

![Help page in English at 60aacc1](https://media.githubusercontent.com/media/gsemet/gsemet-foss-planning-surface/6c8621aff1751d5b60edc765b324049021f3955a/projects/chantier/changes/4-batch/2-actives/439-board-help-page/evidence/help-en.png)

French, "Grill et spécification" open:

![Help page in French at 60aacc1](https://media.githubusercontent.com/media/gsemet/gsemet-foss-planning-surface/6c8621aff1751d5b60edc765b324049021f3955a/projects/chantier/changes/4-batch/2-actives/439-board-help-page/evidence/help-fr-detail.png)

"All projects":

![Help page on All projects at 60aacc1](https://media.githubusercontent.com/media/gsemet/gsemet-foss-planning-surface/6c8621aff1751d5b60edc765b324049021f3955a/projects/chantier/changes/4-batch/2-actives/439-board-help-page/evidence/help-all-projects.png)

360 px wide, the bottom bar scrolled to its end, Configuration reachable:

![Help page at 360 px at 60aacc1](https://media.githubusercontent.com/media/gsemet/gsemet-foss-planning-surface/6c8621aff1751d5b60edc765b324049021f3955a/projects/chantier/changes/4-batch/2-actives/439-board-help-page/evidence/help-360.png)

## Blast radius

The change is in the web client only (a new view, a router and store field, one sheet); revert restores the board.

Grade: 1

## Autonomous decisions

- `test_code_targets.py`'s origin check now accepts the documentation links of `help-topics.js` (`https://github.com/gsemet/chantier`), which the topics' links need.

## Known gaps

- This branch sits on CR-435's title-row commits (PR #408, the Batch page's mode and legend in the title row), still open: the PR's file list therefore also holds `batch-head.js`, `batch.js`, `batch.css`, `batch-nav.css`, `docs/web-board.md` and its pictures, `test_board_title_row.py`. Those are #408's; they leave this diff once #408 merges.

<details>
<summary>Details</summary>

## Changes

- New `js/views/help.js`, `help-topics.js`, `i18n/en-help.js`, `i18n/fr-help.js`, `css/views/help.css`.
- `registry.js` entry `help` (`offline`, no count); `host.js` draws an `offline` view with no project data; `header.js` shows a view's own title except on "All projects" Home; new `help` icon; `nav.help` words.
- `router.js`: `&h=` topic, `topicOf`, `closeTopic()`, history state for an open detail; `store.js` `helpTopic`; `main.js` Escape closes the detail.
- `shell.css`: the phone's bottom bar scrolls sideways (`overflow-x: auto`, items do not shrink).
- `card.css` hover for Help cards; `DESIGN.md` section "The Help page".

## Human decisions

- Help sits in the sidebar right after Home (and the Inbox), the same on every project and on "All projects", with no count.
- 12 concept cards and 13 role cards, each a name and one sentence; a click opens a detail of at most about 150 words on the same page, one at a time.
- A close (Escape, close button, second click) adds no history entry: Back after a close leaves Help.
- The text follows the README and the documentation it links; it ships in English and French, with chantier's own names kept in English.
- The page needs no project data and calls no server operation.

## Impacts

A new Help entry in the sidebar and bottom bar; nothing else changes visibly.

## Test plan

- [ ] New test `test_the_help_page_is_a_view_with_both_languages_and_real_links` (registry, topics, word counts, links and anchors, router and `help.js` rules)
- [x] Local gates at 60aacc1: `just check`, `just eval-dry-run`
- [x] Evidence: four screenshots at 60aacc1 (Deliverables)
- [x] Review: approved at cf99450 (rebase with a conflict resolved); the rebase onto main to 60aacc1 had no conflict
- [ ] Verified at 60aacc1
- [x] CI green at 60aacc1: check x3, eval-dry-run, scenario (ubuntu)

## Internal references

CR-439 help (batch-30).

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
