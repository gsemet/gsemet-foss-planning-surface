Short name: `stack-chain`

# Answers
1. stack-chain-Q1 (2026-11-21): **When the chain is checked.** A. Refused at `ship`: at each ship of a CR already stacked, the CLI refuses when its branch is not based on the head of the CR below ("CR-442: branch not based on CR-441's head"), before a gate or verdict is paid on it.
2. stack-chain-Q2 (2026-11-21): **The stack driver's check before "no restack needed".** A. One card line: it verifies with `git merge-base` that each branch starts from the head of the CR below.
3. stack-chain-Q3 (2026-11-21): **Series batches too.** A. Series and stack: wherever a CR is meant to start from another.
