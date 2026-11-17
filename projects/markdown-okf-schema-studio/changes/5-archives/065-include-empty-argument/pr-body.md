## Summary

Typing a new `{include}` directive made the whole preview fail: while the path was still empty,
the render was refused with an error instead of showing the document. The preview now keeps
rendering.

## Deliverable showcase

````markdown
Before.

```{include}
```

After.
````

| | Before | After |
| --- | --- | --- |
| Preview | error, nothing rendered | "Before." and "After." rendered, placeholder `{include}` between them |
| Warning | none | "Directive {include} needs a path." on the directive line |

## Changes

- The directive placeholder rule in `src/core/render/mystNormalize.ts` also handles the error
  node the parser produces for a missing required argument, for `{include}` only.
- The empty-argument requirement row of the include requirement states the new behaviour; the
  Known issue line is removed.

## Impacts

No visual change besides the placeholder and warning shown for an incomplete include.

## Blast radius

Grade: 1. Only an `{include}` without a path is affected; a `git revert` restores the old behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code): the include-forms test now expects
      the placeholder, the rest of the document and the warning line
- [x] Requirements: SwRS updated, markers in code, `okfreq update-coverage` run
- [x] Local gates: `just check` (2594 unit, 2 contract, 44 security tests, 31 Sphinx tests, all
      passing); okfreq validate (1010 requirements, 0 errors), lint and update-coverage `--check`
      clean

## Internal references

- CR 065 (include-empty-argument)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
