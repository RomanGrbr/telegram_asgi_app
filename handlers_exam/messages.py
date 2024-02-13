from core.handler import (MessageAnyHandler, MessageStrongHandler,
                          MessageLowerHandler, MessageRegexHandler)


async def strong_message(update, context):
    await update.reply_text(text='совпадение точное')


async def lower_message(update, context):
    await update.reply_text(text=f'совпадение без учета регистра')


async def regex_message(update, context):
    await update.reply_text(text='email зарегистрирован')


async def any_message(update, context):
    await update.reply_text(text='Перехватываю все подряд')

strong_message_handler = MessageStrongHandler(
    trigger='Точное', callback=strong_message)
lower_message_handler = MessageLowerHandler(
    trigger='регистр', callback=lower_message)
regex_message_handler = MessageRegexHandler(
    trigger=r'[^@]+@[^@]+\.[^@]+', callback=regex_message)
any_message_handler = MessageAnyHandler(callback=any_message)
