import json, sys, zipfile
src, dst = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "extension/package.json":
            manifest = json.loads(data)
            manifest["capabilities"]["agentsWindow"] = {"supported": True}
            data = json.dumps(manifest, indent=2).encode()
        zout.writestr(item, data)
print("patched", dst)
