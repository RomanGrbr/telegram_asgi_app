from core.handler import CommandHandler


async def start(update, context):
    name = update.message.chat.first_name
    chat_id = update.message.chat.id
    print(f'Привет {name}, чат {chat_id}, команда: /start')
    # await update.reply_text(text=f'Привет {name}')


async def help(update, context):
    name = update.message.chat.first_name
    chat_id = update.message.chat.id
    print(f'Привет {name}, чат {chat_id}, команда: help')
    # await update.reply_text(text=f'Привет {name}')

help_handler = CommandHandler(trigger='/help', callback=help)
start_handler = CommandHandler(trigger='start', callback=start)
