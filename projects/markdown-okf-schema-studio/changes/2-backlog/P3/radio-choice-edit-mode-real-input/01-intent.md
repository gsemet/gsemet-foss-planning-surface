# Radio choices: real-input coverage in edit mode

The real-input radio test (`test/integration/radioChoice.test.ts`) runs its "Tab from the label",
arrow, Space and Enter steps in reading mode. In edit mode a click on the label paragraph opens its
block editor, so the step was moved to reading mode (heavy CI diagnosis, 2026-10-31).

Radio choices are meant to work in both modes. Add real-input coverage for the same steps in edit mode:
reach the label without opening an editor (or start from the option), then Tab, arrows, Space and Enter,
and check focus and writes as in reading mode.

Uncheck to disagree: [x]
