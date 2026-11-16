# Proposal: improve skill boot

Date: 2026-11-16.

This is the saved interview proposal, not an implementation plan, an approved
batch or a claim that the behavior below is already available.

Sources: [request and observations](01-request.md) and
[complete interview decisions](02-interview-responses.md).

## Shared understanding

Chantier startup should establish the role, project, indispensable prerequisites,
permissions and available host capabilities without loading procedures that are
not yet needed. The proposal covers every Chantier role and host, not only Chief
of Staff startup under the Copilot SDK.

The CLI remains mandatory. Startup effects follow distinct rules rather than
one blanket confirmation requirement. A short report must distinguish measured
results, documented capabilities, server announcements and untested paths.

## Scope and boundaries

In scope:

- Initial startup and the handling of existing session state on re-invocation.
- Common role rules and host-specific startup capabilities.
- Deferred reference loading before an action.
- Official CLI preparation, seat acquisition, board launch and autosync joining.
- Startup evidence and reporting.

Not authorized by this handoff:

- Implementation or changing the installed skill.
- Starting a batch, assigning priority or opening a PR.
- Stopping or changing services already running during the interview.
- Changing ordinary batch go, merge, release or publication permissions.

The user chose this directory in the code repository as the handoff destination,
despite the current session using an external planning surface.

## 1. Short mandatory core

Every role has a short mandatory startup core. The combined mandatory Chantier
documentation for that role must not exceed **12 KiB (12,288 bytes)**, including
common and host-specific references.

Project rules and command output are excluded from this limit. Exclusion from
the size limit does not exempt project rules from being read or followed.

Bulk loading later batch, release and other action-specific procedures is
replaced by explicit deferred loading. This is a reduction in required startup
material, not merely a different way to paginate the same full references.

An action-to-required-readings table states what must be loaded before each
action. An inaccessible indispensable reference blocks the action that requires
it. The selected mechanism is an explicit reading contract, not CLI tracking of
claimed comprehension.

## 2. Shared contract and host capability evidence

Keep a common contract with a capability/evidence reference for each host.
Generic startup rules and host-specific mode selection must not contradict one
another.

Distinguish at least these facts in claims to the user:

- A tool is available.
- A behavior is documented.
- A command or end-to-end path was actually exercised.
- A server announces a binding or capability.
- A capability or check was not tested or could not be established.

Examples from the observed session:

- Loading session tools is not proof of a successful Foreman launch.
- A local HTTP success does not prove access from another machine.
- A skipped validation is not a successful validation of the skipped content.
- A failed authentication check is not proof of its underlying root cause.
- Informal capacity estimates are not authoritative model telemetry.

Unproved behavior must stay labeled as such. Availability is not silently
upgraded to proof, and an unavailable feature is not replaced by a look-alike.

## 3. Mandatory CLI and bounded automatic preparation

The CLI is required for startup of the Chantier role.

Automatic preparation is authorized only through the official procedure for the
selected source and version, including the dependencies that procedure requires.
This is an explicit exception to the read-only-check rule below.

Do not silently:

- Select another source or version.
- Upgrade Chantier to make an error disappear.
- Substitute another tool.
- Attempt improvised repair or alternative installation procedures.

If official preparation fails, or the CLI remains unusable, report the exact
failure and stop role initialization. Do not present a partial startup as
successful. This is the explicit exception to action-scoped blocking.

## 4. Startup checks and side effects

Ordinary checks must not create files, install dependencies, activate services
or hide writes in child commands. Classify commands by their actual effects,
not by names such as "preflight".

The explicitly authorized exceptions are official CLI preparation and the
seat-acquisition rule below. Board launch and autosync joining have their own
permission requirements.

For checks other than the mandatory CLI:

- Block the actions whose prerequisites failed.
- Identify those actions and the reason.
- Do not block unrelated discussion.
- Distinguish failure, unavailability and checks not performed.

For example, unavailable GitHub authentication can block delivery without
preventing backlog discussion.

## 5. Seat acquisition

Following an explicit invocation of the Chief of Staff:

