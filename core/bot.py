import httpx

from core.settings import BOT_TOKEN
from core.constants import TELEGRAM_API


class Bot:

    def __init__(self):
        self.token: str = BOT_TOKEN

    async def set_webhook(self, url):
        httpx.post(
            f'{TELEGRAM_API}/bot{self.token}/setWebhook?url={url}'
        )

    async def send_message(self, message, chat_id):
        httpx.get(
            f'{TELEGRAM_API}/bot{self.token}/sendMessage?chat_id={chat_id}&text={message}'
        )


class Update:

    def __init__(self, request, bot):
        self.request = request
        self.bot = bot

    def message(self):
        return self.request.get('message').get('message_id')


