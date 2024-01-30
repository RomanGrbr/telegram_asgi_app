from dataclasses import dataclass
from typing import Optional

import httpx

from core.constants import TELEGRAM_API
from core.settings import BOT_TOKEN
from core.message_type import Message


@dataclass(slots=True)
class Bot:
    token: str = BOT_TOKEN

    async def set_webhook(self, url):
        httpx.post(
            f'{TELEGRAM_API}/bot{self.token}/setWebhook?url={url}'
        )

    async def send_message(
            self, message, chat_id, parse_mode: Optional[str, None] = None
    ):
        request = (f'{TELEGRAM_API}/bot{self.token}'
                   f'/sendMessage?chat_id={chat_id}&text={message}')
        if parse_mode.lower() == 'html':
            httpx.get(f'{request}&parse_mode=HTML')
        elif parse_mode.lower() == 'markdown':
            httpx.get(f'{request}&parse_mode=Markdown')
        else:
            httpx.get(request)

    # TODO Реализован не полностью,
    #  добавить обработку ошибок, директорию сохранения и декодирование
    async def get_file(self, file_id):
        httpx.get(
            f'{TELEGRAM_API}/bot{self.token}/getFile?file_id={file_id}'
        )


class Update:
    __slots__ = (
        'bot', 'request', 'update_id', 'message',
        'callback_query', 'chat_instance'
    )

    def __init__(self, request: dict, bot) -> None:
        self.bot = bot
        self.request = request
        self.update_id = request.get('update_id')
        self.message = Message(request.get('message')) if request.get('message') else None
        # self.callback_query = CallbackQuery(request.get('callback_query')) if request.get('callback_query') else None
        self.chat_instance = request.get('chat_instance')

    async def reply_text(self, text):
        await self.bot.send_message(message=text, chat_id=self.message.chat.id)
