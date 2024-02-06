from core.updater import CommandHandler


async def start(update, context):
    name = update.message.chat.first_name
    chat_id = update.message.chat.id
    print(f'Привет {name}, чат {chat_id}, команда: /start')
    # await update.reply_text(text=f'Привет {name}')

start_handler = CommandHandler(command='start', callback=start)