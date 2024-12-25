from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/start')],
    [KeyboardButton(text='/description'), KeyboardButton(text='/help')],
    [KeyboardButton(text='/read')]
], resize_keyboard=True)
