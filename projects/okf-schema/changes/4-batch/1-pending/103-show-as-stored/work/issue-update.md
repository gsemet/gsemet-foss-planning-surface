A correction to the comment above, before any code:

- `okf-schema show` will still print the stored file as it is, with nothing added.
- The trust level moves to a new command: `okf-schema trust --path <bundle> <concept>` will print `trust: <tier>`, and `stale: true` when the concept is stale. This replaces the sentence saying that the trust tier would appear in no command.
- On a file that is not valid UTF-8, `show` will print its bytes as they are, and `trust` will report an error (exit code 2).
- A separate change, delivered first, will fix the trust tier for the actor forms of OKF 0.2: `reference_agent/gemini-2.5-pro` is read as unverified today.
- Planned for a minor release (0.19.0) instead of a fix release.

No date yet; the pull request will be linked here.
