Real-window integration test flakes. paste-url is a race in the test (diagnosis: CR-350 work/diagnosis.md); proposed test-only fix: drop the obsolete stored-mode wait at test/integration pasteUrl.test.ts:155 and the same wait in dropFiles.test.ts and findInPreview.test.ts. checkbox-toggle also flaked on main 24c9eef (CI run 44651927198).

Also (2026-11-20, CR-350 heavy dispatch 44690391950 at 412ca69): preview-editing stepSchemaOrderAndBadge locator timeout (issue-highlight), and the paste-url edit-mode wait again.
