import asyncio
import os


from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.user_private import user_private_router
from handlers.admin import admin_router
from database.engine import create_db, sessionmaker, drop_db
from middlewares.db import DataBaseMiddleware

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
dp.include_router(user_private_router)
dp.include_router(admin_router)


async def main():
    # await drop_db()
    await create_db()
    dp.update.middleware(DataBaseMiddleware(session_pool=sessionmaker))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())
