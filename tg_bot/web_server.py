from aiohttp import web
from aiogram import Bot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

async def send_result(request):
    print("Received request to /send_result")
    data = await request.post()
    print(f"Request data: {data}")

    user_id = data.get('user_id', False)
    image_1 = data.get('image_1', False)
    image_2 = data.get('image_2', False)

    if not user_id or not image_1 or not image_2:
        print("Missing required fields in request")
        return web.json_response({"error": "Missing required fields"}, status=400)

    print(f"Sending images to user {user_id}")

    # Send images to user via Telegram
    await bot.send_photo(chat_id=user_id, photo=image_1.file)
    await bot.send_photo(chat_id=user_id, photo=image_2.file)
    print(f"Images sent to user {user_id}")

    return web.json_response({"status": "Images sent to user"})

async def start_web_server():
    app = web.Application()
    app.router.add_post('/send_result', send_result)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5001)
    await site.start()