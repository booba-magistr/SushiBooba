from aiogram import types, Router, F
from keyboards import admin_keyboard, inline_buttons
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from filters.chat_types import ChatTypeFilter, IsAdmin
from database.orm_commands import orm_add_product, orm_get_products
from sqlalchemy.ext.asyncio import AsyncSession


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())
get_keyboard = admin_keyboard.add_admin_button.as_markup(resize_keyboard=True)
edit_action = admin_keyboard.delete_back.as_markup(resize_keyboard=True)
ib = inline_buttons.inline_keyboard.as_markup()


@admin_router.message(F.text == 'Админ-панель')
async def cmd_admin(message: types.Message):
    await message.answer('Что хотите сделать?', 
                         reply_markup=admin_keyboard.admin.as_markup(resize_keyboard=True))
    
@admin_router.message(F.text == 'Просмотреть список товаров')
async def lst_products(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.img,
            caption=f"<strong>{product.name}\
                </strong>\nО товаре:{product.description}\nЦена:{product.price}",
                reply_markup=ib
        )

@admin_router.message(F.text == 'В главное меню')
async def back_to_menu(message: types.Message):
    await message.answer('Вы вернулись в главное меню', reply_markup=get_keyboard)

# Code for Finite State Machine

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    img = State()

@admin_router.message(StateFilter(None), F.text == 'Добавить товар')
async def add_product(message: types.Message, state: FSMContext):
    await message.answer('Введите название товара', reply_markup=edit_action)
    await state.set_state(AddProduct.name)

@admin_router.message(StateFilter('*'), F.text.lower()=='отмена')
async def cancel_handler(message: types.Message, state:FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        return
    
    await state.clear()
    await message.answer('Все действия отменены', reply_markup=get_keyboard)

@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer('Невозможно выполнить действие')
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer("Вы вернулись на шаг назад. Выполните предыдущее действие!")
            return
        previous = step

@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if message.text == 'test':
        await message.answer('Некорректное имя!\nВведите ещё раз', reply_markup=edit_action)
        return
    
    await state.update_data(name=message.text)
    await message.answer('Укажите описание товара', reply_markup=edit_action)
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Укажите стоимость товара', reply_markup=edit_action)
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer('Установите фотографию', reply_markup=edit_action)
    await state.set_state(AddProduct.img)

@admin_router.message(AddProduct.img, F.photo)
async def add_photo(message: types.Message, state: FSMContext, session):
    await state.update_data(img=message.photo[-1].file_id)
    await message.answer('Товар добавлен', reply_markup=get_keyboard)
    data = await state.get_data()

    await orm_add_product(session, data)

    await state.clear()
