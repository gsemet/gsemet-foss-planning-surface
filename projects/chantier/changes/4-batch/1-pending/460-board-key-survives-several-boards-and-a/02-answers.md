# Answers

- 2026-11-22, the user, on SameSite: "Lax maintenant" — move the board cookie from SameSite=Strict to Lax in this CR. The spec-critic noted the iOS refresh bug comes mainly from the shared cookie name (fixed by CR-456) and the paste field; Lax is kept for links opened from another site (webmail, chat, GitHub), with writes still POST-only and checked on origin.
