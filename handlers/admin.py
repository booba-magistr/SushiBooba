import os


from aiogram import types, Router, F
from keyboards import admin_keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


from filters.chat_types import ChatTypeFilter, IsAdmin

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


@admin_router.message(F.text == 'Админ-панель')
async def cmd_admin(message: types.Message):
    await message.answer('Что хотите сделать?', 
                         reply_markup=admin_keyboard.admin.as_markup(resize_keyboard=True))
    
@admin_router.message(F.text == 'Просмотреть список товаров')
async def lst_products(message: types.Message):
    await message.answer('Список товаров')

@admin_router.message(F.text == 'Изменить товар')
async def change_product(message: types.Message):
    await message.answer('Какой товар изменить')

@admin_router.message(F.text == 'Удалить товар')
async def delete_product(message: types.Message):
    await message.answer('Удалить товар')


# Code for Finite State Machine

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    img = State()
