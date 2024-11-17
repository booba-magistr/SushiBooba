import os


from aiogram.filters import CommandStart, Command, or_f
from aiogram import types, Router, F
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from database.orm_commands import orm_get_products
from sqlalchemy.ext.asyncio import AsyncSession


user_private_router = Router()
from keyboards import user_keyboard, admin_keyboard

@user_private_router.message(CommandStart())
@user_private_router.message(or_f(Command('about'), (F.text == 'О нас')))
async def get_cmd(message: types.Message):
    text = as_list(
        as_marked_section(
        Bold('Добро пожаловать в SushiBooba!!!'),
        'Заказывайте суши онлайн и наслаждайтесь ими дома',
        'Быстрая доставка',
        'Только свежие и качественные продукты',
        'Разнообразие меню - большой выбор роллов, суши',
        marker='💥'
    ),
        as_marked_section(
            Bold('Время работы'),
            'Пн-Пт: 10:00-21:00',
            'Сб-Вс: 10:00-20:00',
            marker='⌚'
        ),
        sep='\n------------------------------\n'
    )
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(text.as_html(), 
                         reply_markup=admin_keyboard.add_admin_button.as_markup(resize_keyboard=True))
    else:
        await message.answer(text.as_html(), 
                         reply_markup=user_keyboard.start_keyboard.as_markup(resize_keyboard=True))

@user_private_router.message(or_f(Command('menu'), (F.text == 'Меню')))
async def get_message(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.img,
            caption=f"<strong>{product.name}\
                </strong>\nО товаре:{product.description}\nЦена:{round(product.price, 2)}"
        )

@user_private_router.message(or_f(Command('delivery'), (F.text == 'Способы получения')))
async def get_delivery(message: types.Message):
    text = as_marked_section(
        Bold('Способ получения'),
        'Самовывоз',
        'Доставка курьером',
        marker='✅'
    )
    await message.answer(text.as_html())

@user_private_router.message(or_f(Command('contact'), (F.text == 'Контакты')))
async def get_contact(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold('Мы находимся'),
            'Волгоград, пр. имени В.И. Ленина, 28',
            'Волгоград, Рабоче-Крестьянская ул., 9 Б',
            marker='🟢'
        ),
        as_marked_section(
            Bold('Контакты'),
            '8(995)423-27-47',
            '8(909)048-07-32',
            marker='📱'
        ),
        sep='\n------------------------------\n'
    )
    await message.answer(text.as_html())

@user_private_router.message(F.text.lower() == 'id')
async def get_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')