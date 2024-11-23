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
    page: int | None = 1
    product_id: int | None = None


def get_category_btns(*, categories: list, banner_name, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category.name, 
                                          callback_data=MenuCallback(banner_name=banner_name, 
                                                                     category=category.id).pack()))

    keyboard.add(InlineKeyboardButton(text='Корзина', 
                                      callback_data=MenuCallback(banner_name='cart').pack()))
    return keyboard.adjust(*sizes).as_markup()
