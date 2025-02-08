import re
from aiogram import types, Router

from Bot.handlers.handler_text.currency import convert_cur
from Bot.handlers.handler_text.make_qrcode import make_qr
from Bot.handlers.handler_text.date_weeks import cmd_time

router = Router()

date_reg = re.compile(r'\d\d\.\d\d\.\d{4}')


@router.message(lambda message: message.text)
async def process_text(message: types.Message):
    if message.text.startswith('!'):
        await convert_cur(message)
    elif date_reg.match(message.text):
        await cmd_time(message)
    else:
        await make_qr(message)
