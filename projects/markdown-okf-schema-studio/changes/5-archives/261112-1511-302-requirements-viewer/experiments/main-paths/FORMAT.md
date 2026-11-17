# `### Main paths` in a StRS (proposed format)

A StRS tells its use case as one or more paths through states. Each path is a numbered list of
states; under a state, the SwRS that leads to the next state, and the other options a reader has
in that state.

```markdown
### Main paths

#### Path 1: <short name of the path>

1. <state, in the reader's words>
   - SwRS-<ID>: <what moves the reader to the next state>
   - Option SwRS-<ID> (<nominal|boundary|refusal>): <another thing that can happen here>
2. <next state>
   ...
3. <final state: the result the user wanted>

#### Path 2: <name>

1. <a state already named in path 1, same words: the paths join there>
   - SwRS-<ID>: ...
2. <final state>
```

Rules:

- A state is the same state in every path when its text is the same.
- The first bullet without `Option` is the step to the next state; it is drawn on the path.
- `Option` bullets are drawn as branches; the scenario kind in brackets, when given, picks the
  scenarios of the SwRS that this option covers.
- A SwRS that derives from the StRS and appears in no path is listed under the map as "also
  serves this need".
- The last state of a path has no bullet.
