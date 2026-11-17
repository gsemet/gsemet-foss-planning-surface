
# agpkg — coût de `agpkg install` sur cache hit : analyse et propositions

**Émetteur :** équipe C3HW / IVV DevOps
**Version analysée :** `agpkg` master, tag `0.75.1` (commit `848d9a2`)
**Date :** 2026-10-19

---

## 1. Symptôme

Sur les bancs C3HW, l'étape de téléchargement des packages ECU prend **~5 minutes à chaque
job**, y compris lorsque :

- les versions demandées sont strictement identiques au job précédent,
- tous les fichiers sont déjà présents dans le cache agpkg local,
- aucun octet n'est transféré depuis Artifactory.

Ce n'est donc pas un problème de bande passante. En lisant le code, le temps est consommé
par du travail que `install` refait systématiquement alors que son résultat est déjà connu.

---

## 2. Analyse

### 2.1 — Le fichier en cache est relu et re-haché à chaque install

`lib/remotes/_abstract/abstract_cached_file.py`, `download_to_cache()` (L242) :

```python
downloaded = self._download_file_in_cache(
    expected_sha256=expected_sha256,
    remote_sha256=remote_sha256,
)

# Compute and record checksums for the cached file
if self._in_cache.exists():
    checksums = compute_file_checksums(self._in_cache)   # L312
```

`_download_file_in_cache()` a déjà décidé, via `is_file_in_cache()` et le sidecar `.sha256`,
qu'il n'y avait rien à télécharger. Pourtant `compute_file_checksums()` s'exécute quand
même et relit **l'intégralité de l'archive** depuis le disque.

Trois observations :

1. La valeur recalculée n'est utilisée que pour renseigner `self._sha256`, qui est déjà
   disponible dans le sidecar `.sha256` écrit lors du téléchargement initial.
2. Sur le chemin cache miss, le fichier est haché **deux fois** : une fois dans
   `_download_file_and_verify()` (L459-500), une seconde fois ici.
3. `compute_file_checksums()` calcule SHA-256 **et** SHA-1. Le SHA-1 n'est nécessaire qu'à
   l'upload (commentaire L63-65 de `lib/cache.py`), jamais à l'install.

### 2.2 — Le hachage se fait par blocs de 4 KiB

`lib/cache.py`, `compute_file_checksums()` (L57) :

```python
for byte_block in iter(lambda: f.read(4096), b""):
    sha256_hash.update(byte_block)
    sha1_hash.update(byte_block)
```

Idem dans `compute_sha256()` (L84) et `compute_sha1()` (L97).

C'est un point secondaire — voir les mesures en §3, le gain seul est faible — mais il est
gratuit à corriger.

### 2.3 — L'archive est ré-extraite à chaque install, même si rien n'a changé

`api/install.py`, `_install_file()` (L368-381) :

```python
download_result = cached_file.download_to_cache(...)
has_been_downloaded = download_result.has_been_downloaded

if expand_folder and expand_folder.target:
    expand_path = install_directory / expand_folder.target
    _expand_archive_from_cache(...)      # jamais conditionné
```

`has_been_downloaded` est calculé puis utilisé **uniquement pour le reporting**
(`install_report.add_expanded_file(downloaded=...)`). L'extraction, elle, est
inconditionnelle. Il n'existe aucun marqueur permettant de savoir qu'une cible contient
déjà le contenu d'une archive donnée.

C'est le poste de coût dominant sur des packages de plusieurs Go contenant des milliers de
fichiers.

Même remarque pour `copy` : `_copy_file_from_cache()` (L506) fait un `shutil.copy()`
inconditionnel.

### 2.4 — `CHUNK_SIZE = 1024` plafonne le débit de téléchargement

`lib/remotes/_abstract/abstract_cached_file.py` L88 et `utils/artifactoryutils.py` L28-29 :

```python
# keep CHUNK_SIZE under MTU standard size !!!
CHUNK_SIZE = 1024  # 1kB
```

