import os


from typing import Any
from aiogram.filters import Filter
from aiogram import Bot, types


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]):
        self.chat_types = chat_types

    async def __call__(self, message: types.Message):
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: types.Message):
        return message.from_user.id == int(os.getenv('ADMIN_ID'))
