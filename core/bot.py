import json

import httpx

from core.settings import BOT_TOKEN


class Bot:
    token: str = BOT_TOKEN
    #
    # def __init__(self, response: json = None):
    #     self.response = response

    @classmethod
    async def set_webhook(cls, url):
        httpx.post(
            f'https://api.telegram.org/bot{cls.token}/setWebhook?url={url}'
        )

    async def get_response(self, response):
        request = {
            'update_id': response.get('update_id'),
            'message': response.get('message'),
        }
        return request
