# A Verifier's throwaway board stops with the Verifier

Retro of batch-30: a Verifier's throwaway `chantier serve --port 0` outlived it and held the CR folder, so `order merged CR-460` failed (WinError 5) until the user agreed to stop it by hand. The throwaway board stops when the Verifier ends and never outlives it.