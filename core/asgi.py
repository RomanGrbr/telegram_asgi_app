import json
from collections.abc import Callable, Coroutine
from typing import Any


class ASGIApplication:
    post_urls = dict()

    async def __call__(
            self,
            scope: dict,
            receive: Callable[[], str],
            send: Callable[[dict], Coroutine]
    ) -> None:
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
        Handles the ASGI request. Called via the __call__ method.
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
        """Calls the send function with the received code and data"""
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

    def post(self, url: str) -> Callable[..., Any]:
        """Add addresses for post requests"""
        def _wrapper(func):
            self.post_urls[url] = func
        return _wrapper


class JSONResponse:
    """Serialize dict to bite string"""

    def __init__(self, content: dict, code: int = None) -> None:
        self.content = content
        self.code = 200 if content and not code else code

    async def __call__(self) -> tuple[int | None, bytes]:
        assert type(self.code) is int
        return self.code, json.dumps(self.content, indent=2).encode('utf-8')


class Request:
    """Serialize from bite string to dict"""

    def __init__(self, request):
        self.request = request

    async def __call__(self) -> bytes:
        response = await self.request()
        return json.loads(response['body'].decode('utf-8'))
