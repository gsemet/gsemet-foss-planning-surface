# Intent

The user wants a release CR to be the last CR of its batch by default: it depends on every other
CR, a CR added along the way included, and it starts only once they are all delivered.

Today a release CR exists only through `open --release`, and `order add` cannot make one, so a
batch already running cannot take its release. The rule that holds it back, `others_merged`, shows
nowhere: `status` draws a queued release as if it could start.

What a release ships is known only at the end: the version depends on the CRs added since it was
filed. So a release can join a batch early, but it cannot be fully prepared early.
