import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rep import rep

os.chdir(sys.argv[1])
rep("docs/cr-lifecycle-simple-texts.md", "\n🤵 with 👤 you\n", "\n🤵 or 🔥 with 👤 you\n")
print("ok")
