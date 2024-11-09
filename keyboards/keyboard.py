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

admin_keyboard = ReplyKeyboardBuilder()
admin_keyboard.attach(start_keyboard)
admin_keyboard.add(
    KeyboardButton(text='Админ-панель')
)
admin_keyboard.adjust(2, 2, 1)

