Short name: `foreman-idle`

# Answers

1. foreman-idle-Q1 (2026-11-21, asked without its reference, before the reload; recorded as given): **Shape.** The user chose "Mesurer puis couper (Recommandé)": one CR that measures what one Foreman turn reads and costs, then removes the idle wakes (the watcher wakes it on an event).
2. foreman-idle-Q2 (2026-11-21): **Target.** A. The Foreman's share under 15 % of a batch's spend.
3. foreman-idle-Q3 (2026-11-21): **Safety net.** A. A slow heartbeat (about 20 minutes) when nothing arrives; the rest on events.
4. foreman-idle-Q4 (2026-11-21): **Proof.** Open. The user doubts the target is reachable by cutting idle wakes: "Je doute qu'on arrive à ça en réduisant l'idle. C'est sans doute inhérent au système. Demande à un sous agent fable ce qu'il en pense en se basant sur les sessions des 10 derniers jours." A Fable subagent studies the Foreman sessions of the last 10 days (2026-11-11 to 2026-11-21); its findings go to `experiments/foreman-cost-study.md` in this folder.
5. foreman-idle-Q5 (2026-11-21, after the Fable study's verdict): **Revised target.** Set aside: "Met de cote ca va pas, tu peux pas donner des chiffres comme ça. Il faut une étude structurelle d'abord". No figure is set until a structural study of the Foreman's cost exists; foreman-idle-Q2's 15 % no longer holds as a target.
6. foreman-idle-Q6 (2026-11-21): **The Foreman's model.** "Le foreman est déjà en sonnet". The study's claim that batches 28 and 29 ran an Opus Foreman is to be checked against the configuration and the transcripts before it is used.
7. foreman-idle-Q7 (2026-11-21): **Levers in this CR.** Set aside: "Met de côté on retravaille ça plus tard".
8. foreman-idle-Q8 (2026-11-21): **Proof.** A. The next batch's retro repeats the study's measure (the same wake classification) and compares it with batch-29: dollars per CR, calls per wake, and no event left unanswered.

Status (2026-11-21): the grill is paused on the user's word; the CR is reworked later, after a structural study.

Check of foreman-idle-Q6 (2026-11-21, the Chief of Staff): the Foreman transcripts of batch-28 (872ef130) and batch-29 (bc951dfe) carry only `claude-opus-5-5` (1578 and 2455 records), while batch-26 and batch-27's (993a179a, 62abbcd1) carry `claude-sonnet-5-5`. hosts/claude-code.md asks for `model: "claude-sonnet-5-5"` at the Foreman's start, so the last two Foremans ran Opus against the rule. Told to the user.
9. (2026-11-21, the user's words on the retro's point 1, orchestration cost): "Mesure bien mais on décide après". Measure carefully first; decide afterwards. The CR stays paused.
