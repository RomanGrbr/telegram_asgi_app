from core.handler import (MessageAnyHandler, MessageStrongHandler,
                          MessageLowerHandler, MessageRegexHandler)


async def strong_message(update, context):
    name = update.message.chat.first_name
    chat_id = update.message.chat.id
    print(f'Привет {name}, чат {chat_id}, совпадение точное')
    # await update.reply_text(text=f'Привет {name}')


async def lower_message(update, context):
    name = update.message.chat.first_name
    chat_id = update.message.chat.id
    print(f'Привет {name}, чат {chat_id}, совпадение без учета регистра')
    # await update.reply_text(text=f'Привет {name}')


async def regex_message(update, context):
    name = update.message.chat.first_name
    chat_id = update.message.chat.id
    print(f'Привет {name}, чат {chat_id}, email зарегистрирован')
    # await update.reply_text(text=f'Привет {name}')


async def any_message(update, context):
    name = update.message.chat.first_name
    chat_id = update.message.chat.id
    print(f'Привет {name}, чат {chat_id}, Перехватываю все подряд')
    # await update.reply_text(text=f'Привет {name}')

strong_message_handler = MessageStrongHandler(
    trigger='Точное', callback=strong_message)
lower_message_handler = MessageLowerHandler(
    trigger='регистр', callback=lower_message)
regex_message_handler = MessageRegexHandler(
    trigger=r'[^@]+@[^@]+\.[^@]+', callback=regex_message)
any_message_handler = MessageAnyHandler(callback=any_message)
