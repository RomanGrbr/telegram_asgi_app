from dataclasses import dataclass
from typing import Optional

import httpx

from core.constants import TELEGRAM_API
from core.settings import BOT_TOKEN
from core.message_type import Message, PhotoMessage, IlineKeyboardMessage


@dataclass(slots=True)
class Bot:
    token: str = BOT_TOKEN

    def set_webhook(self, url: str) -> None:
        response = httpx.post(
            f'{TELEGRAM_API}/bot{self.token}/setWebhook?url={url}'
        )
        # print(response)  # Возможно использовать для отладки или уведомления

    async def send_message(
            self, text: str, chat_id: int,
            parse_mode: str = '',
            disable_web_page_preview: bool = False,
            reply_to_message_id: Optional[int] = '',
            reply_markup: str = '',
    ):
        # request = (f'{TELEGRAM_API}/bot{self.token}'
        #            f'/sendMessage?chat_id={chat_id}'
        #            f'&text={text}'
        #            f'&parse_mode={parse_mode}'
        #            f'&disable_web_page_preview={disable_web_page_preview}'
        #            f'&reply_to_message_id={reply_to_message_id}'
        #            f'&reply_markup={reply_markup}')
        request = (f'{TELEGRAM_API}/bot{self.token}'
                   f'/sendMessage?chat_id={chat_id}'
                   f'&text={text}')
        httpx.get(request)

    async def send_contact(self):...

    async def send_file(self):...

    # TODO Реализован не полностью. А может перенести в Update?
    #  Добавить обработку ошибок, директорию сохранения и декодирование
    async def get_file(self, file_id):
        httpx.get(
            f'{TELEGRAM_API}/bot{self.token}/getFile?file_id={file_id}'
        )


class BotBilder:
    handlers: dict = dict()
    handlers_list = []
    bot = Bot()

    def add_handler(self, handler):
        handler = handler()
        for key, value in handler.items():
            self.handlers[key] = value

    def add_handler_v2(self, handler):
        self.handlers_list.append(handler)

    async def updater(self, update):
        if isinstance(update.message, IlineKeyboardMessage):
            pass
        elif isinstance(update.message, Message):
            if update.message.text in self.handlers:
                func = self.handlers[update.message.text]
                await func(update, {'context': None})

    async def updater_v2(self, update):
        for handler in self.handlers_list:
            # print(handler.is_callback(update))
            if handler.is_callback(update):
                await handler.get_callback(update, {'context': None})
