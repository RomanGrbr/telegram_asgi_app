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
        if scope['method'] == 'POST':
            if scope['path'] in self.post_urls:
                await send({
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [
                        [b"content-type", b"text/plain"],
                    ],
                })
                await send({
                    "type": "http.response.body",
                    "body": await self.post_urls[scope['path']](receive),
                })
            else:
                await send({
                    "type": "http.response.start",
                    "status": 404,
                    "headers": [
                        [b"content-type", b"text/plain"],
                    ],
                })
        else:
            await send({
                "type": "http.response.start",
                "status": 405,
                "headers": [
                    [b"content-type", b"text/plain"],
                ],
            })

    def post(self, url):
        """Add addresses for post requests"""
        def _wrapper(function):
            self.post_urls[url] = function
        return _wrapper
