class AnketaError(Exception):
    """Своё исключение для ошибок в анкетах."""
    pass

class Person:
    def __init__(self, raw_fio, raw_mail, raw_phone):
        self.fio = self.validate_fio(raw_fio)
        self.mail = self.validate_mail(raw_mail)
        self.phone = self.validate_phone(raw_phone)

    @staticmethod
    def validate_fio(raw):
        fio = " ".join(part.strip() for part in raw.split()).title()
        if len(fio.split()) < 2:
            raise AnketaError("в ФИО меньше двух слов")
        return fio

    @staticmethod
    def validate_mail(raw):
        mail = raw.strip().lower()
        if mail.count("@") != 1:
            raise AnketaError(f"Почта неверная: {mail}")
        local, domain = mail.split("@")
        if not local or not domain or "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise AnketaError(f"Почта неверная: {mail}")
        return mail

    @staticmethod
    def validate_phone(raw):
        digits = "".join(c for c in raw if c.isdigit())
        if len(digits) != 11 or digits[0] not in ("7", "8"):
            raise AnketaError(f"телефон неверный: {raw.strip()}")
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"

    def short_fio(self):
        parts = self.fio.split()
        if len(parts) == 2:
            return f"{parts[0]} {parts[1][0]}."
        return f"{parts[0]} {parts[1][0]}. {parts[2][0]}."

    def masked_phone(self):
        digits = "".join(c for c in self.phone if c.isdigit())
        return f"+7 ({digits[1:4]}) ***-**-{digits[-2:]}"

    # Заглушки для наследников
    def role(self):
        return "человек"

    def extra(self):
        return ""

    def __str__(self):
        return f"{self.fio}"

    def __lt__(self, other):
        return self.fio < other.fio


