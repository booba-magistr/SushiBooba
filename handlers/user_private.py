from aiogram.filters import CommandStart, Command, or_f
from aiogram import types, Router, F


user_private_router = Router()
from keyboards import keyboard

@user_private_router.message(CommandStart())
async def get_cmd(message: types.Message):
    await message.answer('Бот начал работать', 
                         reply_markup=keyboard.start_keyboard.as_markup(resize_keyboard=True))

@user_private_router.message(or_f(Command('menu'), (F.text == 'Меню')))
async def get_message(message: types.Message):
    await message.answer('Ваше меню')

@user_private_router.message(or_f(Command('delivery'), (F.text == 'Способы получения')))
async def get_delivery(message: types.Message):
    await message.answer('Варианты доставки')

@user_private_router.message(or_f(Command('contact'), (F.text == 'Контакты')))
async def get_contact(message: types.Message):
    await message.answer('Контакты')

@user_private_router.message(or_f(Command('about'), (F.text == 'О нас')))
async def get_about(message: types.Message):
    await message.answer('О нас') 
