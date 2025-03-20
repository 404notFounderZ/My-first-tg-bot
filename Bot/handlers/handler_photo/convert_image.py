import datetime
import os

from aiogram.types import FSInputFile
from PIL import Image
from aiogram import types, Bot

from Bot.running import SUPPORTED_FORMATS
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)


# Создаем асинхронную функцию
async def convert_image(message: types.Message):
    current_time = datetime.datetime.now().time()
    print(f'    Информация о пользователе: {message.from_user}')
    print(f'Время отправки сообщения пользователем: {current_time}')
    print(f'Пользователь использовал конвертацию в {SUPPORTED_FORMATS}')
    try:
        # получаем желаемый формат из подписи
        desired_format = message.caption.upper()
        if desired_format not in SUPPORTED_FORMATS:
            await message.reply(f'Неподдерживаемый формат. Используйте один из: {', '.join(SUPPORTED_FORMATS)}')
            return

        # Если нет хранилища для временных файлов, то создаем его
        if not os.path.exists('../Bot/temp'):
            os.makedirs('/Bot/temp')

        # Если сообщение фото, то cкачиваем его как фото
        if message.photo:
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path, f'temp/input_image')
        # Если сообщение файл, то скачиваем его как документ
        else:
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path, f'temp/input_image')

        # конвертируем изображение с помощью библиотеки PIL
        with Image.open('temp/input_image') as img:
            output_path = f'temp/converted_file_image.{desired_format.lower()}'
            img.save(output_path, format=desired_format)

        # отправляем конвертированное изображение
        converted_file = FSInputFile(output_path)
        await message.reply_document(converted_file)

        # удаляем временные файлы
        os.remove('temp/input_image')
        os.remove(output_path)

    except Exception as e:
        await message.reply(f'Произошла ошибка при конвертации: {str(e)}')

