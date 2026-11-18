from people import Person, Student, Teacher, AnketaError

class Registry:
    def __init__(self):
        self.good = []
        self.errors = []

    def add(self, person):
        self.good.append(person)

    def load(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return False

        for lineno, raw in enumerate(lines, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                person = self.parse_line(line)
                self.add(person)
            except AnketaError as e:
                self.errors.append((lineno, line, str(e)))
        return True

    @staticmethod
    def parse_line(line):
        fields = line.split(";")
        if len(fields) != 5:
            raise AnketaError(f"полей не пять (а {len(fields)})")

        typ, fio, mail, phone, extra = [f.strip() for f in fields]

        if typ == "s":
            return Student(fio, mail, phone, extra)
        elif typ == "t":
            return Teacher(fio, mail, phone, extra)
        else:
            raise AnketaError(f"Неизвестный тип: {typ}")

    def get_stats_by_role(self):
        stats = {}
        for p in self.good:
            r = p.role()
            stats[r] = stats.get(r, 0) + 1
        return stats

    def get_stats_by_extra(self):
        stats = {}
        for p in self.good:
            e = p.extra()
            if e:  # чтобы не считать пустые
                stats[e] = stats.get(e, 0) + 1
        return stats

    def save_ok(self, filename="ok.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for p in self.good:
                f.write(f"{p.fio};{p.mail};{p.phone};{p.extra()}\n")

    def save_errors(self, filename="errors.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for lineno, raw, reason in self.errors:
                f.write(f"строка {lineno}: {reason}\n{raw}\n")

    def __len__(self):
        return len(self.good)