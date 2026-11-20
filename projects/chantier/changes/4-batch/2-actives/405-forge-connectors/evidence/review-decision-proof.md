# GitHub reviewDecision real reads (2026-11-20)

## gsemet/okf-schema PR 55 (default branch protection: required_approving_review_count=1)

    gh api graphql -f query="query { repository(owner:\"gsemet\", name:\"okf-schema\") { pullRequest(number:55) { reviewDecision } } }"
{"data":{"repository":{"pullRequest":{"state":"MERGED","reviewDecision":"REVIEW_REQUIRED"}}}}

## gsemet/chantier PR 374 (default branch protection: required_approving_review_count=0)

    gh api graphql -f query="query { repository(owner:\"gsemet\", name:\"chantier\") { pullRequest(number:374) { reviewDecision } } }"
{"data":{"repository":{"pullRequest":{"state":"OPEN","reviewDecision":null}}}}
