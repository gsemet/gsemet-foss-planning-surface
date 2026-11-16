# Answers

## Grill of 2026-11-10, batch-09 paused

1. **How the phone reaches the board.**
   - The options were:
     - through the forge, reading the `STATUS.md` files pushed to the planning repository (the recommendation);
     - the prototype's server reached through Tailscale;
     - a private artifact page.
   - The user chose "Serveur + Tailscale".
   - The board stays a small web server. The phone reaches it through the user's private Tailscale network.
   - The risk, as said in the question: the server has no authentication.
2. **Read or write.**
   - The user chose "Lecture seule (Recommandé)".
   - The board only shows. To act, the user talks to the Chief of Staff.
3. **The address the server listens on.**
   - The recommendation was the Tailscale address only, `127.0.0.1` by default, and `0.0.0.0` refused unless asked.
   - The user chose "0.0.0.0 permis".
   - Listening on all interfaces is allowed. It also opens the board on the local network, with no password.
4. **Who starts and stops it.**
   - The user: "Il se lance quand le chief of staff démarrer en background. Il s'arrête quand le chief of staff se clôture ou passe à un nouveau".
   - The Chief of Staff starts the board in the background when its session starts.
   - The board stops when that Chief of Staff session ends, or when the seat passes to a new Chief of Staff.
5. **How chantier ships it.**
   - The recommendation was a separate script, because AGENTS.md limits the CLI's scope.
   - The user chose "Commande du CLI": a `chantier board` command.

## Still open (grill paused by the user: "On grillera après")

- **The CLI rule.** A `chantier board` command goes against AGENTS.md's CLI scope. Either the CR amends AGENTS.md with a named exception and its reason (the recommendation), or the board is a separate script.
- **The default address.** The board starts with each session. Either `127.0.0.1` by default and `0.0.0.0` on request (the recommendation), or `0.0.0.0` by default.

## Decisions of 2026-11-11 (the two points still open)

Decided by a Fable advisor on the user's delegation: "Grille tout avec une session fable je ne sais pas te répondre…"

6. **The CLI rule: the board is a `chantier board` command (answer 5 stands), and the CR amends
   AGENTS.md's CLI-scope line to name it:** a read-only view of the record the CLI already keeps.
   Reason: the user chose the command; a separate script would need its own way to find the
   planning folder, against "works with no setup"; the exception is written, not silent.
7. **The exception is bounded in that same line:** the board reads only, writes no file, uses the
   standard library only, and knows no role. Anything more (answering an ask, filing an item) is
   another CR. Reason: keeps the scope rule meaningful and answer 2 true.
8. **The default address is `127.0.0.1`.** Another address (`0.0.0.0`, or the Tailscale
   address) is used when asked: by an option of the command, or once for the project in
   `chantier.yaml`, which the Chief of Staff's start then follows. Reason: the board starts by
   itself in every project and has no password; opened by default it would show the planning
   folder to any office or public network. Answer 3 ("0.0.0.0 permis") holds: allowed, on the
   user's word.
9. **When the board listens beyond the local machine, the Chief of Staff says so once at start,
   with the address and "no password".** Reason: the risk is the user's to know each session.
10. **A board that cannot start (port taken, address not there) never blocks the session:** one
    line says why, and the Chief of Staff goes on. A board already running for this project is
    reused, not doubled. Reason: the board is a comfort; the batch is the work.
11. **The board follows the planning folder wherever it is** (in the project or on an external
    planning surface) and today's layout only (`4-batch`). Reason: one generic rule; the
    prototype's older folder names are dropped.
12. **To check at the specification: the overlap with the backlog item `planning-server` (P3).**
    If both serve the same pages, they are one CR. Reason: two servers over the same folder
    would be over-design.

## The specification's open question (2026-11-11)

Settled by the Chief of Staff on the user's delegation ("Grille tout avec une session fable je
ne sais pas te répondre…").

- **A surface with several projects:** one board per project, started and owned by that
  project's Chief of Staff, on its own port. Reason: one owner per board, the seat rule as it
  is; a shared board would need an owner the seat does not name.
