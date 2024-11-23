from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InputMediaPhoto
from database.orm_commands import orm_get_banner, orm_get_categories
from keyboards.inline_buttons import get_category_btns



async def get_categories(session: AsyncSession, banner_name):
    banner = await orm_get_banner(session, banner_name)
    img = InputMediaPhoto(media=banner.img, caption=banner.title)
    cat = await orm_get_categories(session)
    keyboard = get_category_btns(categories=cat, banner_name=banner_name)

    return keyboard, img


async def get_categories_menu(session: AsyncSession, banner_name, category=None):
    if banner_name == 'categories':
        return await get_categories(session, banner_name)