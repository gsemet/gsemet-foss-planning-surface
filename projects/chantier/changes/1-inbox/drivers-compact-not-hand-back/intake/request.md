# Drivers compact their context instead of handing back

Drivers should compact their context and go on, instead of handing back `blocked context`.

Owner's words (2026-11-25, translated from French): "That context size really must be configurable, because here it is too small for the drivers. Can't they compact? Normally that is the usual method to keep the context under control."

This belongs with the item `context-limits-of-the-drivers-configurab` (thresholds as settings, default raised, one list), which does not mention compaction in its request. Chantier's own Chief of Staff or Griller decides whether to fold it into that change or keep it apart.

Wanted:
- Establish first, by measurement, what each host offers: whether a background Driver is compacted by the host, when, and whether the Driver can ask for it. The grill record of the related item already notes agents with a 200,000 window compacted near 162,000 (batch-16 and batch-17).
- Where compaction works, a Driver continues after it (rereads its card and its CR's files) and does not hand back for context.
- Where it does not, keep the hand-back, with the configured threshold.

From the markdown-okf-schema-studio batch-09 (2026-11), where Drivers' hand-backs for context lengthened the batch. Filed on the owner's word (2026-11-26).
