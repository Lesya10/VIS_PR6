import requests

class ServerNedostupen(Exception):
    """Своё исключение для проблем с сетью"""
    pass

BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 3

def _request(method, endpoint, **kwargs):
    """Внутренняя функция: таймаут, ловля ошибок, проверка на 500."""
    url = BASE_URL + endpoint
    try:
        response = requests.request(method, url, timeout=TIMEOUT, **kwargs)
        # Если сервер ответил 500 и выше — исключение
        if response.status_code >= 500:
            raise ServerNedostupen(f"Ошибка сервера: код {response.status_code}")
        return response
    except (requests.ConnectionError, requests.Timeout) as e:
        raise ServerNedostupen(f"Сервер недоступен: {e}")

def get_ankety():
    """Забирает все анкеты с сервера"""
    r = _request("GET", "/anketi")
    return r.json()

def get_anketa(nomer):
    """Забирает одну анкету. Если нет, то возвращает None"""
    r = _request("GET", f"/anketi/{nomer}")
    if r.status_code == 404:
        return None
    return r.json()

def proverit_mail(mail):
    """Отправляет почту на /proverka. Возвращает True/False."""
    r = _request("POST", "/proverka", json={"mail": mail})
    # Сервер отвечает 201 (создано/принято) или 200
    if r.status_code in (200, 201):
        return r.json().get("prinyato", False)
    return False

def get_statistika():
    """Забирает статистику сервера."""
    r = _request("GET", "/statistika")
    return r.json()