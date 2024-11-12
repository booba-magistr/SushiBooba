from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from database.models import Product


inline_keyboard = InlineKeyboardBuilder()
inline_keyboard.add(
    InlineKeyboardButton(text='Удалить', callback_data=f'delete_{Product.id}'),
    InlineKeyboardButton(text='Изменить', callback_data=f'change_{Product.id}')
)
inline_keyboard.adjust(2,)