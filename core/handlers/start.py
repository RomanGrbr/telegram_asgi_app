from core.updater import CommandHandler


async def start(update, context):
    name = update.message.mess_from.first_name
    await update.reply_text(text=f'Привет {name}')

start_handler = CommandHandler('/start', start)
