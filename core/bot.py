from dataclasses import dataclass, field

import httpx

from core.handler import Handler
from core.settings import TELEGRAM_API
from core.updater import Update


@dataclass(slots=True)
class Bot:
    """Реализует взаимодействие с API Telegram.

    Methods:
        set_webhook: Установить вебхук.
        send_message: Отправить сообщение.
        send_contact: Отправить контакт.
        send_file: Отправить файл.
        get_file: Получить файл.

    Args:
        token (str): Значение полученное у BotFather.

    Attributes:
        token (str): Значение полученное у BotFather.

    """

    def __init__(self, token: str) -> None:
        self.token: str = token

    def set_webhook(self, url: str) -> None:
        """Регистрирует адрес вебхука в Telegram."""
        response = httpx.post(
            f'{TELEGRAM_API}/bot{self.token}/setWebhook?url={url}'
        )
        # print(response)  # Возможно использовать для отладки или уведомления

    async def send_message(
            self, text: str, chat_id: int,
            parse_mode: str = '',
            disable_web_page_preview: bool = False,
            reply_to_message_id: int = '',
            reply_markup: str = '',
    ):
        """Отправляет текстовое сообщение в Telegram.

        Args:
            text (str): Сообщение для отправки.
            chat_id (int): id чата для отправки сообщения.
            parse_mode (str): Оформление текста сообщения HTML или Markdown.
            disable_web_page_preview (bool): Показ привью отправленной ссылки.
            reply_to_message_id (int): Идентификатор сообщения для ответа.
            reply_markup (str): Тип быстрого ответа.

        """
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

    async def send_contact(self):
        """Отправляет контакт в Telegram."""
        pass

    async def send_file(self):
        """Отправляет файл в Telegram."""
        pass

    # TODO Реализован не полностью. А может перенести в Update?
    #  Добавить обработку ошибок, директорию сохранения и декодирование
    async def get_file(self, file_id: int):
        """Получает файл по его id

        Args:
            file_id (int): id файла для загрузки из полученного сообщения.

        """
        httpx.get(
            f'{TELEGRAM_API}/bot{self.token}/getFile?file_id={file_id}'
        )


@dataclass(slots=True)
class BotBilder:
    """Создает экземпляр бота и управляет обработчиками.

    Methods:
        add_handler: Добавить хендлер в обработку.
        updater: Вызвать хендлер.

    Args:
        token (str): Значение полученное у BotFather

    Attributes:
        handlers_list (list): Хранит добавленные обработчики.
        bot: (class): Экземпляр бота

    """

    handlers_list: list = field(default_factory=list)

    def __init__(self, token: str) -> None:
        self.bot: Bot = Bot(token)

    def add_handler(self, handler: Handler) -> None:
        """Добавляет хендлер в обработчик."""
        self.handlers_list.append(handler)

    async def updater(self, update: Update) -> None:
        """Передает запрос соответствующему хендлеру."""
        for handler in self.handlers_list:
            if handler.respond(update):
                return await handler.get_callback(update, {'context': None})
