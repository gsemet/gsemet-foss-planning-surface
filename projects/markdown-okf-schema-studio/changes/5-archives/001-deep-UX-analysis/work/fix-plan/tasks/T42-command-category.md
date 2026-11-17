# T42 — Short command titles with a category

| Field | Value |
| --- | --- |
| Fixes | Follow-up of [UX-30](../../07-discoverability-and-chrome/UX-30-no-entry-point-besides-palette.md) (Explorer label) |
| Decisions | D-20, D-13 |
| Depends on | T40 |
| Gate | `unit contracts full` |
| Risk | Low (the reload suite finds the command by its palette text) |
| Commit message | `fix(vscode): give the Studio commands a category and short titles` |

## Goal

The Explorer context menu and the title-bar tooltip read "Open Preview to Side". The Command
Palette still reads "Markdown OKF-Schema Studio: Open Preview to Side".

## Allowed files

- `package.json`: `contributes.commands` only.
- `test/security/package-contract.test.ts`: only the expected `commands` entries.
- `README.md`: only if a sentence names the Explorer entry with the full title. The palette
  sentence at line 140 stays as it is: the palette text does not change.

## Steps

1. In `package.json`, give each of the two commands:
   - `"category": "Markdown OKF-Schema Studio"`;
   - a title without the prefix: `"Open Preview to Side"` and `"Refresh Preview"`.

   Keep every other key unchanged: `icon`, `enablement`, `menus` and `keybindings`.
2. Update the expected commands in `package-contract.test.ts` to match, and add the `category`
   field to the test's type if it needs one. Keep every other assertion unchanged.

## Tests

- **Unit / contracts:** `package-contract.test.ts` asserts the new entries.
- **Full gate:** the reload suite runs "Markdown OKF-Schema Studio: Open Preview to Side" from the
  palette. It must pass unchanged, which proves the palette text did not change.

## Expected changes to existing tests

- `package-contract.test.ts`, "contributes only opt-in …": the two `commands` entries. List them.

## Must not change

- The command IDs, the menus, the keybinding, and the palette text.
