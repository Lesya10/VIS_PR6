from registry import Registry

def print_table(registry):
    # Ширины колонок
    w_num, w_fio, w_role, w_extra, w_phone = 3, 28, 15, 15, 19
    
    print(f"{'№':>{w_num}}  {'ФИО':<{w_fio}} {'Роль':<{w_role}} "
          f"{'Группа/кафедра':<{w_extra}} {'Телефон':<{w_phone}}")
    print("-" * 85)

    # Сортируем принятых по ФИО
    registry.good.sort()

    for i, p in enumerate(registry.good, 1):
        fio = p.fio
        if len(fio) > w_fio:
            fio = fio[:w_fio-1] + "…"
        
        print(f"{i:>{w_num}}  {fio:<{w_fio}} {p.role():<{w_role}} "
              f"{p.extra():<{w_extra}} {p.masked_phone():<{w_phone}}")
    print("-" * 85)


def main():
    reg = Registry()
    
    if not reg.load("anketa.txt"):
        print("Ошибка: Файл anketa.txt не найден. Завершение работы!")
        return

    print_table(reg)

    print(f"\nОтклонено строк: {len(reg.errors)}")
    for lineno, raw, reason in reg.errors:
        print(f"  строка {lineno}: {reason}")
        print(f"      {raw}")

    print(f"\nПринято: {len(reg)} | Отклонено: {len(reg.errors)}")

    print("\nПо ролям:")
    for role, count in sorted(reg.get_stats_by_role().items()):
        print(f"  {role:<15} {count}")

    print("\nПо группам:")
    for extra, count in sorted(reg.get_stats_by_extra().items()):
        print(f"  {extra:<15} {count}")

    reg.save_ok()
    reg.save_errors()
    print("\nСохранено: ok.txt и errors.txt")

if __name__ == "__main__":
    main()