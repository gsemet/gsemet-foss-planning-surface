# CommentsController.post() records its text hash before the last staleness check

From PR #189 (review-threads diagnostics): `CommentsController.post()` stores its text hash before
its last staleness check, so an overtaken post can make a newer post with the same text skip
posting. Possible lost comment update. Reproduce with a unit test, then fix.
