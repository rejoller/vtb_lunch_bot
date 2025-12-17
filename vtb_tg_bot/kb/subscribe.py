from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



text = 'Подписаться'

markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=text, callback_data='subscribe')
    ]
])