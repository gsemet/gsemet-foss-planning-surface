# retro batch-28: hold a ready CR out of the stack

From batch-28's retro (2026-11-19), kept by the retro critic.

The user asked to keep CR-381 (Read the Docs) and CR-382 out of the forge stack, to merge them a
week later (order O-25). `stack <order>` and `forge-stack rebuild` cannot leave out a CR handed
back ready: CRs not named go on top. The rebuild put #346 and #347 on top of the new forge stack
#355 (against O-26), the record still lists them above the top, and the Foreman had to ask (A-39);
the user then merged up to #354 and left the two drafts on top.

Long-term fix: a way to hold a ready CR out of the stack order (for example `order hold <cr>` or
`stack --out <cr>`), so the stack driver's rebuild, the record and the forge stack leave it apart
until the user puts it back.
