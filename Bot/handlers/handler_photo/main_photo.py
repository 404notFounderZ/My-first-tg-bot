import os

from Bot.handlers.handler_photo.recognize_photo import recognize_file
from Bot.handlers.handler_photo.convert_image import convert_image
from Bot.handlers.handler_photo.decode_qr import decode_qr

from aiogram import types, Router, Bot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
router = Router()


# Общий обработчик функций, чтобы бот был прост в использовании
@router.message(lambda message: message.photo or message.document or message.file)
async def process_photo(message: types.Message):
    caption = message.caption.lower() if message.caption else ''
    if any(text in caption for text in ['png', 'jpeg', 'webp', 'bmp', 'pdf', 'tiff', 'ico',
                                        'ppm', 'eps']):
        await convert_image(message)
    elif 'распознать' in caption:
        await recognize_file(message)
    else:
        await decode_qr(message)
