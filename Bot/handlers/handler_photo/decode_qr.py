import os

import cv2
import zxing
from aiogram import types, Bot
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)

import logging
logging.basicConfig(
    filename='action.log', level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S', filemode='a', force=True
)
# считывание QR-кода с помощью Zxing
async def decode_zxing(image_p):
    reader = zxing.BarCodeReader(java='C:\\Program Files\\Java\\jdk-23\\bin\\java.exe')
    try:
        barc = reader.decode(image_p)
        if barc and barc.parsed:
            return barc.parsed.encode('utf-8').decode('utf-8')
    except Exception as e:
        pass

async def decode_cv2(image_p):
    rus_qr = cv2.imread(image_p)
    decode_rus = cv2.QRCodeDetector()
    qr_data, _, _ = decode_rus.detectAndDecode(rus_qr)
    return qr_data

# функция для расшифровки qr кода
async def decode_qr(message: types.Message):
    logging.info(f'{message.from_user.username, message.from_user.id} --- Decode QR-code')

    try:
        # скачиваем фото
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        temp_path = "temp/qr_image.png"
        await bot.download_file(file.file_path, temp_path)
        # раскодированная информация
        qr_data = await decode_zxing(temp_path)

        if not qr_data:
            print('cv2')
            qr_data = await decode_cv2(temp_path)

        # отправляем результат
        if qr_data:
            await message.reply(f'🔒QR-код успешно расшифрован\n\n'
                                f'ℹ️Информация с QR-кода: <tg-spoiler>{qr_data}</tg-spoiler>',
                                parse_mode=ParseMode.HTML)
        else:
            await message.reply('Не удалось распознать QR-код')

        # удаляем временный файл
        os.remove(temp_path)
    except Exception as e:
        await message.reply(f'Ошибка при расшифровке QR-кода: {e}')
