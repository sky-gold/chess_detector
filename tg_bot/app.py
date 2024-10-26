import os
import hashlib
import requests
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.executor import start_polling
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
DETECTOR_URL = "http://detector:5000/detect"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=['photo'])
async def photo(message: types.Message):
    print("GOT PHOTO")

    user_id = message.chat.id
    await bot.send_message(chat_id=user_id, text="Detecting...")

    fileID = message.photo[-1].file_id
    file_info = await bot.get_file(fileID)
    save_path = f"/app/temp/{13123}.jpg"
    
    # Ensure the temp directory exists
    if not os.path.exists("/app/temp"):
        os.makedirs("/app/temp")
    
    await bot.download_file(file_info.file_path, save_path)
    print(f"Image saved to {save_path}")
    
    # Send request to detector
    with open(save_path, 'rb') as img:
        response = requests.post(DETECTOR_URL, files={'image': img}, data={'user_id': user_id})
        print(f"Response from detector: {response.status_code}")
    
    # Delete temporary photo
    os.remove(save_path)
    print(f"Temporary photo deleted: {save_path}")

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

async def on_startup(dispatcher):
    await start_web_server()

if __name__ == "__main__":
    start_polling(dp, skip_updates=True, on_startup=on_startup)