import sys
sys.argv=[sys.argv[0],"none"]+sys.argv[1:]
exec(open(sys.argv[0].replace("r3_t.py","r3_scan.py")).read().split("if __name__")[0])
for i in sys.argv[2:]:
    for pre in ("SwRS-","StRS-"):
        k=pre+"MDOKFSTUDIO-"+i
        if k in reqs: print(i, reqs[k]["req_lifecycle"], "|", reqs[k]["title"]); 
