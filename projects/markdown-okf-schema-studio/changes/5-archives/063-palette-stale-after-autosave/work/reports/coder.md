Fixed. Commit 51920e5 on changes-requests/063-palette-stale-after-autosave. Verified by code reading
(currentPreviewDocument compared document.revision to the render revision) and a unit test that failed
before the change. No real-window run.
