# Answers: tracker-import

## 2026-11-20, after the outside poller's spec (CR-410)

Q1. CR-410 sets the rule that chantier never reads a tracker itself: an outside program of the
user's reads it and writes into chantier. So this item becomes that program: it reads the tracker
(GitHub/GitLab open issues, maybe a label; Jira by JQL) and files each ticket with `chantier file`;
chantier would only refuse a ticket whose link is already filed. What do we do with it?

The user: "Re-griller après 29". Keep it in P4; re-grill it on the outside-poller model once
CR-410 has merged (batch-29): chantier refuses a ticket already filed, the program stays the
user's (an example in the docs). No grill before then.
