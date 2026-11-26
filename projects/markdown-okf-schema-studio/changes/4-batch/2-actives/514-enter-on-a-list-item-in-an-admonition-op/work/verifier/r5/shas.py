import json, pathlib, re, sys

work = pathlib.Path(sys.argv[1])
body = json.loads((work / "verifier/r5/pr-540-f9dc2c6-closing.json").read_text(encoding="utf-8"))["body"]
lines = body.replace("\r\n", "\n").split("\n")
start = lines.index("## Impacts")
end = lines.index("## Blast radius")
sha = re.compile(r"(?<![0-9a-f-])(?=[0-9a-f]*[a-f])(?=[0-9a-f]*[0-9])[0-9a-f]{7,40}(?![0-9a-f-])")
print("== SHA named in the Impacts section (link targets removed, alt texts and text kept)")
for number in range(start, end):
    visible = re.sub(r"\]\([^)]*\)", "]", lines[number])
    print(number + 1, "text:", sha.findall(visible), "| link targets:", sorted({s for u in re.findall(r"\]\((https://github\.com/gsemet/[^)]*)\)", lines[number]) for s in sha.findall(u)}), "|", visible[:90])
print("== SHA named anywhere in the body, link targets removed")
for number, line in enumerate(lines, 1):
    visible = re.sub(r"\]\([^)]*\)", "]", line)
    found = sha.findall(visible)
    if found:
        print(number, found, visible[:90])
print("5f0746d in body:", "5f0746d" in body)
