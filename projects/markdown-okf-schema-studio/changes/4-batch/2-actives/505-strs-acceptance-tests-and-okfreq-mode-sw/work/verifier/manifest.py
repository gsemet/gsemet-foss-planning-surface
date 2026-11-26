"""Verifier of CR-505: print the acceptance manifest of an artifact zip, without extracting it.

usage: python -I manifest.py <artifact.zip>
"""
import json
import sys
import zipfile

with zipfile.ZipFile(sys.argv[1]) as archive:
    names = [n for n in archive.namelist() if n.endswith("acceptance-manifest.json")]
    print("manifests:", names)
    for name in names:
        print(json.dumps(json.loads(archive.read(name).decode("utf-8")), indent=1)[:4000])
