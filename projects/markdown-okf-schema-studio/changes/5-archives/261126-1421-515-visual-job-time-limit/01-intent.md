# The CI visual job runs at its 15-minute limit

The job `visual` of `.github/workflows/ci.yml` takes 804 to 890 s of its 900 s on main and was
cancelled on both attempts of run 45795716172 (head 5f7658a, CR-511). Every pull request runs it, so
it can block each CR of batch-09. See `intake/request.md` for the runs.

Wanted: every run of the checks the job does today ends well under its limit, with the limit not
raised, no check dropped and no re-run used to pass. Splitting the job or making it faster are both
acceptable; the choice belongs to the specification. The CR sits low in batch-09's stack so that the
CRs above it get the fix.
