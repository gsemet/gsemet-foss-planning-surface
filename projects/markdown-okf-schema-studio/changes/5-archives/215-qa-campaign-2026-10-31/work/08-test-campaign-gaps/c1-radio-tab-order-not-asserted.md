# The radio E2E never walks the Tab order

`test/integration/radioChoice.test.ts` moves focus with `radioAt(...).focus()`, so tab entry, Shift+Tab and extra stops (finding 215-c1-1) are not asserted. Add a one-Tab assertion from the label paragraph. Source: charter C1, replay `scenarios/215-c1-1-radio-tab-entry-extra-stops.json`.

Uncheck to disagree: [x]
