import pytest
from registry import Registry
from people import Student

@pytest.fixture
def journal(tmp_path):
    f = tmp_path / "test_anketa.txt"
    content = (
        "s;Иванов Иван;ivanov@mail.ru;+79211112233;09с33\n"
        "t;Петров Пётр;petrov@mail.ru;+79211112233;Кафедра И9\n"
        "s;Сидорова Анна;sidorova@mail.ru;+79211112233;09с33\n"
        "s;Ошибка;bad-mail;+79211112233;09с33\n"
        "t;Ошибка 2;ok@mail.ru;123;Кафедра\n"
        "x;Ошибка 3;ok@mail.ru;+79211112233;Пусто\n"
    )
    f.write_text(content, encoding="utf-8")
    reg = Registry()
    reg.load(f)
    return reg

def test_empty_registry_len():
    reg = Registry()
    assert len(reg) == 0

def test_loaded_len(journal):
    assert len(journal) == 3

def test_errors_count(journal):
    assert len(journal.errors) == 3

def test_errors_line_numbers(journal):
    lines = [err[0] for err in journal.errors]
    assert lines == [4, 5, 6]

def test_load_nonexistent_file():
    reg = Registry()
    assert reg.load("no_such_file.txt") is False
    assert len(reg) == 0

def test_stats_by_role(journal):
    stats = journal.get_stats_by_role()
    # Внимание: у вас роли с большой буквы!
    assert stats == {"Студент": 2, "Преподаватель": 1}

def test_stats_by_extra(journal):
    stats = journal.get_stats_by_extra()
    # Внимание: группы у вас в нижнем регистре, а кафедра - Title Case
    assert stats == {"09с33": 2, "Кафедра И9": 1}

def test_iter_registry(journal):
    count = 0
    for p in journal:
        count += 1
    assert count == 3

def test_sort_by_alphabet(journal):
    journal.good.sort()
    fios = [p.fio for p in journal.good]
    assert fios == ["Иванов Иван", "Петров Пётр", "Сидорова Анна"]

def test_save_ok(journal, tmp_path):
    out = tmp_path / "ok.txt"
    journal.save_ok(out)
    lines = out.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 3
    assert "Иванов Иван" in lines[0]

def test_save_errors(journal, tmp_path):
    out = tmp_path / "errors.txt"
    journal.save_errors(out)
    text = out.read_text(encoding="utf-8")
    assert "строка 4:" in text
    assert "строка 5:" in text

#Часть 3
def test_sort_with_yo():
    reg = Registry()
    p1 = Student("Яковлева Анна", "a@b.ru", "+79211112233", "1")
    p2 = Student("Ёлкина Мария", "a@b.ru", "+79211112233", "1")
    p3 = Student("Абрамова Ольга", "a@b.ru", "+79211112233", "1")
    reg.add(p1)
    reg.add(p2)
    reg.add(p3)
    
    reg.good.sort()
    fios = [p.fio for p in reg.good]
    
    assert fios == ["Абрамова Ольга", "Ёлкина Мария", "Яковлева Анна"]