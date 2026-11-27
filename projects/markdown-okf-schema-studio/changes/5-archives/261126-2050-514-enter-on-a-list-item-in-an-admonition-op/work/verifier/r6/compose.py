import pathlib, sys

work = pathlib.Path(sys.argv[1])
third = (work / "verify-f9dc2c6-third.md").read_text(encoding="utf-8")
new = (work / "verifier" / "r6" / "new-claims.md").read_text(encoding="utf-8")


def between(start, end):
    return third[third.index(start):third.index(end)]


carry = "_carried from f9dc2c6: same head, and the description text it judges is unchanged (claim F1)._\n\n"

e2 = between("### E2. ", "### E3. ").split("\n", 2)[2]
e2 = e2.replace("E1.", "F5.").replace(": E1.", ": F5.")

e4 = between("### E4. ", "### E5. ").split("\n", 2)[2]
local_start = e4.index("- Local gates.")
local_end = e4.index("- Review. ")
e4 = e4[:local_start] + e4[local_end:]

parts = [new]
parts.append("## Carried claims: the description's unchanged parts\n\n")
parts.append("### E2. The sentences on screenshots and clip in Deliverables and on title clicks in Impacts: VERIFIED (f9dc2c6)\n\n" + carry + e2)
parts.append("### E4. Test plan items Tests, Requirements, Changelog, Review and CI (Local gates is F6): VERIFIED (f9dc2c6)\n\n" + carry + e4)

bullets = between("## Carried claims: the three bullets of the previous pass", "## Files that may be attached")
bullets = bullets.replace("(claim E0)", "(claim F1)").replace("(The description's links as judged then; the posted ones are judged in E3.)", "(The description's links as judged then; the posted ones are judged in F4.)")
parts.append(bullets)

files = between("## Files that may be attached", "## Limits")
files = files.replace("Clip of the branch (the description now carries the GIF as an upload and links the other two, E3):", "Clip of the branch (the description links all three at the head, F4):")
parts.append(files)

parts.append(between("## Limits", "- This pass judged the description"))
parts.append("- This pass judged the description: no test, build, capture or probe of the code was run again.\n\nVERIFIED\n")

out = "".join(parts)
(work / "verify.md").write_text(out, encoding="utf-8", newline="\n")
print("chars", len(out), "left E0:", "claim E0" in out, "NOT VERIFIED mentions:", out.count("NOT VERIFIED"))
