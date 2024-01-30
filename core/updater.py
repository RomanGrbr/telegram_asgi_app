from typing import Optional

from core.application import JSONResponse
from core.message_type import Message
from core.bot import Bot


class ParsMessage:
    def __init__(self, message):
        self.message = Message(message.get('message')) if message.get(
            'message') else None


class Update:
    handlers: dict = dict()

    def __init__(self, request: dict, bot: Bot) -> None:
        self.bot: Bot = bot
        self.update_id: int = request.get('update_id')
        self.data: ParsMessage = ParsMessage(request)

    async def run_handlers(self):
        if self.data.message.text in self.handlers:
            func = self.handlers[self.data.message.text]
            await func(self.data, {'context': None})

    async def reply_text(
            self,
            text: str,
            parse_mode: Optional[str] = '',
            disable_web_page_preview: bool = False,
            reply_to_message_id: Optional[int] = '',
            reply_markup: Optional[dict] = None,
    ):
        if reply_markup:
            _, reply_markup = JSONResponse(content=reply_markup)
        await self.bot.send_message(
            text=text,
            chat_id=self.data.message.chat.id,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
        )

    async def add_handler(self, handler):
        handler = await handler()
        for key, value in handler.items():
            self.handlers[key] = value


class CommandHandler:
    def __init__(self, command: str, func):
        self.command = command
        self.func = func

    async def __call__(self, *args, **kwargs):
        return {self.command: self.func}
