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
    KeyboardButton(text='В главное меню'),
)
admin.adjust(2, 1)

edit_buttons = ReplyKeyboardBuilder()
edit_buttons.add(
    KeyboardButton(text='Назад'),
    KeyboardButton(text='Отмена'),
    KeyboardButton(text='Оставить без изменений')
)
edit_buttons.adjust(2, 1)
