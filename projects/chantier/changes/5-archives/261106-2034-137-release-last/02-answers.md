# Answers

- **A computed list or real dependencies?** Real ones: the release's `after` holds the CRs, by the
  user's word, over a list recomputed at each read.
- **What of a CR abandoned or descoped?** It must be handled properly: it stops holding the release
  back, where a cancelled CR stays unmet for any other `after`.
- **Can a release be prepared ahead?** Not entirely, by the user's word: "on ne peut peut être pas
  préparer entièrement la release en avance de phase", the version for one. The version is settled
  with the user once the others are delivered.
- **Where does it run?** In batch-07, so that v0.7.0 closes that batch, by the user's word. The
  release itself is added once this CR is merged.
- **May a CR join once the release has started?** No, by the user's word, a fix of the release
  excepted: a CR that comes after the release goes in a next batch. Batches do not run in parallel
  for now, so it waits in the inbox until this one closes.
