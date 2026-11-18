# Optimise the startup core in size and efficiency

The startup core (the files `startup-manifest.json` names: common, host and role cores and each
role's wrapper) is read whole by every session and agent at each boot and reload. It sits at its
limit of 12544 bytes since v0.13.0 (CR-363), so each new rule that must be read at boot (the
watcher's start, 2026-11-18) has to fight for room. The user wants the limit kept and the core
made smaller and more effective: the rules that matter at boot clear and unmissable, the rest
deferred to the cards.

Source: the user, 2026-11-18: « Je suis d'accord pour que la limite à 12K reste, il faut que ce
noyau soit optimisé en taille et en efficacité. »
Short name: `startup-core-optimise`
