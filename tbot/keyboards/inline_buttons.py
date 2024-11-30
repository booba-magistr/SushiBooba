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
    user_id: int | None = None
    action: str | None = None


def get_category_btns(*, categories: list, sizes: tuple[int] = (2,)):
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

def get_user_cart(
    *,
    page: int | None,
    pagination_btns: dict | None,
    banner_name,
    product_id: int | None,
    sizes: tuple[int] = (3,)
):
    keyboard = InlineKeyboardBuilder()
    if page:
        keyboard.add(InlineKeyboardButton(text='Удалить',
                    callback_data=MenuCallback(banner_name=banner_name, action='delete', product_id=product_id, page=page).pack()))
        keyboard.add(InlineKeyboardButton(text='-1',
                    callback_data=MenuCallback(banner_name=banner_name, action='decrement', product_id=product_id, page=page).pack()))
        keyboard.add(InlineKeyboardButton(text='+1',
                    callback_data=MenuCallback(banner_name=banner_name, action='increment', product_id=product_id, page=page).pack()))

        keyboard.adjust(*sizes)

        row = []
        for text, menu_name in pagination_btns.items():
            if menu_name == "next":
                row.append(InlineKeyboardButton(text=text,
                        callback_data=MenuCallback(banner_name='cart', page=page + 1).pack()))
            elif menu_name == "previous":
                row.append(InlineKeyboardButton(text=text,
                        callback_data=MenuCallback(banner_name='cart', page=page - 1).pack()))

        keyboard.row(*row)

        row2 = [
        InlineKeyboardButton(text='К выбору категории',
                    callback_data=MenuCallback(banner_name='categories').pack()),
        InlineKeyboardButton(text='Заказать',
                    callback_data=MenuCallback(banner_name='order').pack()),
        ]
        return keyboard.row(*row2).as_markup()
    else:
        keyboard.add(
            InlineKeyboardButton(text='К выбору категории',
                    callback_data=MenuCallback(banner_name='categories').pack()))
        
        return keyboard.adjust(*sizes).as_markup()