Nous pensons que le commentaire repose sur un malentendu : ce paramètre est la taille de
lecture **applicative** (`iter_content` / `write_to`), pas la taille des segments TCP. La
segmentation est gérée par le noyau à partir du MSS négocié ; la valeur passée à `requests`
n'a aucune influence dessus. Elle détermine seulement combien d'octets sont tirés du buffer
socket à chaque itération Python.

Conséquence : à 1 Ko par itération, un transfert de 1 Go impose **un million d'itérations
Python**, ce qui crée un plafond de débit indépendant du lien réseau (voir §3.2).

### 2.5 — Aucun parallélisme

`api/install.py` (L146-169) : la boucle d'installation traite les dépendances puis les
fichiers séquentiellement. Les téléchargements sont I/O-bound et se parallélisent très bien.

### 2.6 — Le lockfile peut contenir des doublons, qui sont traités deux fois

Dans notre `agpkg.lock.json`, la dépendance `PCU` produit deux entrées distinctes pointant
vers **la même URL** (deux patterns qui résolvent le même fichier) :

```
PCU/Userdebug/S510_PCU_261.04.22_BL07.00_Debug_Binaries_Userdebug_Dev.zip  -> expand ./PCU/debug
PCU/Userdebug/S510_PCU_261.04.22_BL07.00_Debug_Binaries_Userdebug_Dev.zip  -> expand ./PCU/debug
```

`install` traite les deux entrées : l'archive est donc hachée et extraite deux fois. C'est
sans doute à corriger côté `update` (génération du lockfile) plutôt que côté `install`, mais
une déduplication défensive à l'install serait peu coûteuse.

---

## 3. Mesures

### 3.1 Méthodologie et limites

Les chiffres ci-dessous ont été produits sur une machine de développement **Linux / ext4 /
SSD NVMe, cache de pages chaud**. Ce sont donc des **planchers**. Les bancs C3HW tournent
sous **Windows / NTFS**, avec l'analyse antivirus à l'écriture : le coût par fichier y est
structurellement plus élevé.

Nous n'avons volontairement pas extrapolé le facteur Windows. Nous présentons :
- les coûts plancher mesurés, reproductibles ;
- l'observation terrain (~5 min) ;
- et nous demandons en §4.6 l'instrumentation qui permettrait de trancher.

Scripts de mesure fournis en annexe (§6), rejouables tels quels.

### 3.2 Résultats

**Hachage d'un fichier en cache — exécuté à chaque install, même sur cache hit**

| Variante | Débit | Coût |
|---|---|---|
| agpkg actuel : SHA-256 + SHA-1, blocs 4 KiB | 182 MB/s | **5,6 s/Go** |
| SHA-256 + SHA-1, blocs 1 MiB | 205 MB/s | 5,0 s/Go (×1,1) |
| SHA-256 seul, blocs 1 MiB | 288 MB/s | 3,6 s/Go (×1,6) |
| **Non exécuté sur cache hit** | — | **0 s** |

Lecture : augmenter la taille de bloc ne rapporte presque rien (le hachage est CPU-bound).
**Le vrai gain est de ne pas hacher du tout quand le sidecar fait déjà foi.**

**Streaming HTTP — effet de `CHUNK_SIZE`** (loopback, donc sans limite de lien)

| `CHUNK_SIZE` | Débit plafond |
|---|---|
| 1024 B (actuel) | 63 MB/s (~500 Mbit/s) |
| 1 MiB | 90 MB/s (~720 Mbit/s) |

Lecture : à 1 Ko, le débit plafonne à ~63 MB/s **quelle que soit la bande passante
disponible**, sur un CPU de développement récent. Sur le CPU d'un banc, ce plafond est plus
bas. Ce n'est pas le poste principal sur cache hit, mais c'est un plafond artificiel lors
des vrais téléchargements.

