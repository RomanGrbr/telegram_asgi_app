import json


class ASGIApplication:
    post_urls = dict()

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            raise ValueError(
                "Can only handle ASGI/HTTP connections, not %s." % scope["type"]
            )
        await self.handle(scope, receive, send)

    async def handle(self, scope, receive, send):
        """
        Handles the ASGI request. Called via the __call__ method.
        """
        response = await receive()
        response = json.loads(response['body'].decode('utf-8'))
        if scope['method'] == 'POST':
            if scope['path'] in self.post_urls:
                body = await self.post_urls[scope['path']](response)
                data, code = await body()
                await self.request(send, data, code)
            else:
                await self.request(send, code=404)
        else:
            await self.request(send, code=405)

    @staticmethod
    async def request(send, code: int, data: str = b''):
        """Calls the send function with the received code and data"""
        await send({
            "type": "http.response.start",
            "status": code,
            "headers": [
                [b"content-type", b"text/plain"],
            ],
        })
        await send({
            "type": "http.response.body",
            "body": data,
        })

    def post(self, url: str):
        """Add addresses for post requests"""
        def _wrapper(function):
            self.post_urls[url] = function
        return _wrapper


class JSONResponse:
    """Serialize dict to bite string"""

    def __init__(self, data: dict, code: int = None):
        self.data = data
        self.code = 200 if data and not code else code

    async def __call__(self):
        assert type(self.code) == int
        return self.code, json.dumps(self.data, indent=2).encode('utf-8')
