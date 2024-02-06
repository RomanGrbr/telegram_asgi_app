from core import message_type
from core.bot import Bot


class Update:
    MESSAGE_TYPE = {
        'text': message_type.Message,
        'photo': message_type.PhotoMessage,
        'document': message_type.DocumentMessage,
        'voice': message_type.VoiceMessage,
        'location': message_type.LocationMessage,
        'poll': message_type.PollMessage,
        'contact': message_type.ContactMessage,
        'audio': message_type.AudioMessage,
    }

    def __init__(self, request: dict, bot: Bot) -> None:
        self.bot = bot
        self.update_id: int = request.get('update_id')
        self.message = self.pars_message(request)

    def pars_message(self, request):
        if request.get('callback_query'):
            return message_type.IlineKeyboardMessage(
                request.get('callback_query'))
        for key, value in self.MESSAGE_TYPE.items():
            if key in request.get('message'):
                return value(request.get('message'))

    # async def reply_text(
    #         self,
    #         text: str,
    #         parse_mode: str = '',
    #         disable_web_page_preview: bool = False,
    #         reply_to_message_id: int = '',
    #         reply_markup: Optional[dict | str] = None,
    # ):
    #     if reply_markup:
    #         reply_markup = Response(content=reply_markup)
    #     await self.bot.send_message(
    #         text=text,
    #         chat_id=self.data.message.chat.id,
    #         parse_mode=parse_mode,
    #         disable_web_page_preview=disable_web_page_preview,
    #         reply_to_message_id=reply_to_message_id,
    #         reply_markup=reply_markup,
    #     )


class Handler:
    # __slots__ = 'command', 'callback'
    command = None

    def __init__(self, command: str, callback):
        self._add_command(command)
        self.callback = callback

    @classmethod
    def is_callback(cls, update):
        # print(update.message.text)
        if update.message.text == cls.command:
            return True
        else:
            return False

    # @classmethod
    async def get_callback(self, update, context):
        await self.callback(update, context)

    @classmethod
    def _add_command(cls, command):
        cls.command = command


class MessageStrongHandler(Handler):
    def __call__(self, *args, **kwargs):
        return {self.command: self.callback}


class CommandHandler(Handler):
    def __call__(self, *args, **kwargs):
        return {self.get_command(): self.callback}

    def get_command(self):
        return f'/{self.command}'
