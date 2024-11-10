from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


start_keyboard = ReplyKeyboardBuilder()
start_keyboard.add(
    KeyboardButton(text='Меню'),
    KeyboardButton(text='Способы получения'),
    KeyboardButton(text='Контакты'),
    KeyboardButton(text='О нас')
)
start_keyboard.adjust(2, 2)
