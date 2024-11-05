from aiogram.filters import CommandStart, Command
from aiogram import types, Router


user_private_router = Router()


@user_private_router.message(CommandStart())
async def get_cmd(message: types.Message):
    await message.answer('Бот начал работать')

@user_private_router.message(Command('menu'))
async def get_message(message: types.Message):
    await message.answer('Ваше меню')


@user_private_router.message(Command('delivery'))
async def get_delivery(message: types.Message):
    await message.answer('Варианты доставки')