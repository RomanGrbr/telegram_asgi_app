from .comands import start_handler, help_handler
from .messages import strong_message_handler, any_message_handler


def setup_dispatcher(dp):
    dp.add_handler(help_handler)
    dp.add_handler(start_handler)
    dp.add_handler(strong_message_handler)
    dp.add_handler(any_message_handler)
    return dp
