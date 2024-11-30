from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InputMediaPhoto
from database.orm_commands import *
from keyboards.inline_buttons import get_category_btns, get_products_btns, get_user_cart
from utils.paginator import Paginator



async def get_categories(session: AsyncSession, banner_name):
    banner = await orm_get_banner(session, banner_name)
    img = InputMediaPhoto(media=banner.img, caption=banner.title)
    cat = await orm_get_categories(session)
    keyboard = get_category_btns(categories=cat)

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

async def get_cart(session, page, user_id, product_id, action, banner_name):
    if action == "delete":
        await orm_delete_from_cart(session, user_id, product_id)
        if page > 1:
            page -= 1
    elif action == "decrement":
        is_cart = await orm_reduce_product_in_cart(session, user_id, product_id)
        if page > 1 and not is_cart:
            page -= 1
    elif action == "increment":
        await orm_add_to_cart(session, user_id, product_id)

    carts = await orm_get_user_carts(session, user_id)

    if not carts:
        banner = await orm_get_banner(session, banner_name)
        img = InputMediaPhoto(
            media=banner.img, caption=f"<strong>{banner.title}</strong>"
        )

        keyboard = get_user_cart(
            page=None,
            banner_name=None,
            pagination_btns=None,
            product_id=None,
        )

    else:
        paginator = Paginator(carts, page=page)

        cart = paginator.get_page()[0]

        cart_price = round(cart.quantity * cart.product.price, 2)
        total_price = round(
            sum(cart.quantity * cart.product.price for cart in carts), 2
        )
        img = InputMediaPhoto(
            media=cart.product.img,
            caption=f"<strong>{cart.product.name}</strong>\n{cart.product.price}$ x {cart.quantity} = {cart_price}$\
                    \nТовар {paginator.page} из {paginator.pages} в корзине.\nОбщая стоимость товаров в корзине {total_price}",
        )

        pagination_btns = pages(paginator)

        keyboard = get_user_cart(
            banner_name=banner_name,
            page=page,
            pagination_btns=pagination_btns,
            product_id=cart.product.id,
        )

    return keyboard, img

async def get_categories_menu(session: AsyncSession, 
banner_name, 
category=None, 
page=None,
product_id=None,
user_id=None,
action=None):
    if banner_name == 'categories':
        return await get_categories(session, banner_name)
    elif banner_name == 'menu':
        return await get_products(session, category, page)
    elif banner_name == 'cart':
        return await get_cart(session, page, user_id, product_id, action, banner_name)
    