# Verify CR-486

Head: f7e99103cc4ca824807c3d196cb69ba5735fc74f

- Spec's 8 tests (beside x3 origins, own folder with status, nested, no match x2 with Refresh, several, no pointer x2 with no `remote` call, surface keys, Windows CRLF) pass at f7e99103. Command: `just mod` in the worktree. Output: `106 pass 0 fail`, each new test listed `(pass)`. They are new in the diff against the base (`git diff <base>...HEAD -- hooks/register.test.tsx`: +206 lines), so absent on the base. VERIFIED.
- Behaviours read against `hooks/register.tsx` at f7e99103 (git diff): pointer regex, CRLF split, ancestors then siblings, exists-before-git, normalUrl, pinned base with site.root = surface, common read from surface cwd, no-match and several lines match the spec text, `choose` and `rechoose` honour `pinned`, `site-6`, header comment. VERIFIED.
- docs/boards.md sentence present (diff). VERIFIED.
- PR body draft (work/pr-body.md): consistent with the diff; Known gaps names the missing real-session screenshot. The posted PR's head is f7e99103 (`gh pr view 464`). Test plan boxes still hold `<sha7>` placeholders: to fill at ship. No images. VERIFIED as a draft.
- Gates cited by the Driver (just check, scenario, CI): not re-run here.
- Real-session screenshot: UNVERIFIED (Playwright not installed), stays a Known gap.

VERIFIED
