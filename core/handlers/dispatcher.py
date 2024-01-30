from .start import start_handler


async def setup_dispatcher(dp):
    await dp.add_handler(start_handler)
    return dp
