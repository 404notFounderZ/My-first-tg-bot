import datetime
import os

import zxing
from aiogram import types, Bot
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)


# считывание QR-кода с помощью Zxing
async def decode_zxing(image_p):
    reader = zxing.BarCodeReader(java='C:\\Program Files\\Java\\jdk-23\\bin\\java.exe')
    barc = reader.decode(image_p)
    if barc and barc.parsed:
        return barc.parsed
    return None

# функция для расшифровки qr кода
async def decode_qr(message: types.Message):
    current_time = datetime.datetime.now().time()
    print(f'    Информация о пользователе: {message.from_user}')
    print(f'Время отправки сообщения пользователем: {current_time}')
    print('Пользователь использовал расшифровку QR-code')
    try:
        # скачиваем фото
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        temp_path = "temp/qr_image.png"
        await bot.download_file(file.file_path, temp_path)
        # раскодированная информация
        qr_data = await decode_zxing(temp_path)

        # удаляем временный файл
        os.remove(temp_path)

        # отправляем результат
        if qr_data:
            await message.reply(f'🔒QR-код успешно расшифрован\n\n'
                                f'ℹ️Информация с QR-кода: <tg-spoiler>{qr_data}</tg-spoiler>',
                                parse_mode=ParseMode.HTML)
        else:
            await message.reply('Не удалось распознать QR-код')

    except Exception as e:
        await message.reply(f'Ошибка при расшифровке QR-кода: {e}')