**Extraction ZIP — forme réaliste d'un package ECU** (4 000 fichiers × 128 Ko = 500 Mo)

| | Coût |
|---|---|
| `zipfile.extractall` | **2,9 s/Go** (0,36 ms/fichier) |
| Non exécutée si déjà extraite | **0 s** |

### 3.3 Synthèse

Sur un job où **rien n'a changé**, agpkg consomme aujourd'hui un plancher d'environ
**8,5 s par Go installé** (5,6 de hachage + 2,9 d'extraction), dont **la totalité est
évitable**, auquel s'ajoute un appel réseau de stat + SHA-256 par fichier.

Sur nos bancs Windows, l'étape observée est de ~5 min. L'écart entre ce plancher Linux et
l'observation terrain est précisément l'argument : quand le coût unitaire est élevé, la
seule optimisation qui compte est de **supprimer le travail**, pas de l'accélérer.

---

## 4. Propositions

Classées par rapport gain / risque.

### 4.1 — Ne pas recalculer les checksums sur cache hit `[gain fort, risque nul]`

Dans `download_to_cache()`, conditionner l'appel à `compute_file_checksums()` au fait qu'un
téléchargement a réellement eu lieu ; sinon lire le sidecar `.sha256`.

```python
if downloaded:
    self._sha256 = compute_file_checksums(self._in_cache).sha256
else:
    self._sha256 = read_sha256_sidecar(self._in_cache)
```

Supprime aussi le double hachage sur le chemin cache miss.

### 4.2 — Ne calculer le SHA-1 qu'à l'upload `[gain moyen, risque faible]`

`compute_file_checksums()` est utilisé sur le chemin install alors que seul l'upload
consomme le SHA-1. Soit un paramètre `with_sha1=False`, soit un `compute_sha256()` dédié
côté install. ×1,6 sur ce qui resterait de hachage.

### 4.3 — Rendre `expand` idempotent `[gain fort, risque moyen]`

Écrire un marqueur après extraction, par exemple
`<target>/.agpkg-expanded.json` : `{ "<archive>": "<sha256>" }`, et sauter
`_expand_archive_from_cache()` quand le marqueur correspond et que la cible n'est pas vide.

Point d'attention : cela modifie un contrat implicite (« install produit toujours un arbre
frais »). Proposition : comportement activé par défaut, avec `--force` / `--no-skip-expand`
pour revenir à l'ancien comportement.

### 4.4 — Augmenter les tailles de bloc `[gain faible, risque nul]`

`CHUNK_SIZE` : 1024 → 1 MiB. Blocs de hachage : 4096 → 1 MiB. Et corriger le commentaire sur
le MTU (§2.4).

### 4.5 — Paralléliser les téléchargements `[gain moyen, risque moyen]`

`ThreadPoolExecutor` sur la boucle de `install_packages()`, avec un `--jobs` (défaut 4).
Les téléchargements sont I/O-bound. Pour l'extraction, sérialiser par dossier cible et
paralléliser entre cibles distinctes.

### 4.6 — Instrumenter `[prérequis]`

Aucune mesure de durée n'existe aujourd'hui dans le chemin install. Un simple récapitulatif
en fin d'install (par fichier : taille, téléchargé O/N, durée hachage, durée extraction)
permettrait à chaque projet de quantifier son propre cas — et de valider ces correctifs.

### 4.7 — Mode « confiance au lockfile » `[fonctionnalité, à discuter]`

Même parfaitement optimisé, `install` fait un aller-retour réseau (stat + SHA-256) **par
fichier, à chaque run**. Une option `--offline` / `--locked` qui fait confiance au lockfile
et au cache ramènerait un install inchangé à quelques secondes.

Nous comprenons que cela dépasse la correction de performance et relève d'un arbitrage
produit.

### 4.8 — Déduplication des entrées de lockfile `[gain faible, risque nul]`

Voir §2.6. À traiter de préférence dans `update`.

---

## 5. Ce que nous avons mis en place en attendant

