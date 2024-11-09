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

add_admin_button = ReplyKeyboardBuilder()
add_admin_button.attach(start_keyboard)
add_admin_button.add(
    KeyboardButton(text='Админ-панель')
)
add_admin_button.adjust(2, 2, 1)

admin_keyboard = ReplyKeyboardBuilder()
admin_keyboard.add(
    KeyboardButton(text='Просмотреть список товаров'),
    KeyboardButton(text='Изменить товар'),
    KeyboardButton(text='Удалить товар')
)
admin_keyboard.adjust(2, 1)

