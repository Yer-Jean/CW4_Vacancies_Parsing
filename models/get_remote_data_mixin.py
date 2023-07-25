import json
import requests

from models.exceptions import GetRemoteDataException


class GetRemoteData:

    @staticmethod
    def get_remote_data(**kwargs) -> dict | None:
        """Метод получает ответ сайта по API в формате JSON.
        В случае успеха возвращает словарь с данными.
        В случае ошибки возвращает None, при этом обрабатываются
        как сетевые(web) исключения, так и ошибки ответа сайта.
        Кроме того, проверяется корректность JSON-формата.
        Все исключения обрабатываются в классе GetRemoteDataException
        """
        try:
            response = requests.get(**kwargs)
        except requests.exceptions.ConnectionError:
            raise GetRemoteDataException('Не найден сайт или ошибка сети')
        except requests.exceptions.HTTPError:
            raise GetRemoteDataException('Некорректный HTTP ответ')
        except requests.exceptions.Timeout:
            raise GetRemoteDataException('Вышло время ожидания ответа')
        except requests.exceptions.TooManyRedirects:
            raise GetRemoteDataException('Превышено максимальное значение перенаправлений')

        if response.status_code != 200:  # Все ответы сайта, кроме - 200, являются ошибочными
            raise GetRemoteDataException(f'Ошибка {response.status_code} - {response.reason}')

        # Пытаемся декодировать JSON
        try:
            data: dict = response.json()
        except json.decoder.JSONDecodeError:
            raise GetRemoteDataException('Ошибка в формате данных')

        # Возвращаем словарь с данными, если не возникло каких-либо ошибок
        return data
