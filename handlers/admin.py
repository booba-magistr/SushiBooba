import os


from aiogram import types, Router, F
from keyboards import keyboard


from filters.chat_types import ChatTypeFilter, IsAdmin

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


@admin_router.message(F.text == 'Админ-панель')
async def cmd_admin(message: types.Message):
    await message.answer('Что хотите сделать?', 
                         reply_markup=keyboard.admin_keyboard.as_markup(resize_keyboard=True))