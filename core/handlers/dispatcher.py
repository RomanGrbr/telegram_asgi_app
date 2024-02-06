from .start import start_handler
from .help import help_handler


def setup_dispatcher(dp):
    # dp.add_handler(start_handler)
    # dp.add_handler(help_handler)
    dp.add_handler_v2(start_handler)
    return dp
