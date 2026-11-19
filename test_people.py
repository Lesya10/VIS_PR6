import pytest
from people import Person, Student, Teacher, AnketaError
from registry import Registry

# 1. ФИО приводится к одному виду
@pytest.mark.parametrize("raw, expected", [
    ("  иванов   иВАН петрович ", "Иванов Иван Петрович"),
    ("петрова анна", "Петрова Анна"),
    ("сИдоров пётр сергеевич", "Сидоров Пётр Сергеевич"),
    ("кузнецов павел", "Кузнецов Павел")
])
def test_fio_format(raw, expected):
    p = Person(raw, "a@b.ru", "+79211112233")
    assert p.fio == expected

# 2. ФИО из одного слова отклоняется
def test_fio_odno_slovo():
    with pytest.raises(AnketaError):
        Person("Иванов", "a@b.ru", "+79211112233")

# 3. Почта приводится к нижнему регистру
@pytest.mark.parametrize("raw, expected", [
    ("IVANOV@MAIL.RU", "ivanov@mail.ru"),
    ("  Petrov@Yandex.Ru  ", "petrov@yandex.ru")
])
def test_mail_lower(raw, expected):
    p = Person("Иванов Иван", raw, "+79211112233")
    assert p.mail == expected

# 4. Плохая почта отклоняется
@pytest.mark.parametrize("bad_mail", [
    "ivanov.mail.ru",
    "ivanov@mail",
    "@mail.ru",
    "ivanov@.ru"
])
def test_bad_mail(bad_mail):
    with pytest.raises(AnketaError):
        Person("Иванов Иван", bad_mail, "+79211112233")

# 5. Телефон приводится к одному виду
@pytest.mark.parametrize("raw", [
    "+7 (921) 111-22-33",
    "89211112233",
    "7 921 111 22 33",
    "+79211112233"
])
def test_phone_format(raw):
    p = Person("Иванов Иван", "a@b.ru", raw)
    assert p.phone == "+7 (921) 111-22-33"

# 6. Плохой телефон отклоняется
@pytest.mark.parametrize("bad_phone", [
    "+7 (921) 111-22",
    "12345678901",
    "892111122334"
])
def test_bad_phone(bad_phone):
    with pytest.raises(AnketaError):
        Person("Иванов Иван", "a@b.ru", bad_phone)

# 7. Телефон выводится с маской
def test_masked_phone():
    p = Person("Иванов Иван", "a@b.ru", "+79211112233")
    assert p.masked_phone() == "+7 (921) ***-**-33"

# 8. ФИО сокращается до инициалов
def test_short_fio():
    p = Person("Иванов Иван Петрович", "a@b.ru", "+79211112233")
    assert p.short_fio() == "Иванов И. П."
    p2 = Person("Петрова Анна", "a@b.ru", "+79211112233")
    assert p2.short_fio() == "Петрова А."

# 9. Студент и преподаватель отвечают по-разному
def test_role():
    s = Student("Иванов Иван", "a@b.ru", "+79211112233", "09с33")
    t = Teacher("Петров Пётр", "a@b.ru", "+79211112233", "Кафедра И9")
    assert s.role() == "Студент"         # У вас с большой буквы
    assert t.role() == "Преподаватель"   # У вас с большой буквы

# 10. Студент без группы отклоняется
def test_student_bez_gruppy():
    with pytest.raises(AnketaError):
        Student("Иванов Иван", "a@b.ru", "+79211112233", "")

# 11. Строка файла разбирается верно
def test_parse_line_student():
    p = Registry.parse_line("s;Иванов Иван;a@b.ru;+79211112233;09с33")
    assert isinstance(p, Student)
    assert p.extra() == "09с33"

def test_parse_line_teacher():
    p = Registry.parse_line("t;Петров Пётр;a@b.ru;+79211112233;Кафедра И9")
    assert isinstance(p, Teacher)
    assert p.extra() == "Кафедра И9"

# 12. Плохая строка отклоняется
@pytest.mark.parametrize("bad_line", [
    "x;Иванов Иван;a@b.ru;+79211112233;09с33",
    "s;Иванов Иван;a@b.ru",
    ""
])
def test_parse_line_bad(bad_line):
    with pytest.raises(AnketaError):
        Registry.parse_line(bad_line)

#Часть 3
def test_dvoynaya_familiya():
    p = Person("петров-водкин кузьма", "a@b.ru", "+79211112233")
    assert p.fio == "Петров-Водкин Кузьма"

def test_mail_s_probelom():
    with pytest.raises(AnketaError):
        Person("Иванов Иван", "iv anov@mail.ru", "+79211112233")