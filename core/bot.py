from dataclasses import dataclass

import httpx

from core.constants import TELEGRAM_API
from core.settings import BOT_TOKEN


@dataclass
class Bot:
    token: str = BOT_TOKEN

    async def set_webhook(self, url):
        httpx.post(
            f'{TELEGRAM_API}/bot{self.token}/setWebhook?url={url}'
        )

    async def send_message(self, message, chat_id):
        httpx.get(
            f'{TELEGRAM_API}/bot{self.token}/sendMessage?chat_id={chat_id}&text={message}'
        )


class BaseMessageChat:
    def __init__(self, data: dict):
        self.id = data.get('id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.username = data.get('username')


class From(BaseMessageChat):
    def __init__(self, mess_from):
        super().__init__(mess_from)
        self.is_bot = mess_from.get('is_bot')
        self.language_code = mess_from.get('language_code')


class Chat(BaseMessageChat):
    def __init__(self, chat):
        super().__init__(chat)
        self.type = chat.get('type')


class Message:
    def __init__(self, message):
        self.message_id = message.get('message_id')
        self.mess_from = From(message.get('from'))
        self.chat = Chat(message.get('chat'))
        self.date = message.get('date')
        self.text = message.get('text')

        # self.photo = message.get('photo')
        # self.document = message.get('document')
        # self.voice = message.get('voice')
        # self.location = message.get('location')
        # self.poll = message.get('poll')
        # self.contact = message.get('contact')
        # self.audio = message.get('audio')
        # self.caption = message.get('caption')


class CallbackQuery:
    def __init__(self, callback_query):
        self.id = callback_query.get('id')


class Update:
    def __init__(self, request, bot):
        self.bot = bot
        self.request = request
        self.update_id = request.get('update_id')
        self.message = Message(request.get('message')) if request.get('message') else None
        self.callback_query = request.get('callback_query')

        # self.entities = self.message.get('entities')
        # self.reply_markup = self.message.get('reply_markup')


    async def mess_from(self):
        return From(self.mess_from)



