from .start import start_handler


def setup_dispatcher(dp):
    dp.add_handler(start_handler)
    return dp
