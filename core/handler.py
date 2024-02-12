from collections.abc import Callable
from typing import Any

from core.updater import Update


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
    pass


class MessageLowerHandler(Handler):
    """Хендлер соответствия сообщению без учета регистра."""

    def respond(self, update: Update) -> bool:
        """Проверить соответствует ли запрос триггеру."""
        return update.message.text.lower() == self.trigger.lower()


class MessageStrongHandler(Handler):
    """Хендлер строгого соответствия сообщению."""

    def respond(self, update: Update) -> bool:
        """Проверить соответствует ли запрос триггеру"""
        return update.message.text == self.trigger


class CommandHandler(MessageStrongHandler):
    """Хендлер обрабатывающий команды начинающиеся с '/'"""

    def _add_command(self, trigger: str) -> str:
        """Добавить триггер для хендлера"""
        return trigger if trigger.startswith('/') else f'/{trigger}'
