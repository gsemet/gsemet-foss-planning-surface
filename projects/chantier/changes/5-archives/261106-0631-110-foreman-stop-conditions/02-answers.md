# Answers

Given by the user on 2026-11-06, in the Chief of Staff's session.

- **Heartbeat:** 30 minutes instead of 55.
- **Stop:** when the batch has landed, or when something is blocked and nothing moves. The user
  can take long over a review; at worst they wake the Foreman. A stack blocked and not finished
  is a stop too.
- **The rule:** while any Driver is active the Foreman stays. When all have ended or are blocked,
  and none is active after 30 minutes, everything stops.
- **Long PR:** a PR in a long fix loop keeps its Driver alive, with an exit condition so that it
  cannot loop forever.
