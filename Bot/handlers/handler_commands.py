import json
import sqlite3
import os

import aiohttp
from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from Bot.keyboard.inline_keyboard import get_keyboard, rates_keyboard
from Bot.running import HELP_COM
from dotenv import load_dotenv
import logging

logging.basicConfig(
    filename='action.log', level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S', filemode='a'
)

load_dotenv()
URL_EXCHANGE_RATES = os.getenv('URL_EXCHANGE_RATES')
router = Router()

def save_user_to_txt(user: types.User):
    filename = "data_base.txt"

    file_exists = os.path.exists(filename)

    user_data = (
        f"ID: {user.id}\n"
        f"Имя: {user.first_name}\n"
        f"Юзернейм: @{user.username or 'Не указан'}\n"
        f"------------------------\n"
    )

    if not is_user_in_file(user.id, filename):
        with open(filename, "a", encoding="utf-8") as f:
            if not file_exists:
                f.write("======\n\n")
            f.write(user_data)

def is_user_in_file(user_id: int, filename: str) -> bool:
    if not os.path.exists(filename):
        return False

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        return f"ID: {user_id}\n" in content

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    user = message.from_user
    save_user_to_txt(user)

    logging.info(f'{message.from_user.username, message.from_user.id} --- /start')
    await message.answer(
        f'👋Привет {message.from_user.first_name}!\nЯ многофункциональный бот. Все мои возможности отмечены ниже.',
        reply_markup=get_keyboard())


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    logging.info(f'{message.from_user.username, message.from_user.id} --- /help')
    await message.answer(f'Мои команды:\n{HELP_COM}\n\n'
                         f'Полный код бота вы можете посмотреть здесь:'
                         f' https://github.com/404notFounderZ/My-first-tg-bot')


@router.message(Command('get_info'))
async def cmd_info(message: Message):
    logging.info(f'{message.from_user.username, message.from_user.id} --- /get_info')
    await message.answer(f'Твой ID: <code>{message.from_user.id}</code>\n'
                         f'Твой username: @{message.from_user.username}', parse_mode=ParseMode.HTML)

@router.message(Command('support'))
async def cmd_support(message: Message):
    logging.info(f'{message.from_user.username, message.from_user.id} --- /support')
    await message.answer(
        f'🙁Техподдержка:\n\nЕсли при использовании бота возникла ошибка, пишите в личные сообщения '
        f'<a href="t.me/denis9F">Денису</a>', parse_mode=ParseMode.HTML)

@router.message(Command('rates'))
async def cmd_rates(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_EXCHANGE_RATES) as response:
            data = await response.json()
            logging.info(f'{message.from_user.username, message.from_user.id} --- /rates')
            if data['result'] == 'success':
                usd_to_rub = data['conversion_rates']['RUB']
                eur_to_usd = data['conversion_rates']['EUR']
                kzt_to_usd = data['conversion_rates']['KZT']
                try_to_usd = data['conversion_rates']['TRY']

                eur_to_rub = (1 / eur_to_usd) * usd_to_rub
                kzt_to_rub = (1 / kzt_to_usd) * usd_to_rub
                try_to_rub = (1 / try_to_usd) * usd_to_rub

            else:
                await message.answer('❌Не удалось получить актуальный курс валют')

    await message.answer(f'💰Курс валют в рублях: \n\n'
                         f'1$ (доллар) = {usd_to_rub:.2f}₽\n'
                         f'1€ (евро) = {eur_to_rub:.2f}₽\n'
                         f'1₸ (тенге) = {kzt_to_rub:.2f}₽\n'
                         f'1₺ (тур. лира) = {try_to_rub:.2f}₽', reply_markup=rates_keyboard())


