import datetime
import os
import cv2

from aiogram import types, Bot
from aiogram.enums import ParseMode
from Bot.running import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)


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

        # считывание QR-кода
        img = cv2.imread(temp_path)
        detector = cv2.QRCodeDetector()
        qr_data, _, _ = detector.detectAndDecode(img)

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
