import sys
sys.path.insert(0, sys.argv[1])
from gard import *
set_list("FMEDIT-051", "depends_on", add=["SwRS-MDOKFSTUDIO-TRUST-005"])
