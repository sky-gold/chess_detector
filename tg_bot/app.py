import os
from aiogram import Bot, Dispatcher, executor
from handlers import setup_handlers
from web_server import start_web_server

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def on_startup(dispatcher):
    await start_web_server()
    setup_handlers(dispatcher)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)