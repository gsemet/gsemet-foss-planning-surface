# Independent FullCycle Inspector Feedback

**Initial verdict: REWORK.** Review of coder revision `17fdfca` found three evidence and
implementation gaps that made its `GO` claim premature:

- `enableFindWidget` was not enabled on the `WebviewPanel`, so native Webview find was not
   available. The first attempted fix put the option on `WebviewOptions`, which is not the VS Code
   API surface that owns it.
- Accessibility CSS was emitted as a file inside the disposable Sphinx output stage. The trusted
   extension-host run reported `Webview.loadLocalResource - Error using fileReader`; changing the
   filename did not change the failure, which implicated stage lifetime rather than dot-file
   handling.
- The evidence named stale revision `93bf8d2`, had no real browser suite, and left selection/copy,
   Webview find, zoom, screen-reader, theme, high-contrast, reduced-motion, and stock-coexistence
   checks pending while still declaring `GO`. Serialized HTML, fake-DOM events, and a successful
   extension-host exit do not prove those interactions.

The inspector moved `enableFindWidget` to `createWebviewPanel`, inlined the accessibility CSS
under the existing CSP nonce, added regression assertions for both changes, and reran the trusted
and untrusted extension hosts. The local-resource error disappeared. A real Chromium probe now
exercises authentic sanitized Sphinx output and the compiled Webview runtime for selection,
clipboard copy, native Webview find, keyboard reveal, deferred navigation, theme updates, forced
colors, reduced motion, responsive resize, preview scroll messages, and stock-preview coexistence.
The probe also verifies the semantic accessibility tree. Actual VoiceOver or other
assistive-technology speech output was not executed and is not inferred from those checks.

**Final inspector verdict: ACCEPTED / GO for the Task 06 development gate.** The focused unit,
extension-host, browser, packaging, security, and semantic accessibility checks pass after rework.
The documented VoiceOver protocol remains unexecuted and is retained as Task 07 release evidence;
this verdict makes no claim about spoken output or final release readiness. Task 07 remains
unreached and this review does not start it.

# Task 06: Interaction and Parity Completion

**Depends on**: Task 05

## Important Information

Before coding, Read FIRST -> Load [05-task-00-READBEFORE.md](05-task-00-READBEFORE.md)

## Applicable Guidelines

| Rule | Application |
| ---- | ----------- |
| [Stock preview inventory](02-stock-livepreview-spec.md) | Use relevant interaction ideas; do not clone every stock feature. |
| Independent settings | Use MyST-specific settings with stock-like defaults; never mutate stock settings. |
| Native diff | Leave the stock rendered-diff workflow untouched. |
| Accessibility | Support keyboard use, semantic output, focus, zoom, contrast, screen readers, and reduced motion. |
| Mapping honesty | Maintain block/line sync and inert unmappable fragments. |

## Objective

Complete bidirectional scrolling, basic preview interaction, theme, accessibility, and stock
non-regression for the one side preview of the active Markdown file.

## Files to Modify/Create

- `package.json`
- `src/configuration/*`
- `src/webview/*`
- `media/*`
- `test/integration/parity/*`
- `test/browser/*`

## Detailed Steps

1. Add only the MyST-specific settings needed for this preview. Do not alter stock settings.
2. Complete active-file editor-to-preview and preview-to-editor mapping with image-load stabilization,
   stale-response rejection, and feedback-loop suppression.
3. Test rendered text selection/copy, local links, Webview find, and keyboard focus on a MyST file.
4. Confirm opening the MyST view does not change the stock Markdown preview or its settings.
5. Complete safety UX: trust-disabled command state/message, blocked-content diagnostics, active
   resource policy, and no permissive security selector that can bypass hard gates.
6. Complete accessibility: semantic headings/landmarks, alt text, keyboard navigation, visible
   focus, high contrast, theme changes, zoom, screen-reader labels, and reduced-motion behavior.
7. Cover empty, malformed, missing, deleted, and build-failing documents without replacing
   current content with another document or presenting stale output as current.
8. Test short and long open files, unsaved edits, images, editor switches, rapid scrolling,
   theme changes, and reduced motion. Use focused visual checks for long-page drift.

## Acceptance Criteria

- [ ] MyST settings never modify `markdown.*` settings.
- [ ] Editor-to-preview and preview-to-editor scrolling remains stable after images, insertions,
      resize, zoom, rapid movement, hidden content, and includes.
- [ ] Source reveal never navigates unmappable output; rendered text, local links, and Webview
   find work in authentic MyST/Sphinx output.
- [ ] The stock preview retains its settings, commands, and rendered diff after installation.
- [ ] Trust and blocked-content UX cannot bypass Task 01 safety controls.
- [ ] Keyboard navigation, semantic headings/landmarks, focus, alt text, zoom, high contrast,
      screen-reader labels, and reduced motion have automated or documented manual evidence.
- [ ] Empty, malformed, missing, deleted, and failing active documents show correct status and recover.
- [ ] Long-file visual checks show no cumulative source/preview drift or unreadable error state.
- [ ] Focused unit, extension-host, browser, and accessibility checks pass.

## Testing Strategy

Use extension-host tests for active-document identity, settings, stock coexistence, and focus.
Use Webview tests for scrolling, find, theme, and zoom. Record manual accessibility checks when
automation is unavailable.

## Notes

Do not weaken rendering, dirty-source integrity, mapping, Workspace Trust, or resource security.
Do not describe the single-file MyST preview as a full stock-preview replacement.
