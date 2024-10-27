import os
import requests
from aiogram import Dispatcher, types
from utils import generate_random_string

DETECTOR_URL = "http://detector:5000/detect"

async def photo(message: types.Message):
    print("GOT PHOTO")

    user_id = message.chat.id
    await message.answer("Detecting...")

    fileID = message.photo[-1].file_id
    file_info = await message.bot.get_file(fileID)
    save_path = f"/app/temp/{generate_random_string(10)}_{user_id}.jpg"
    
    # Ensure the temp directory exists
    if not os.path.exists("/app/temp"):
        os.makedirs("/app/temp")
    
    await message.bot.download_file(file_info.file_path, save_path)
    print(f"Image saved to {save_path}")
    
    # Send request to detector
    with open(save_path, 'rb') as img:
        response = requests.post(DETECTOR_URL, files={'image': img}, data={'user_id': user_id})
        print(f"Response from detector: {response.status_code}")
    
    # Delete temporary photo
    os.remove(save_path)
    print(f"Temporary photo deleted: {save_path}")

def setup_handlers(dp: Dispatcher):
    dp.register_message_handler(photo, content_types=['photo'])