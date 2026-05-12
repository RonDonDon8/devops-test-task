import requests
import logging

# 4. Результат скрипта необходимо логировать в консоль.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)


# 2. При получении статус-кодов 4xx и 5xx - генерировать исключительную ситуацию.
class HTTPResponseError(Exception):
    """Кастомное исключение для обработки HTTP ошибок 4xx и 5xx."""
    pass


def fetch_and_process(status_code: int) -> None:
    """Выполняет запрос и маршрутизирует логику в зависимости от ответа."""
    url = f"https://httpstat.us/{status_code}"

    # timeout=10 защищает от бесконечного зависания, если сервис "лежит"
    # allow_redirects=False нужен, чтобы  получить код 3xx, а не конечный 200
    response = requests.get(url, allow_redirects=False, timeout=10)

    code = response.status_code
    body = response.text.strip()

    # 1. При получении статус-кодов 1xx, 2xx, 3xx - логировать содержимое
    if 100 <= code < 400:
        logging.info(f"Успех/Инфо/Редирект -> Статус: {code} | Тело: '{body}'")

    # 2. При получении статус-кодов 4xx и 5xx - генерировать исключение
    elif code >= 400:
        raise HTTPResponseError(f"Ошибка HTTP -> Статус: {code} | Тело: '{body}'")


def main():
    # 3. При вызове скрипта, он должен выполнить 5 разных запросов
    test_codes = [200, 201, 302, 404, 500]

    for code in test_codes:
        logging.info(f"--- Отправка запроса: {code} ---")
        try:
            fetch_and_process(code)
        except HTTPResponseError as e:
            # Перехватываем наше сгенерированное исключение, чтобы скрипт не упал полностью и продолжил выполнять оставшиеся запросы
            logging.error(f"Сгенерировано исключение: {e}")
        except requests.RequestException as e:
            # Защита от падения, если пропал интернет или сервер httpstat.us недоступен
            logging.error(f"Сетевая ошибка (сервер не ответил): {e}")


if __name__ == "__main__":
    main()