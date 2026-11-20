import requests

BASE = "http://127.0.0.1:5000"

print("H1")
r = requests.get(BASE + "/")
print("Код ответа:", r.status_code)
print("Тип r.text:", type(r.text))
print("Тип r.json():", type(r.json()))
print("Название сервиса:", r.json()["servis"])

print("\nH2")
r = requests.get(BASE + "/anketi")
ankety = r.json()
print("Пришло анкет:", len(ankety))
print("ФИО первой:", ankety[0]["fio"])

print("\nH3")
r = requests.get(BASE + "/anketi/99")
print("Код ответа:", r.status_code)
print("r.ok:", r.ok)
if r.status_code == 404:
    print("Сервер ответил:", r.json()["oshibka"])


print("\nH4")
r = requests.get(BASE + "/anketi", params={"tip": "t"})
print("Адрес запроса:", r.url)
for a in r.json():
    print(f"ФИО: {a['fio']}, Кафедра: {a['kafedra']}")

print("\nH5")
for mail in ["ivanov@mail.ru", "kuznetsov.mail.ru"]:
    r = requests.post(BASE + "/proverka", json={"mail": mail})
    print(f"Почта: {mail} | Код: {r.status_code} | prinyato: {r.json().get('prinyato')}")