from dataclasses import dataclass
from typing import Optional

import httpx

from core.constants import TELEGRAM_API
from core.settings import BOT_TOKEN


@dataclass(slots=True)
class Bot:
    token: str = BOT_TOKEN

    async def set_webhook(self, url: str) -> None:
        response = httpx.post(
            f'{TELEGRAM_API}/bot{self.token}/setWebhook?url={url}'
        )
        print(response)  # Возможно использовать для отладки или уведомления

    async def send_message(
            self, text: str, chat_id: int,
            parse_mode: str = '',
            disable_web_page_preview: bool = False,
            reply_to_message_id: Optional[int] = '',
            reply_markup: str = '',
    ):
        request = (f'{TELEGRAM_API}/bot{self.token}'
                   f'/sendMessage?chat_id={chat_id}'
                   f'&text={text}'
                   f'&parse_mode={parse_mode}'
                   f'&disable_web_page_preview={disable_web_page_preview}'
                   f'&reply_to_message_id={reply_to_message_id}'
                   f'&reply_markup={reply_markup}')
        httpx.get(request)

    async def send_contact(self):...

    async def send_file(self):...

    # TODO Реализован не полностью. А может перенести в Update?
    #  Добавить обработку ошибок, директорию сохранения и декодирование
    async def get_file(self, file_id):
        httpx.get(
            f'{TELEGRAM_API}/bot{self.token}/getFile?file_id={file_id}'
        )
