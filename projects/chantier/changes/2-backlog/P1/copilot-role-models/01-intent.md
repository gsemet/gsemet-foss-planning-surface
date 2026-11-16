---
type: cr-intent
id: copilot-role-models
description: User-requested update of Copilot role model defaults, captured for later implementation.
generated:
  by: Copilot
  at: "2026-11-16"
sources:
  - {id: request, resource: intake/request.md, title: Requested Copilot role model mapping, last_modified: "2026-11-16"}
---

# Update Copilot role model defaults

## Requested mapping

| Role | Model |
|---|---|
| CR Driver | Claude Sonnet 5.5 |
| Investigator | GPT-5.6 Luna |
| Coder | GPT-6.1 Sol |
| Inspector | GPT-6.1 Sol |
| Verifier | GPT-6.1 Terra |
| Debugger, when needed | GPT-6.1 Terra |
| Conflict resolver, when needed | GPT-6.1 Terra |

Preserve the other roles' defaults and the Claude Code configuration. This
request does not require starting Debugger or Conflict resolver when unnecessary.
The exact harness identifiers and model availability must be verified during
implementation; the display names above are the user's requested mapping.

## Context and scope

The [original request](intake/request.md) is preserved unchanged. This is a
separate model-default update, related to the broader
[flexible configuration request](../model-defaults-board-config/01-intent.md).
The defaults change must remain consistent with whichever configuration
source is in place when it is implemented, without duplicating sources of truth.

CR-296 exposed that the Copilot host enforces the named Coder's required Luna
model over a requested Sol override. A subsequent generic Coder did run on Sol,
confirmed by host logs. Therefore changing the intended defaults must include
the shipped Copilot agent definitions, not only a runtime override.

## Expected outcome

- Shipped Copilot role definitions select the requested models.
- CLI model catalogs, role-model checks and directly related documentation agree
  with those definitions, including GPT-6.1 Terra.
- Existing model-policy and tool restrictions remain unchanged unless separately
  authorized; no silent model fallback.
- Preserve host-specific frontmatter conventions and shared role contracts.
- Verify the changed defaults and report any availability or host limitation.

## Next step

Implement and validate this mapping in a future authorized batch. Recording this
request does not resume CR-296, modify installed plugin files or authorize a merge.
No tracker issue or attachment was supplied.
