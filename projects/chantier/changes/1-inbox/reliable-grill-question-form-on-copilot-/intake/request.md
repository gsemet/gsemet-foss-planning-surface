# Reliable grill question form on Copilot (ask_user)

Make the grill's question form reliable on Copilot (`ask_user`): text first, a short form, and a recovery when the text is not seen.

Observed 2026-11-23 in an okf-schema grill (CoS session, Copilot, chantier 0.15.1), the user's statements:

- The text before the tool call was missing or unreadable several times: "reformatte ton intro et question", then "je ne vois pas ta reformulation", then "il n'y a pas le détail ci-dessus", then "écris-moi avant l'appel du tool c'est illisible". When the same text was posted as a plain message of its own, ending the turn, the user read it, and then asked for the tool call ("et maintenant appelle le tool").
- Too much text was put in the tool's `message` field (the whole question text copied into it), and at other times none at all before the call: "plusieurs fois tu as mis trop de texte dans l'appel de l'outil, des fois pas de texte du tout avant".
- A first call was refused by the tool: a property without `"type": "string"` ("Invalid input: requestedSchema.properties.scope"). Every property needs its `type`.
- The user answered a question by asking for a clarification ("je ne comprends pas la difference entre A et C"), and a reformulation sent only through the tool's `message` was not seen. The reformulation must come as text first, as any series.

What `hosts/copilot.md` ("Ask the user a series of questions") says today: "the host's question tool ... The tool's exact name and whether it has its own free answer are not recorded here", unproved. Record what this session proved:

- The tool is `ask_user`: a `message` string and a `requestedSchema.properties` object, one property per question, each with `type: "string"`, `title`, `enum` (the options) and `default` (the recommended option). The user can type a free answer instead of picking an option (seen on Q2, Q7, Q11, Q14 of this grill): it is the tool's "Other".
- The fields shown to the user, and whether the text written before a call in the same turn is shown: to be found by a trial, then recorded. If the text before a call is not reliably seen on Copilot, the card says what to do (for example, end the turn with the text, and call the tool when the user says so, or put the questions in the tool's `message`).

What to change in the cards (chief-of-staff.md "Backlog and grill", the Griller card, `hosts/copilot.md`):

1. `hosts/copilot.md`: the row above, with the tool's name, its shape, the `type: "string"` rule, the free answer, and the result of the trial on where the preceding text appears.
2. The general rule says "the form is the short mirror of the text": add the limit for the tool's `message`: one line (the series and the references, e.g. "acceptance-paths, series 3: Q11, Q12, Q13"), never the options or the context; the form's titles start with the reference, the options start with the same words as the text.
3. A user's answer that asks for an explanation or a reformulation is handled as a new text-first message (the text, then the tool for that one question), never a tool call alone.
4. A check before each call: the text for this very call was written in this turn, with every reference of the form in it. A call whose references are not in the text just before it is not made.

Out of scope: the other hosts' question tools (Claude Code's `AskUserQuestion` row stays as it is), a change of the series format itself.
