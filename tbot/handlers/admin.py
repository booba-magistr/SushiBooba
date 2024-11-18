from aiogram import types, Router, F
from keyboards import admin_keyboard
from keyboards.inline_buttons import get_inline_btn
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from filters.chat_types import ChatTypeFilter, IsAdmin
from database.orm_commands import *
from sqlalchemy.ext.asyncio import AsyncSession


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

#### Admin's keyboards ####
get_keyboard = admin_keyboard.add_admin_button.as_markup(resize_keyboard=True)
edit_action = admin_keyboard.edit_buttons.as_markup(resize_keyboard=True)


@admin_router.message(F.text == 'Админ-панель')
async def cmd_admin(message: types.Message):
    await message.answer('Что хотите сделать?', 
                         reply_markup=admin_keyboard.admin.as_markup(resize_keyboard=True))
    
@admin_router.message(F.text == 'Просмотреть список товаров')
async def get_categories(message: types.Message, session: AsyncSession):
    btns = {category.name: f'category_{category.id}' for category in await orm_get_categories(session)}
    await message.answer('Выберите категорию', 
                         reply_markup=get_inline_btn(btn=btns, sizes=(2, 2)))
    
@admin_router.callback_query(F.data.startswith('category'))
async def lst_products(callback: types.CallbackQuery, session: AsyncSession):
    category_id = callback.data.split('_')[-1]
    if not await orm_get_products(session, category_id):
        await callback.answer()
        await callback.message.answer('Товары по данной категории отсутствуют')
    else:
        await callback.answer()
        for product in await orm_get_products(session, int(category_id)):
            await callback.message.answer_photo(
                product.img,
                caption=f"<strong>{product.name}\
                    </strong>\nО товаре:{product.description}\nЦена:{product.price}",
                    reply_markup=get_inline_btn(btn={
                        'Удалить': f'delete_{product.id}',
                        'Изменить': f'change_{product.id}'
                    })
            )

@admin_router.message(F.text == 'В главное меню')
async def back_to_menu(message: types.Message):
    await message.answer('Вы вернулись в главное меню', reply_markup=get_keyboard)

@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split('_')[-1]
    await orm_delete_product(session, int(product_id))

    await callback.answer()
    await callback.message.answer('Товар удалён')

#### Code for Finite State Machine to add product in menu ####

class AddProduct(StatesGroup):
    name = State()
    category = State()
    description = State()
    price = State()
    img = State()

    current_update_product = None

@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def update_item(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    product_id = callback.data.split('_')[-1]
    current_update_product = await orm_get_product(session, int(product_id))

    AddProduct.current_update_product = current_update_product
    await callback.answer()
    await callback.message.answer('Введите название товара', reply_markup=edit_action)
    await state.set_state(AddProduct.name)

@admin_router.message(StateFilter(None), F.text == 'Добавить товар')
async def add_product(message: types.Message, state: FSMContext):
    await message.answer('Введите название товара', reply_markup=edit_action)
    await state.set_state(AddProduct.name)

@admin_router.message(StateFilter('*'), F.text.lower()=='отмена')
async def cancel_handler(message: types.Message, state:FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        return
    if AddProduct.current_update_product:
        AddProduct.current_update_product = None
    
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

@admin_router.message(AddProduct.name, or_f(F.text, F.text == 'Оставить без изменений'))
async def add_name(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == 'Оставить без изменений':
        await state.update_data(name = AddProduct.current_update_product.name)
    else:
        await state.update_data(name=message.text)
    btns = {category.name: str(category.id) for category in await orm_get_categories(session)}
    await message.answer('К какой категории будет относится товар', 
                         reply_markup=get_inline_btn(btn=btns, sizes=(2, 2)))
    await state.set_state(AddProduct.category)

@admin_router.callback_query(AddProduct.category, F.data.isdigit())
async def add_category(callback: types.CallbackQuery, state: FSMContext):
    if callback.message.text == 'Оставить без изменений':
        await state.update_data(category = AddProduct.current_update_product.category)
    else:
        await state.update_data(category=int(callback.data))
        await callback.answer()
    await callback.message.answer('Укажите описание товара')
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.description, or_f(F.text, F.text == 'Оставить без изменений'))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == 'Оставить без изменений':
        await state.update_data(description = AddProduct.current_update_product.description)
    else:
        await state.update_data(description=message.text)
    await message.answer('Укажите стоимость товара', reply_markup=edit_action)
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.price, or_f(F.text, F.text == 'Оставить без изменений'))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == 'Оставить без изменений':
        await state.update_data(price = AddProduct.current_update_product.price)
    else:
        await state.update_data(price=float(message.text))
    await message.answer('Установите фотографию', reply_markup=edit_action)
    await state.set_state(AddProduct.img)

@admin_router.message(AddProduct.img, or_f(F.photo, F.text == 'Оставить без изменений'))
async def add_photo(message: types.Message, state: FSMContext, session):
    if message.text == 'Оставить без изменений':
        await state.update_data(img = AddProduct.current_update_product.img)
    else:
        await state.update_data(img=message.photo[-1].file_id)

    data = await state.get_data()

    if AddProduct.current_update_product:
        await orm_update_product(session, AddProduct.current_update_product.id, data)
        await message.answer("Товар успешно изменён", reply_markup=get_keyboard)
    else:
        await orm_add_product(session, data)
        await message.answer('Товар добавлен', reply_markup=get_keyboard)

    await state.clear()
    AddProduct.current_update_product = None