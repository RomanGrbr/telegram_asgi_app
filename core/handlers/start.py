from core.updater import CommandHandler


async def start(update, context):
    print(update.message.text)

start_handler = CommandHandler('/start', start)
