# Trust tier: count the actor forms allowed by OKF 0.2

## Intent

`okf-schema` reads a concept as `unverified`, and warns W10, when its `verified[].by` actor is
written in a form OKF 0.2 allows but without a colon, such as
`reference_agent/gemini-2.5-pro` (spec sections 5.3 and 7: any actor that does not start with
`human:` is machine-confirmed).

The trust tier must count those actors, W10 must accept the specification's forms
(`<producer>/<version>`, `human:<id>`, `process:<id>`), and the documentation and scaffold that
teach another form must be corrected. CR `58-show-as-stored` adds a command printing this tier
and stacks on this fix.
