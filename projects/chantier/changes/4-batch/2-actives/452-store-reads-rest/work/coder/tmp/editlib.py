SRC = r"C:\Users\gaeta\Projets\chantier.worktrees\batch-30-CR-452\skills\chantier\scripts\cli\src\chantier"


class Editor:
    def __init__(self, rel):
        self.path = SRC + "\\" + rel.replace("/", "\\")
        with open(self.path, encoding="utf-8") as f:
            self.s = f.read()

    def r(self, a, b, c=1):
        n = self.s.count(a)
        assert n == c, (a[:80], n)
        self.s = self.s.replace(a, b)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(self.s)
