import json
import sys
import os
from client import get_ankety, get_statistika, proverit_mail, ServerNedostupen
from people import Student, Teacher, AnketaError
from registry import Registry

def process_ankety_from_server(ankety_data):
    """Превращает список словарей с сервера в объекты классов"""
    reg = Registry()
    for i, item in enumerate(ankety_data, 1):
        tip = item.get("tip")
        try:
            if tip == "s":
                p = Student(item["fio"], item["mail"], item["phone"], item.get("gruppa", ""))
            elif tip == "t":
                p = Teacher(item["fio"], item["mail"], item["phone"], item.get("kafedra", ""))
            else:
                raise AnketaError(f"неизвестный тип: {tip}")
            reg.add(p)
        except (AnketaError, KeyError) as e:
            # Если объект не создался, записываем в брак
            reg.errors.append((i, str(item), str(e)))
    return reg

def print_table(reg):
    if not reg.good:
        print("Нет принятых анкет")
        return
    print(f"\n{'№':>3} {'ФИО':<28} {'Роль':<15} {'Группа/кафедра':<15} {'Телефон':<19}")
    print("-" * 85)
    reg.good.sort()
    for i, p in enumerate(reg.good, 1):
        print(f"{i:>3} {p.fio:<28} {p.role():<15} {p.extra():<15} {p.masked_phone():<19}")

def main():
    source = "Сервер"
    try:
        #Пытаемся забрать данные с сервера
        ankety_data = get_ankety()
        reg = process_ankety_from_server(ankety_data)
        
        #Запрашиваем статистику у сервера
        server_stat = get_statistika()
        
    except ServerNedostupen as e:
        #Сервер недоступен, тогда переключаемся на файл
        print(f"Внимание! {e}")
        print("Переключаемся на запасной источник — файл anketa.txt...")
        source = "Файл anketa.txt"
        reg = Registry()
        if not reg.load("anketa.txt"):
            print("Ошибка: Сервер недоступен и файл anketa.txt не найден. Завершение работы.")
            sys.exit(1)
        server_stat = None

    #Печатаем таблицу принятых анкет
    print(f"\nИсточник данных: {source}")
    print_table(reg)
    
    #Печатаем список отклоненных с причинами
    print(f"\nОтклонено строк: {len(reg.errors)}")
    for lineno, raw, reason in reg.errors:
        print(f"  строка {lineno}: {reason}")
        # Если данные с сервера, выводить огромный JSON в брак, выводим только причину
        if source == "Файл anketa.txt":
            print(f"      {raw}")

    print(f"\nПринято: {len(reg)} | Отклонено: {len(reg.errors)}")
    
    # Вывод сводки по ролям
    print("\nПо ролям:")
    for r, c in reg.get_stats_by_role().items():
        print(f"  {r}: {c}")

    # Вывод статистики сервера рядом
    if server_stat:
        print("\nСтатистика сервера:")
        print(f"  Всего анкет: {server_stat['vsego']}")
        for rol, count in server_stat['po_rolyam'].items():
            print(f"  {rol}: {count}")

    #Отправляем почту каждой принятой анкеты на /proverka
    print("\nПроверка почты на сервере:")
    for p in reg.good:
        result = proverit_mail(p.mail)
        print(f"  {p.mail} - {'Принята' if result else 'Отклонена'}")

    #Сохраняем итог в файл otchet.json
    otchet = {
        "istochnik": source,
        "prinyato": len(reg),
        "otkloneno": len(reg.errors),
        "spisok_prinyatyh": [p.fio for p in reg.good]
    }
    with open("otchet.json", "w", encoding="utf-8") as f:
        json.dump(otchet, f, ensure_ascii=False, indent=2)
    print("\nОтчет сохранен в otchet.json")

if __name__ == "__main__":
    main()