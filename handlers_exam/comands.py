from core.handler import CommandHandler
from core.button import KeyboardButton, ReplyKeyboardMarkup

async def start(update, context):
    await update.reply_text(text='принял команду /start')


async def items(update, context):
    buttons = [
        [KeyboardButton('кнопка1')]
    ]
    await update.reply_text(
        text='Лови кнопки',
        reply_markup=ReplyKeyboardMarkup(keyboard=buttons))

items_handler = CommandHandler(trigger='/items', callback=items)
start_handler = CommandHandler(trigger='start', callback=start)
