import sys
sys.path.insert(0,'skills/chantier/scripts/cli/tests')
import test_startup_manifest as m
manifest, mp = m._manifest()
folder=mp.parent
for host in ['claude','copilot']:
    for role, wrapper in m._roles().items():
        entry = manifest.get("entries", {}).get(role, {})
        wp = m._wrapper_path(role, host, entry, wrapper)
        req=[folder/manifest["common"],folder/manifest["hosts"][host]["core"],folder/manifest["role_core"],mp]
        if wp is not None: req.append(wp)
        files, sections = m._sections(manifest["startup_sections"].get(role, []), host)
        print("startup-bytes", role, host, m._unique_startup_bytes(req,sections), m._reload_bytes(manifest,host,req,sections))
