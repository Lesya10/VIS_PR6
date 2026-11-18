'''
#task_1
class Student:
    def __init__(self, fio, group):
        self.fio = fio
        self.group = group

    def short(self):
        # Разбиваем ФИО на части
        parts = self.fio.split()
        if len(parts) == 3:
            return f"{parts[0]} {parts[1][0]}. {parts[2][0]}."
        elif len(parts) == 2:
            return f"{parts[0]} {parts[1][0]}."
        else:
            return self.fio

if __name__ == "__main__":
    s1 = Student("Беляева Олеся Андреевна", "09с41")
    s2 = Student("Поляк Эля", "09с42")

    print(s1.fio)
    print(s1.group)
    print(s1.short())
    
    # Доказываем независимость полей
    print(f"{s2.short()} | {s2.group}")

#task_2
class Counter:
    def __init__(self, name):
        self.name = name
        self.value = 0

    def add(self, n=1):
        self.value += n

    def reset(self):
        self.value = 0

    def __str__(self):
        return f"{self.name}: {self.value}"

if __name__ == "__main__":
    accepted = Counter("принято")
    rejected = Counter("отклонено")

    # Увеличиваем "принято"
    accepted.add(7)
    # Увеличиваем "отклонено"
    rejected.add()

    print(accepted)
    print(rejected)

    # Сбрасываем "принято" и показываем, что "отклонено" не изменилось
    accepted.reset()
    print(f"после сброса: {accepted}")

#task3
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    def __str__(self):
        return f"{self.celsius:.1f} C = {self.fahrenheit:.1f} F"

    def __lt__(self, other):
        return self.celsius < other.celsius

if __name__ == "__main__":
    t1 = Temperature(21.5)
    t2 = Temperature(-3.0)
    t3 = Temperature(15.0)

    print(t1)
    print(t2)
    
    temps = [t1, t2, t3]
    
    print("\nпо возрастанию:")
    for t in sorted(temps):
        print(t)
        
    print(f"\nСамый тёплый: {max(temps)}")

#task4
import math

class Figure:
    def __init__(self, name):
        self.name = name

    def area(self):
        return 0

    def __str__(self):
        return f"{self.name}: площадь {self.area():.2f}"

class Rect(Figure):
    def __init__(self, width, height):
        super().__init__("Прямоугольник")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Figure):
    def __init__(self, radius):
        super().__init__("Круг")
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

if __name__ == "__main__":
    figures = [
        Rect(3, 4),
        Circle(2),
        Rect(5, 3)
    ]

    total_area = 0
    for fig in figures:
        print(fig)
        total_area += fig.area()

    print(f"\nОбщая площадь: {total_area:.2f}")
'''
#task5
class AgeError(Exception):
    pass

class Person:
    def __init__(self, name, age):
        if not (0 <= age <= 120):
            raise AgeError(f"Возраст {age} вне границ 0..120")
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age} лет"

if __name__ == "__main__":
    # Тестовые данные
    test_data = [
        ("Беляева Олеся", 19),
        ("Поляк Эля", 200),
        ("Сидоров Пётр", -5)
    ]

    valid_people = []

    for name, age in test_data:
        try:
            p = Person(name, age)
            valid_people.append(p)
        except AgeError as e:
            print(f"Не принято: {name} — {e}")

    print(f"\nПринято: {len(valid_people)}")
    for p in valid_people:
        print(f"  {p}")