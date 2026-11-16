---
type: cr-intent
id: model-defaults-board-config
description: User-requested cross-harness agent configuration and board editor, with requirements captured and design still to specify.
generated:
  by: Copilot
  at: "2026-11-16"
sources:
  - {id: request, resource: intake/request.md, title: Initial configuration request, last_modified: "2026-11-16"}
  - {id: discussion, resource: "agent-host-session://ahp-session/677413b8-a70b-4570-8f08-34eec54f803f", title: Configuration discussion and expanded user requirements, last_modified: "2026-11-16"}
---

# Flexible agent configuration across coding-agent harnesses

## Current understanding

The user wants a configuration system designed across coding-agent harnesses, not a
Copilot-only model override. Plugin agent files remain the distributed bases. Users
must be able to customize roles, including models and tools, without editing those
installed files or losing their settings when the plugin updates.

The initial request remains in [the immutable intake](intake/request.md). The user
subsequently confirmed P1 and expanded the scope as recorded below. This request is
separate from CR-296 improve-skill-boot and is not authorized to join batch-20.

## Requirements captured on 2026-11-16

- Replace the hardcoded model catalog/defaults with `config/chantier.defaults.yml`
  in the Chantier repository. Preserve the host-specific agent frontmatter format.
- Use the shipped agent definitions as bases for configurable roles, rather than
  requiring users to fork or modify installed plugin agent files.
- Support customization beyond model selection, explicitly including tools.
- Design the role configuration independently of the coding-agent harness, with
  host-specific translation where necessary. Unsupported capabilities must be
  explicit; do not silently substitute models or drop tool restrictions.
- Avoid scattering temporary agent files across workspaces or user directories.
  Whether any controlled materialization is necessary remains a design question.
- Provide a generic root-level `chantier.yml` and per-project configuration in an
  external planning surface, such as `projects/chantier/chantier.yml`.
- Provide a Configuration page in the Chantier board for easy project-level
  customization. It must use the same configuration and resolution rules as the CLI,
  rather than maintaining an independent configuration mechanism.
- Preserve plugin upgradeability: user configuration remains separate from the
  installed plugin files.

## Known constraints and unverified options

- The current implementation recognizes `chantier.yaml` at the code repository root;
  it does not yet implement the requested surface configuration location.
- Chantier currently refuses per-role model overrides on Copilot because the launch
  capability is recorded as unproved.
- This session's `task` tool exposes an explicit model parameter. A generic-agent
  launch with the role contract supplied in its prompt is a candidate approach,
  not a verified design or an equivalent replacement for enforced tool restrictions.
- Effective model selection and tool restrictions must be verified on each supported
  harness. Do not equate prompt instructions with harness-enforced permissions.
- CR-296 round 5 provides a concrete Copilot-host finding: its Driver passed
  `model: gpt-6.1-sol` with the named `chantier-coder`, but the host reported
  "Required model enforcement replaced requested model `gpt-6.1-sol` with
  `gpt-5.6-luna`." Thus this named agent's required model took precedence in
  this execution. The Coder had already edited files when the Driver received
  the result; post-completion detection is not a pre-execution guarantee.
  The user authorized a sixth-round generic Sol Coder trial with the role
  contract supplied explicitly; its outcome is not yet established.
- No attachment or source tracker issue has been supplied.

## Open design questions

- Which root does the generic `chantier.yml` belong to: code repository, planning
  surface, or both? What is the precedence when both exist?
- How do plugin defaults, the generic root configuration and surface-project
  overrides merge, especially lists such as tools?
- How are `chantier.yaml` compatibility and conflicting filenames handled?
- Which role fields beyond model and tools are configurable, and how are tool
  additions constrained by the harness and user permissions?
- How are plugin agent bases read and translated without duplicating their contracts
  or generating unmanaged files? How do base changes interact with existing overrides?
- How does the board show inherited values, overrides, effective settings and
  unsupported capabilities, and validate changes before saving?
- How do configuration changes interact with already-running or frozen batches?

## Next step

Specify the configuration layers, merge semantics, capability contract and board UX,
then verify the launch mechanisms on the supported harnesses. No implementation or
additional batch launch is authorized by recording this request.