- A free seat may be taken without another confirmation.
- A seat already owned by this session needs no ownership-change confirmation.
- A seat naming another session requires a question before takeover, including
  when the other session's liveness cannot be established.

Never infer permission to replace another session from inactivity or unknown
liveness. Existing active-batch handover and role boundaries remain applicable.

## 6. Board launch

Ask before starting the board server. Explain its relevant effects, including
the persistent process and the configured network exposure.

Board permission and autosync permission are independent:

- Accepting the board must not implicitly join autosync for either the board
  process or the agent session.
- The board must be able to run without joining autosync.
- Do not stop or reconfigure another session's shared service implicitly.

Report the board's verified readiness and the limits of testing. A listening
address is not proof of LAN reachability.

## 7. Autosync opt-in and manual synchronization

Starting a persistent autosync participant requires explicit opt-in. It is not
an automatic consequence of starting the role or the board.

Opt-in concerns persistent participation, not a general ban on surface Git
operations. Without participation, follow the project's existing manual
synchronization rules.

Do not stop other participants because this session has not opted in.
Existing shared synchronization and this session's participation are different
facts and should be reported as such.

Project rules still govern synchronization, approvals, conflicts, secret
scanning and publication. This proposal grants no additional Git permission.

## 8. Permission scope, inheritance and re-invocation

Where startup permission is needed, obtain it in the interactive session rather
than repeatedly asking through subordinate agents.

Permissions apply only to:

- The session in which they were granted.
- The project concerned.
- The explicitly authorized effects.

Subordinate agents inherit only the permissions necessary within their role.
Inheritance never grants additional merge or publication permission.

A simple reload does not require the same grant again or authorize duplicate
services. Additional effects or a different project require a new grant.
Permissions are withdrawable; this does not authorize stopping a shared service
owned by another session.

These are effect-specific rules, not a requirement to ask one blanket activation
question on every startup:

| Effect | Final rule | Decision |
| --- | --- | --- |
| Official CLI preparation | Automatic; failure stops role initialization | Q17, Q19, Q23 |
| Free or own CoS seat after explicit invocation | No redundant confirmation | Q20 |
| Taking another session's seat | Ask; unknown liveness is not permission | Q20 |
| Board server launch | Ask first | Q17 |
| Persistent autosync participation | Explicit opt-in; independent of board | Q17, Q21 |
| Manual surface synchronization without participation | Follow existing project rules | Q24 |

## 9. Startup report

Use a short factual report covering:

- Role and project.
- Relevant checked state.
- Blocked actions and their causes.
- Permissions pending and effects already authorized.
- Limits of the evidence.

Offer the detailed product introduction on request instead of requiring it in
the initial report.

Do not invent remaining context capacity, imply a skipped check passed, or
describe an untested network or session path as verified.

## Acceptance criteria

These are required outcomes to verify during realization, not results already
obtained:

1. The mandatory Chantier startup documentation for every supported role/host
   combination fits within 12,288 bytes, including common and host material.
2. Later actions have explicit required references, and an unavailable
   indispensable reference prevents that action.
3. Official CLI preparation preserves the selected source/version; failure
   ends role initialization with the diagnostic and no alternative route.
4. A free CoS seat after explicit invocation is taken without a redundant ask;
   another occupant, including unknown liveness, is never replaced silently.
5. Declining a board launch starts no board server.
6. Accepting a board without autosync opt-in creates no autosync participant
   for either the server or the session.
7. Existing shared autosync participants are not stopped by a local opt-out.
8. Without autosync participation, manual synchronization follows project rules.
9. Reloading does not duplicate services or repeat unchanged permissions.
10. Action-scoped failures do not falsely block unrelated discussion, while
    mandatory CLI failure still stops role initialization.
11. Reports distinguish tested local readiness, announced bindings, available
    tools, untested paths, and skipped validation.

## Unresolved items and evidence still due

No unresolved user decision was identified at interview closure.

The size target and cross-host behaviors are not yet demonstrated. Concrete
verification belongs to realization; this document does not claim that a
scenario, host trial or implementation already passes.
