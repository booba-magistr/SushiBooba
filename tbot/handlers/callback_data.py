from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InputMediaPhoto
from database.orm_commands import orm_get_banner, orm_get_categories, orm_get_products
from keyboards.inline_buttons import get_category_btns, get_products_btns
from database.orm_commands import Paginator



async def get_categories(session: AsyncSession, banner_name):
    banner = await orm_get_banner(session, banner_name)
    img = InputMediaPhoto(media=banner.img, caption=banner.title)
    cat = await orm_get_categories(session)
    keyboard = get_category_btns(categories=cat, banner_name=banner_name)

    return keyboard, img

def pages(paginator: Paginator):
    btns = dict()
    if paginator.has_previous():
        btns["Пред. страница"] = "previous"

    if paginator.has_next():
        btns["След. страница"] = "next"

    return btns

async def get_products(session, category, page):
    products = await orm_get_products(session, category_id=category)

    paginator = Paginator(products, page=page)
    product = paginator.get_page()[0]

    img = InputMediaPhoto(
        media=product.img,
        caption=f"<strong>{product.name}\
                </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}₽\n\
                <strong>Товар {paginator.page} из {paginator.pages}</strong>",
    )

    pagination_btns = pages(paginator)

    keyboard = get_products_btns(
        category=category,
        page=page,
        pagination_btns=pagination_btns,
        product_id=product.id,
    )

    return keyboard, img

async def get_categories_menu(session: AsyncSession, 
banner_name, 
category:int | None=None, 
page=None):
    if banner_name == 'categories':
        return await get_categories(session, banner_name)
    if banner_name == 'menu':
        return await get_products(session, category, page)