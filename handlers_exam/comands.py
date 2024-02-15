from core.handler import CommandHandler
from core.button import (KeyboardButton, ReplyKeyboardMarkup,
                         InlineKeyboardButton, InlineKeyboardMarkup)


async def start(update, context):
    await update.reply_text(text='принял команду /start')


async def buttons(update, context):
    keyboard = [
        [KeyboardButton('кнопка1'), KeyboardButton('кнопка2')],
        [KeyboardButton('кнопка3'), KeyboardButton('кнопка4')]
    ]
    await update.reply_text(
        text='Лови кнопки',
        reply_markup=ReplyKeyboardMarkup(keyboard=keyboard,
                                         one_time_keyboard=True)
    )


async def inline(update, context):
    keyboard = [
        [
            InlineKeyboardButton(text='Вариант 1', callback_data='hello'),
            InlineKeyboardButton(text='Вариант 2', callback_data='go home')
        ]
    ]
    await update.reply_text(
        text='Что делать?',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))

buttons_handler = CommandHandler(trigger='/buttons', callback=buttons)
start_handler = CommandHandler(trigger='start', callback=start)
inline_handler = CommandHandler(trigger='inline', callback=inline)
