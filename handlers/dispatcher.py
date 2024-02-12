from .comands import help_handler, start_handler
from .messages import (any_message_handler, strong_message_handler,
                       lower_message_handler, regex_message_handler)


def setup_dispatcher(dp):
    """Добавляет хендлеры вызывающие соответствующие функции в обработку."""
    dp.add_handler(help_handler)
    dp.add_handler(start_handler)
    dp.add_handler(strong_message_handler)
    dp.add_handler(lower_message_handler)
    dp.add_handler(regex_message_handler)
    dp.add_handler(any_message_handler)
