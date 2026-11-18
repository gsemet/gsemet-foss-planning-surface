# A restack re-checks PR bodies' SHAs and evidence links

From the retro of batch-24 (2026-11-18), kept by the retro critic; the user asked to file all six and run them in batch-24.

After a restack, PR-body evidence captions named SHAs no longer in the head's history, and one PR's screenshot links pointed at blobs of the pre-restack commit, which GitHub may drop. The restack re-checks each PR body's SHAs as `ship` does, and evidence images are attached as uploads or recaptured at the restacked head.

