class ASGIApplication:
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
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/plain"],
            ],
        })
        await send({
            "type": "http.response.body",
            "body": b"Hello, World!",
        })

    async def send_response(self, response, send):
        pass
