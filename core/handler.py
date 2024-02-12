from collections.abc import Callable
from typing import Any
import re
import os

from core.updater import Update
from core.settings import BASE_DIR, MEDIA_ROOT


class Handler:
    """Базовый хендлер.

    Вызывает функцию callback если запрос соответствует заданному trigger.

    Methods:
        respond: Определить соответствует ли запрос trigger, если да то 'True'
        get_callback: Вызвать заданную функцию в атрибуте 'callback'
        _add_command: Установить триггер 'trigger' для вызова 'callback'

    Args:
        callback (def): Функция реагирующая на заданную команду 'trigger'
        trigger (str): Триггер для вызова функции

    Attributes:
        callback (def): Функция реагирующая на заданную команду 'trigger'
        trigger (str): Триггер для вызова функции

    """

    __slots__ = 'callback', 'trigger'

    def __init__(self, callback: Callable, trigger: str = '') -> None:
        self.callback = callback
        self.trigger = self._add_command(trigger)

    def respond(self, update: Update) -> bool:
        """Проверить соответствует ли запрос триггеру."""
        return True

    async def get_callback(self, update: Update, context: dict) -> Any:
        """Вызвать назначенную функцию."""
        await self.callback(update, context)

    def _add_command(self, trigger: str) -> str:
        """Добавить триггер для хендлера."""
        return trigger


class MessageAnyHandler(Handler):
    """Хендлер для всех типов сообщений."""

    def respond(self, update: Update) -> bool:
        """Проверить соответствует ли запрос триггеру."""
        return hasattr(update.message, 'text')


class MessageLowerHandler(MessageAnyHandler):
    """Хендлер соответствия сообщению без учета регистра."""

    def respond(self, update: Update) -> bool:
        """Проверить соответствует ли запрос триггеру."""
        return (super().respond(update) and
                update.message.text.lower() == self.trigger.lower())


class MessageStrongHandler(MessageAnyHandler):
    """Хендлер строгого соответствия сообщению."""

    def respond(self, update: Update) -> bool:
        """Проверить соответствует ли запрос триггеру."""
        return super().respond(update) and update.message.text == self.trigger


class MessageRegexHandler(MessageAnyHandler):
    """Хендлер соответствия сообщения регулярному сообщению."""

    def respond(self, update: Update) -> bool:
        """Проверить соответствует ли запрос регулярному выражению триггера."""
        return (super().respond(update) and
                re.fullmatch(self.trigger, update.message.text))


class CommandHandler(MessageStrongHandler):
    """Хендлер обрабатывающий команды начинающиеся с '/'"""

    def _add_command(self, trigger: str) -> str:
        """Добавить триггер для хендлера."""
        return trigger if trigger.startswith('/') else f'/{trigger}'


class FileHandler(Handler):
    """Хендлер обработки файлов.

     Methods:
        run_upload: Загрузка файла, используя метод get_file экземпляра bot

    Args:
        path (str): Директория для загрузки файла.
        receive (bool): Выполнить загрузку.

    Attributes:
        path (str): Директория для загрузки файла.
        receive (bool): Выполнить загрузку.

    """

    __slots__ = 'path', 'receive'

    def __init__(
            self,
            callback: Callable,
            trigger: str = '',
            path: str = MEDIA_ROOT,
            receive: bool = False
    ) -> None:
        super().__init__(callback, trigger)
        self.path: str = os.path.join(BASE_DIR, path)
        self.receive: bool = receive

    async def get_callback(self, update: Update, context: dict) -> Any:
        """Вызвать назначенную функцию и загрузить файл."""
        await super().callback(update, context)
        if self.receive:
            for file in update.message.files:
                await self.run_upload(update, file)

    async def run_upload(self, update: Update, file: str) -> None:
        """Загрузить файл."""
        await update.bot.get_file(file, self.path)


class PhotoHandler(FileHandler):
    """Хендлер обрабатывающий фотографии."""

    def respond(self, update: Update) -> bool:
        """Проверить содержит ли запрос фотографии."""
        return hasattr(update.message, 'photo')


class DocumentHandler(FileHandler):
    """Хендлер обрабатывающий документы."""

    def respond(self, update: Update) -> bool:
        """Проверить содержит ли запрос документ."""
        return hasattr(update.message, 'document')


class VoiceHandler(FileHandler):
    """Хендлер обрабатывающий аудио сообщения."""

    def respond(self, update: Update) -> bool:
        """Проверить содержит ли запрос аудио сообщение."""
        return hasattr(update.message, 'voice')


class AudioHandler(FileHandler):
    """Хендлер обрабатывающий музыку."""

    def respond(self, update: Update) -> bool:
        """Проверить содержит ли запрос музыку."""
        return hasattr(update.message, 'audio')


class LocationHandler(Handler):
    """Хендлер геопозиции."""

    def respond(self, update: Update) -> bool:
        """Проверить содержит ли запрос геопозицию."""
        return hasattr(update.message, 'location')


class ContactHandler(Handler):
    """Хендлер контактов."""

    def respond(self, update: Update) -> bool:
        """Проверить содержит ли запрос контакт."""
        return hasattr(update.message, 'contact')


class PollHandler(Handler):
    """Хендлер опросов."""

    def respond(self, update: Update) -> bool:
        """Проверить содержит ли запрос опрос."""
        return hasattr(update.message, 'poll')