Par transparence, et parce que cela peut servir de banc d'essai aux correctifs ci-dessus :

1. **Correction de notre côté.** `agpkg install` était appelé sans `--groups` alors que la
   liste des groupes nécessaires était déjà calculée. Corrigé : un job ne traite plus que
   les packages dont il a besoin.

2. **Un installeur de contournement.** Un script Python local lit `agpkg.lock.json` et
   applique les actions d'import, en implémentant 4.1 / 4.3 / 4.4 / 4.5 / 4.8. Il
   **réutilise exactement la disposition de cache d'agpkg**
   (`<racine>/<host>/<chemin URL>` + sidecar `.sha256`) afin que les deux outils partagent
   le même cache et que `agpkg install` reste interchangeable — il est d'ailleurs conservé
   en repli automatique.

Nous considérons ce script comme **temporaire**. Dès qu'une version d'agpkg intégrant 4.1 à
4.5 sera disponible, nous le supprimons : nous n'avons aucun intérêt à maintenir une
implémentation parallèle couplée au schéma de lockfile `1.x`.

Nous sommes volontaires pour contribuer les MR si cela vous convient.

---

## 6. Annexe — reproduction des mesures

Les deux scripts suivants sont autonomes (stdlib + `requests`).

### 6.1 Hachage et streaming

```python
import hashlib, http.server, os, tempfile, threading, time
from pathlib import Path
import requests

root = Path(tempfile.mkdtemp()); payload = root / "payload.bin"
block = os.urandom(1024 * 1024)
with payload.open("wb") as f:
    for _ in range(512):
        f.write(block)
size = payload.stat().st_size

def bench(label, fn):
    t = time.monotonic(); fn(); d = time.monotonic() - t
    print(f"{label:45} {d:6.2f}s  {size/1024/1024/d:7.1f} MB/s  {d/(size/1024**3):6.2f} s/GB")

def agpkg_hash():                       # copie exacte de lib/cache.py
    a, b = hashlib.sha256(), hashlib.sha1()
    with payload.open("rb") as f:
        for blk in iter(lambda: f.read(4096), b""):
            a.update(blk); b.update(blk)

def fast_hash():
    a = hashlib.sha256()
    with payload.open("rb") as f:
        for blk in iter(lambda: f.read(1024 * 1024), b""):
            a.update(blk)

bench("agpkg: sha256+sha1, 4 KiB", agpkg_hash)
bench("sha256 seul, 1 MiB", fast_hash)

os.chdir(root)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), http.server.SimpleHTTPRequestHandler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_address[1]}/payload.bin"

def stream(chunk):
    def run():
        with requests.get(url, stream=True) as r, (root / "out.bin").open("wb") as f:
            for d in r.iter_content(chunk):
                f.write(d)
    return run

bench("CHUNK_SIZE = 1024 (actuel)", stream(1024))
bench("CHUNK_SIZE = 1 MiB", stream(1024 * 1024))
srv.shutdown()
```

### 6.2 Extraction, forme réaliste

```python
import os, shutil, tempfile, time, zipfile
from pathlib import Path

root = Path(tempfile.mkdtemp()); src = root / "src"
for i in range(4000):
    sub = src / f"dir{i // 200:03d}"; sub.mkdir(parents=True, exist_ok=True)
    (sub / f"file{i:05d}.bin").write_bytes(os.urandom(128 * 1024))

archive = root / "pkg.zip"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
    for p in sorted(src.rglob("*")):
        if p.is_file():
            zf.write(p, p.relative_to(src))

total = sum(p.stat().st_size for p in src.rglob("*") if p.is_file())
t = time.monotonic()
with zipfile.ZipFile(archive) as zf:
    zf.extractall(root / "out")
d = time.monotonic() - t
print(f"extract {d:.2f}s -> {d/(total/1024**3):.1f} s/GB ({d/4000*1000:.2f} ms/fichier)")
```

