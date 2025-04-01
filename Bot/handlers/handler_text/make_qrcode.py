import os
import tempfile
import datetime
import qrcode
from aiogram import types
from aiogram.types import FSInputFile
import logging

logging.basicConfig(
    filename='action.log', level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S', filemode='a', force=True
)
# асинхронная функция создание QR - кода
async def make_qr(message: types.Message):
    global img
    logging.info(f'{message.from_user.username, message.from_user.id} --- Make QR-code')
    try:
        # формат QR - кода и его версия
        if message.text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10, border=3
            )
            qr.add_data(message.text)
            qr.make(fit=True)
            img = qr.make_image(front_color='black', back_color='white')

        # создание QR-кода
        with tempfile.NamedTemporaryFile(delete=False, suffix='png') as temp_file:
            img.save(temp_file, 'png')
            temp_file_path = temp_file.name

        await message.reply_photo(photo=FSInputFile(temp_file_path))
        # удаляем временные файлы
        os.unlink(temp_file_path)

    except Exception as e:
        await message.reply(f'Произошла ошибка при создании QR: {str(e)}')
