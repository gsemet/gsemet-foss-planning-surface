# Retro

- Cost: three PRs (#357, #358, #359) lost visual runs and one rerun before the cause was clear.
- Root cause: ci.guidelines rule 4 cached the archives but still refreshed the package lists, twice.
- Process fix: done in this CR (rule 4 now says a full cache installs without a refresh).
