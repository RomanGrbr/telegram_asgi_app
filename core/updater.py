from core import parser
from core.bot import Bot


class Update:
    """Определяет тип полученного сообщения.

    Methods:
        pars_message: Преобразовать сообщение в экземпляр pyhon

    Args:
        request (dict): Запрос полученный от asgi.
        bot (class): Экземпляр бота.

    Attributes:
        MESSAGE_TYPE (dict): Хранит добавленные обработчики.
        bot (class): Экземпляр бота.
        update_id (int): id обновления.
        message (class): Экземпляр сообщения соответствующего типа.

    """
    MESSAGE_TYPE: dict[str: parser.Message] = {
        'text': parser.Message,
        'photo': parser.PhotoMessage,
        'document': parser.DocumentMessage,
        'voice': parser.VoiceMessage,
        'location': parser.LocationMessage,
        'poll': parser.PollMessage,
        'contact': parser.ContactMessage,
        'audio': parser.AudioMessage,
    }

    def __init__(self, request: dict, bot: Bot) -> None:
        self.bot: Bot = bot
        self.update_id: int = request.get('update_id')
        self.message = self.pars_message(request)

    def pars_message(self, request: dict):
        """Преобразует сообщение в класс python."""
        if request.get('callback_query'):
            return parser.IlineKeyboardMessage(
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
