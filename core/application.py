import json
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
# from typing import Any


@dataclass
class ASGIApplication:
    """Приложение реализующее основные методы взаимодействия с ASGI сервером.

    Methods:
        handle: Обработать запрос от ASGI.
        request: Отправить ответ используя функцию send.
        post: Зарегистрировать url адрес для POST запросов.

    Attributes:
        post_urls (dict): url адреса для обработки POST запросов.

    """
    post_urls: dict = field(default_factory=dict)

    async def __call__(
            self,
            scope: dict,
            receive: Callable[[], str],
            send: Callable[[dict], Coroutine]
    ) -> None:
        """Вызывается сервером ASGI.

        Args:
            scope (dict): Передаваемая в области действия соединения информация
            receive: Входящий запрос.
            send: Функция отправки ответа.

        Raises:
            ValueError: Если тип не соответствует http

        """
        if scope['type'] != 'http':
            raise ValueError(
                f'Can only handle ASGI/HTTP connections, not {scope["type"]}.'
            )
        await self.handle(scope, receive, send)

    async def handle(
            self,
            scope: dict,
            receive: Callable[[], str],
            send: Callable[[dict], Coroutine]
    ) -> None:
        """
        Обрабатывает запрос ASGI. Вызывается с помощью метода __call__.

        Args:
            scope (dict): Передаваемая в области действия соединения информация
            receive: Входящий запрос
            send: Функция отправки ответа.

        """
        request = Request(receive)
        if scope['method'] == 'POST':
            if scope['path'] in self.post_urls:
                body = await self.post_urls[scope['path']](await request())
                data, code = await body()
                await self.request(send, data, code)
            else:
                await self.request(send, code=404)
        else:
            await self.request(send, code=405)

    @staticmethod
    async def request(
            send: Callable[[dict], Coroutine], code: int, data: bytes = b''
    ) -> None:
        """Вызывает функцию отправки с полученным кодом и данными.

        Args:
            send: Функция отправки ответа
            code (int): HTTP код ответа
            data (bytes): Строка ответа

        """
        await send({
            "type": "http.response.start",
            "status": code,
            "headers": [
                [b"content-type", b"application/json"],
            ],
        })
        await send({
            "type": "http.response.body",
            "body": data,
        })

    def post(self, url: str) -> Callable[..., ...]:
        """Добавляет url адреса для обработки POST запросов.

        Декоратор с параметром url

        Args:
            url (str): url адрес.

        """
        def _wrapper(func):
            """Добавляет декарируемую функцию в список обработки url адресов"""
            self.post_urls[url] = func
        return _wrapper


@dataclass
class Response:
    """Преобразование словаря в строку байт.

    Args:
        content (dict): Словарь для преобразования.

    """
    content: dict

    async def __call__(self) -> bytes:
        return json.dumps(self.content, indent=2).encode('utf-8')


@dataclass
class JSONResponse:
    """Преобразование словаря в строку байт.

    Args:
        content (dict): Словарь для преобразования.

    """
    content: dict
    code: int = 200

    async def __call__(self) -> tuple[int | None, bytes]:
        assert type(self.code) is int
        return self.code, json.dumps(self.content, indent=2).encode('utf-8')


@dataclass
class Request:
    """Преобразование строки байт в словарь.

    Args:
        receive: Функция возвращающая строку запроса.

    """
    receive: Callable[[], ...]

    async def __call__(self) -> bytes:
        response = await self.receive()
        return json.loads(response['body'].decode('utf-8'))
