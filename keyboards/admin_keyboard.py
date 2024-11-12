from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton
from .user_keyboard import start_keyboard


add_admin_button = ReplyKeyboardBuilder()
add_admin_button.attach(start_keyboard)
add_admin_button.add(
    KeyboardButton(text='Админ-панель')
)
add_admin_button.adjust(2, 2, 1)

admin = ReplyKeyboardBuilder()
admin.add(
    KeyboardButton(text='Добавить товар'),
    KeyboardButton(text='Просмотреть список товаров'),
)
admin.adjust(2, 2)

delete_back = ReplyKeyboardBuilder()
delete_back.add(
    KeyboardButton(text='Назад'),
    KeyboardButton(text='Отмена')
)
delete_back.adjust(2)