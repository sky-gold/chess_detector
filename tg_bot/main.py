import os
import telebot
import hashlib

BOT_TOKEN = os.getenv("BOT_TOKEN")
DETECTOR_URL = "http://detector:5000/detect"  # URL вашего другого контейнера

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=['photo'])
def photo(message):
    user_id = message.chat.id
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = f"temp/{hashlib.sha256(downloaded_file).hexdigest()}.jpg"
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    img = open(save_path, 'rb')
    bot.send_photo(user_id, img, caption=save_path)

if __name__ == '__main__':
    bot.polling(none_stop=True)