# A project icon for T3 Code through `t3.json` at the repository's root

The user's request (2026-11-18), as given:

Ajoute une icône de projet pour T3 Code via un fichier `t3.json` à la racine du dépôt.

Contexte : T3 Code choisit l'icône d'un projet dans cet ordre :
1. le champ `iconPath` de `t3.json` (chemin relatif à la racine, qui doit rester dans le dépôt) ;
2. sinon, des fichiers usuels : favicon.svg/.ico/.png à la racine ou dans public/, app/icon.*,
   src/app/favicon.ico, src/app/icon.*, assets/icon.*, assets/logo.*, .idea/icon.svg ;
3. sinon, le `<link rel="icon" href="…">` de index.html ou public/index.html.

À faire :
1. Si un fichier de l'étape 2 existe déjà, ou si index.html déclare une icône qui existe,
   ne change rien : dis-le-moi et arrête-toi.
2. Sinon, trouve le meilleur logo du dépôt : logo, icon ou favicon, en .svg ou .png, plutôt
   carré, dans images/, assets/, docs/, media/, .github/ ou le README. Prends un fichier suivi
   par git, pas un fichier dans node_modules ou un dossier de build. Si plusieurs candidats se
   valent, montre-les-moi et demande lequel prendre.
3. Crée `t3.json` à la racine, ou complète-le s'il existe déjà sans toucher à ses autres
   champs :
   {
     "$schema": "https://t3.codes/schema/t3.json",
     "iconPath": "<chemin/relatif/vers/le/logo>"
   }
4. Optionnel, seulement si c'est évident d'après package.json, justfile, Makefile ou
   pyproject : propose-moi, sans les ajouter d'office, des entrées "scripts" pour T3.
   Chaque script a "name", "command" et éventuellement "icon" (une valeur parmi play, test,
   lint, configure, build, debug). Il peut aussi avoir "runOnWorktreeCreate": true pour un
   script d'installation lancé à la création d'un worktree.
5. Ne commite pas. Montre-moi le `t3.json` final.
