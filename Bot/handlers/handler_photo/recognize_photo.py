import pytesseract
import asyncio
import os

from PIL import Image

from aiogram import types, Bot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
# подключаем скаченную папку Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import logging
logging.basicConfig(
    filename='action.log', level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S', filemode='a', force=True
)

async def recognize_file(message: types.Message):
    logging.info(f'{message.from_user.username, message.from_user.id} --- Recognize photo')
    try:
        if not os.path.exists('../Bot/temp'):
            os.makedirs('/Bot/temp')

        # cкачиваем файл
        if message.photo:
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path,
                                    f'temp/{file_id}recognize')

        else:
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path,
                                    f'temp/{file_id}recognize')
        # открываем файл, делаем его черно-белым и распознаем текст
        with open(f'temp/{file_id}recognize', 'rb') as input_file:
            recognize = Image.open(input_file)
            img = recognize.convert('L')

            custom_config = r'--oem 3 --psm 6'
            recognize_text = pytesseract.image_to_string(img, config=custom_config, lang='rus+eng')
        # визуальное действие печати
        await bot.send_chat_action(chat_id=message.from_user.id, action='typing')
        await asyncio.sleep(3)
        # отправление результата пользователю
        await message.reply(f'Распознанный текст:\n\n{recognize_text}')

        # удаляем временные файлы
        os.remove(f'temp/{file_id}recognize')

    except Exception as e:
        await message.reply(f'Произошла ошибка: {str(e)}')
