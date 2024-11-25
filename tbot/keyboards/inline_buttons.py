from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


def get_inline_btn(
    *,
    btn: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, value in btn.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()


class MenuCallback(CallbackData, prefix='menu'):
    banner_name: str
    category: int | None = None
    page: int = 1
    product_id: int | None = None


def get_category_btns(*, categories: list, banner_name, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category.name, 
                                          callback_data=MenuCallback(banner_name='menu', 
                                                                     category=category.id).pack()))

    keyboard.add(InlineKeyboardButton(text='Корзина', 
                                      callback_data=MenuCallback(banner_name='cart').pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_products_btns(
    *,
    category: int,
    page: int,
    pagination_btns: dict,
    product_id: int,
    sizes: tuple[int] = (2, 1)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад',
                callback_data=MenuCallback(banner_name='categories').pack()))
    keyboard.add(InlineKeyboardButton(text='Добавить в корзину',
                callback_data=MenuCallback(banner_name='add_to_cart', product_id=product_id).pack()))
    keyboard.add(InlineKeyboardButton(text='Просмотреть корзину',
                callback_data=MenuCallback(banner_name='cart').pack()))

    keyboard.adjust(*sizes)

    row = []
    for text, menu_name in pagination_btns.items():
        if menu_name == "next":
            row.append(InlineKeyboardButton(text=text,
                    callback_data=MenuCallback(
                        banner_name='menu',
                        category=category,
                        page=page + 1).pack()))
        
        elif menu_name == "previous":
            row.append(InlineKeyboardButton(text=text,
                    callback_data=MenuCallback(
                        banner_name='menu',
                        category=category,
                        page=page - 1).pack()))

    return keyboard.row(*row).as_markup()