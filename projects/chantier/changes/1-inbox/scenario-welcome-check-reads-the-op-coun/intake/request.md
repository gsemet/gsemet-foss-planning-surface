# Scenario welcome check reads the op count from protocol.OPS

Retro of batch-30: the scenario's welcome check hard-codes the number of server ops, so CR-449 and CR-458 broke it in turn. It reads the count from protocol.OPS, and a Driver whose change touches the protocol runs the scenario unit before its push.