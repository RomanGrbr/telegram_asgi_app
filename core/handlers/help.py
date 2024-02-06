from core.updater import MessageStrongHandler


async def help(update, context):
    name = update.message.chat.first_name
    chat_id = update.message.chat.id
    print(f'Привет {name}, чат {chat_id}, команда: help')
    # await update.reply_text(text=f'Привет {name}')

help_handler = MessageStrongHandler(command='help', callback=help)
