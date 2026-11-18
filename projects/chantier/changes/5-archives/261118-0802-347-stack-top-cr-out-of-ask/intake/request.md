# A CR taken on top of a ready stack stays out of its ask

From the retro of batch-24 (2026-11-18), kept by the retro critic; the user asked to file all six and run them in batch-24.

CR-342, CR-343 and CR-344 were all taken on CR-341's branch (`take`'s nearest earlier CR with a PR), so CR-342's draft PR blocked the partial-stack ask for CR-338..341 (`forge-stack show` 'missing #304' until the Foreman reordered the record), and the final-order restack needed conflict resolvers on CR-344 and CR-345 plus new Inspectors and Verifiers. A CR taken on top of a ready stack is based on the CR just before it in the stack order and kept out of that stack's ask until it hands back.

