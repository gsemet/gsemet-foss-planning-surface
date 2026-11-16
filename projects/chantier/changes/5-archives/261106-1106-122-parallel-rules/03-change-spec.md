# A batch runs its CRs in parallel unless the plan says why not

By default a CR starts as soon as a slot is free, and the stack driver rebases afterwards. Touching
the same file is no reason to wait.

## The rules, in the cards

- **`chief-of-staff.md`, dependencies:** `depends.json` is written only when a CR needs the result
  of another. The plan says what it needs. Two CRs editing the same file do not depend on each other.
- **`chief-of-staff.md`, a queue:** the Chief of Staff may propose a queue with no real dependency,
  for instance when the work is small and rebasing it would cost more than waiting. The plan gives
  the reason for each CR queued this way, and the user's go approves it. There is no threshold: the
  Chief of Staff judges and says why.
- **`chief-of-staff.md`, the plan:** it says how many CRs start at once, on how many slots.
- **`foreman.md`:** the Foreman takes every CR `take` accepts, up to the free slots, and holds none
  in reserve.
- **`concepts.md`:** the batch and dependency entries say the same.

## The base of a CR

In a stack, a CR with no open dependency starts on the default branch, not on the CR before it in
the chain. `take` prints that base. A CR with an open dependency keeps today's rule: it starts on
the branch of its last dependency still open.

`take stack` is unchanged in what it does: it prints the stack in its order, and the stack driver
puts each CR on the one under it once they are ready. A CR's start base and its place in the stack
are two things, and the CLI keeps them apart.

## Changing a dependency in an open batch

A new order, `order after <cr> --note "<CR ids, comma separated, or - for none>"`, replaces the
`after` of a queued CR, with no drop and no new number.

- It exits 2 on a CR that is not queued, an unknown CR, or a cycle, as `open` does.
- It is logged and printed as a line for the Foreman, as any order.
- `chief-of-staff.md` lists it with the other orders.

## Done when

- The cards say this, and a stack's independent CRs start on the default branch.
- `just scenario` runs a stack with independent CRs taken at once, then stacked, and changes a
  dependency with `order after`.
- `just check` and `just scenario` pass.
