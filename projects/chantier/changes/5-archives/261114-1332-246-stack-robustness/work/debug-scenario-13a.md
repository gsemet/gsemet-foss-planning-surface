# Debug: just scenario red at 7c2859d (CR-246)
Only 1 of 714 checks fails (section 13a, stack_cli): "`stack` with no CR prints the lines `take stack` printed ...".
Cause: scenario/run_scenario.py:3566-3570 asserts `again == out`, but commands/delivery.py:152 (stack, read-only)
returns [*stack_lines, context_line(...)] while `take stack` (commands/driver.py:78-79) returns [head, *reopened, *rows]
with no context line. The failing output shows the extra last line "context: not measured (no steering transcript recorded)".
Both the delivery.py line and the check were added in 7c2859d (CR-246), not CR-244's base.
Fix: either compare `again[:-1] == out` and check again[-1].startswith("context:") in the scenario, or drop context_line from stack (if the spec says it prints the same lines). Also check the card/spec for which is intended.
