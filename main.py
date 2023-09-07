from aiogram import executor
from database import create_db
from commands import dp
from aiogram import Dispatcher


async def on_startup(dispatcher):
    create_db()

executor.start_polling(dp, on_startup=on_startup, skip_updates=True)