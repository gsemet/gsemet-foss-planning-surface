import sys
sys.path.insert(0, sys.argv[1])
import gard
orig = gard.read
import merge
def rd(p):
    t = p.read_bytes().decode("utf-8")
    return t
merge.read = rd
merge.write = lambda p, t: p.write_bytes(t.encode("utf-8"))
merge.refs_fix({"REVIEW-069": "REVIEW-054", "REVIEW-070": "REVIEW-074", "REVIEW-071": "REVIEW-074",
          "REVIEW-101": "REVIEW-100", "REVIEW-216": "REVIEW-017", "REVIEW-156": "REVIEW-152",
          "REVIEW-178": "REVIEW-186", "REVIEW-007": "REVIEW-006", "REVIEW-005": "REVIEW-009",
          "REVIEW-010": "REVIEW-009", "REVIEW-200": "REVIEW-195", "REVIEW-203": "REVIEW-195",
          "REVIEW-208": "REVIEW-207", "FMEDIT-054": "FMEDIT-016", "FMSCHEMA-060": "FMSCHEMA-050"})
