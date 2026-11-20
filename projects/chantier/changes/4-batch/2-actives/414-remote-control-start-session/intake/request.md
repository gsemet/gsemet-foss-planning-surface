# Sessions start from Remote Control when no other folder is named

# Sessions start from Remote Control when no other folder is named

The user's request, relayed by the Studio Chief of Staff (2026-11-20): "tu peux encoder ca dans les
instructions specifique a Claude Code, comment faire en sorte que la creation de sous session
fonctionne toujours même depuis remote".

## The trial (2026-11-20, Battlestation, Studio's Chief of Staff on Remote Control)

The session ran in the Studio's main checkout, with the planning surface as an added directory.

- `start_session` (user_asked, fresh, `use_worktree: false`) WITH `cwd` = the planning surface:
  refused twice ("The user is working over Remote Control, and this turn can't start that
  session, so nothing was started").
- The same call with NO `cwd` (the session's own folder) started every time:
  - two Grillers;
  - then the batch-07 Foreman (model claude-sonnet-5-5, effort medium). It landed on the Studio
    main checkout, passed its worktree check, claimed the batch, wrote to the planning surface by
    absolute paths and started a Driver.

## Asked

- `skills/chantier/references/hosts/claude-code.md`: fix the "Classes of session" row ("Desktop,
  driven by Remote Control: Can start a session: no") and the Surfaces table's `start_session`
  refusal. What Remote Control refuses is a start in another folder (`cwd`).
- Encode the rule: from Remote Control, the steering session starts the Foreman and Grillers with
  no `cwd`, in its own folder, which must be a main checkout (no worktree); the planning surface is
  given by absolute paths in the prompt (the CLI's `--project`, the brief's path).
- Check every card and doc that repeats the old rule (the mode choice "direct under Remote
  Control", `planning-modes.md`'s Remote section, the chief-of-staff skill's description) and keep
  them true.
- When merged, tell the Studio Chief of Staff in one line.
