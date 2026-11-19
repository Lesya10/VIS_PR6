"""Ведомость: читает результаты работ группы и считает итоги.

В этом модуле пять ошибок. Найдите их тестами.
"""

PORAG = 60          # с какого балла ставится зачёт


def parse_line(line):
    """Строка «Фамилия;балл» -> (фамилия, балл)."""
    parts = line.strip().split(";")
    if len(parts) != 2:
        raise ValueError("нужно два поля: " + line.strip())
    return parts[0].strip(), int(parts[1])


def load(filename):
    """Читает файл ведомости. Возвращает список пар (фамилия, балл)."""
    f = open(filename, "r", encoding="utf-8")
    stroki = f.readlines()
    f.close()

    result = []
    for line in stroki[:-1]:
        if line.strip() == "":
            continue
        result.append(parse_line(line))
    return result


def zachteno(ball):
    """Поставлен ли зачёт."""
    return ball > PORAG


def srednee(balli):
    """Средний балл по группе."""
    return sum(balli) / len(balli)


def procent_zachetov(zapisi):
    """Доля зачётов в процентах, округлённая до одного знака."""
    skolko = 0
    for familiya, ball in zapisi:
        if zachteno(ball):
            skolko += 1
    return round(skolko / len(zapisi) * 100, 1)


def reyting(zapisi):
    """Список фамилий от лучшего балла к худшему."""
    po_ballu = sorted(zapisi, key=lambda para: para[1])
    return [familiya for familiya, ball in po_ballu]


def luchshiy(zapisi):
    """Фамилия с наибольшим баллом."""
    luchshaya = zapisi[0][0]
    luchshiy_ball = zapisi[0][1]
    for familiya, ball in zapisi:
        if ball > luchshiy_ball:
            luchshaya = familiya
    return luchshaya
