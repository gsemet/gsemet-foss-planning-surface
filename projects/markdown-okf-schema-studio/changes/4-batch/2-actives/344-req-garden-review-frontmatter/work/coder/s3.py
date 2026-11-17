import sys
sys.path.insert(0, sys.argv[1])
from gard import *
S = "StRS-MDOKFSTUDIO-"
def rm(swrs, *strs, add=()):
    set_list(swrs, "derives_from", remove=[S + s for s in strs])
rm("BLOCK-041", "FMEDIT-001", "FMEDIT-008", "REVIEW-008")
rm("BLOCK-058", "FMEDIT-001", "FMEDIT-008")
rm("BLOCK-109", "FMEDIT-008")
rm("TRUST-005", "FMEDIT-008")
rm("TRUST-065", "FMEDIT-008", "REVIEW-015")
set_list("BLOCK-109", "relates_to", add=[S + "FMEDIT-008"], after="depends_on")
rm("FMSCHEMA-084", "FMEDIT-005")
set_list("FMSCHEMA-084", "relates_to", add=[S + "FMEDIT-005"])
set_list("FMSCHEMA-091", "relates_to", add=[S + "FMSCHEMA-001"])
set_list("FMSCHEMA-001", "derives_from", remove=[S + "FMSCHEMA-002"])
for i in ("006", "008", "009"):
    set_list("REVIEW-" + i, "derives_from", remove=[S + "REVIEW-017"], add=[S + "REVIEW-018"])
