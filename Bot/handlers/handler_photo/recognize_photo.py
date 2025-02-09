import pytesseract
import asyncio

import os

from aiogram.types import FSInputFile
from PIL import Image

from aiogram import types, Bot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
# подключаем скаченную папку Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


async def recognize_file(message: types.Message):
    print(f'Расшифровка текста с фото \n{message.from_user}')
    try:
        if not os.path.exists('../Bot/temp'):
            os.makedirs('/Bot/temp')

        # cкачиваем файл
        if message.photo:
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path,
                                    f'temp/recognize')

        else:
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path,
                                    f'temp/recognize')

        with open('temp/recognize', 'rb') as input_file:
            recognize = Image.open(input_file)
            img = recognize.convert('L')

            check_photo = 'temp/check_image.jpg'
            img.save(check_photo)

            # потом убрать
            await message.reply_photo(photo=FSInputFile(check_photo),
                                      caption='Фото после обработки')

            custom_config = r'--oem 3 --psm 6'
            recognize_text = pytesseract.image_to_string(img, config=custom_config, lang='rus+eng')

        await bot.send_chat_action(chat_id=message.from_user.id, action='typing')
        await asyncio.sleep(3)
        await message.reply(f'Распознанный текст:\n\n{recognize_text}')

        # удаляем временные файлы
        os.remove('temp/recognize')
        os.remove(check_photo)

    except Exception as e:
        await message.reply(f'Произошла ошибка: {str(e)}')
