import datetime
import os

import aiohttp
from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from Bot.keyboard.inline_keyboard import get_keyboard, rates_keyboard
from Bot.running import HELP_COM
from dotenv import load_dotenv

load_dotenv()
URL_EXCHANGE_RATES = os.getenv('URL_EXCHANGE_RATES')
router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    current_time = datetime.datetime.now().time()
    print(f'    Информация о пользователе: {message.from_user}')
    print(f'Время отправки сообщения пользователем: {current_time}')
    print('Пользователь использовал команду /start')
    await message.answer(
        f'👋Привет {message.from_user.first_name}!\nЯ многофункциональный бот. Все мои возможности отмечены ниже.',
        reply_markup=get_keyboard())


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    current_time = datetime.datetime.now().time()
    print(f'    Информация о пользователе: {message.from_user}')
    print(f'Время отправки сообщения пользователем: {current_time}')
    print('Пользователь использовал команду /help')
    await message.answer(f'Мои команды:\n{HELP_COM}')


@router.message(Command('get_info'))
async def cmd_info(message: Message):
    current_time = datetime.datetime.now().time()
    print(f'    Информация о пользователе: {message.from_user}')
    print(f'Время отправки сообщения пользователем: {current_time}')
    print('Пользователь использовал команду /get_info')
    await message.answer(f'Твой ID: <code>{message.from_user.id}</code>\n'
                         f'Твой username: @{message.from_user.username}', parse_mode=ParseMode.HTML)

@router.message(Command('support'))
async def cmd_support(message: Message):
    await message.answer(
        f'🙁Техподдержка:\n\nЕсли при использовании бота возникла ошибка, пишите в личные сообщения '
        f'<a href="t.me/denis9F">Денису</a>', parse_mode=ParseMode.HTML)

@router.message(Command('rates'))
async def cmd_rates(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_EXCHANGE_RATES) as response:
            data = await response.json()
            print('Пользователь использовал команду /rates')

            if data['result'] == 'success':
                usd_to_rub = data['conversion_rates']['RUB']
                eur_to_usd = data['conversion_rates']['EUR']
                kzt_to_usd = data['conversion_rates']['KZT']

                eur_to_rub = (1 / eur_to_usd) * usd_to_rub
                kzt_to_rub = (1 / kzt_to_usd) * usd_to_rub

            else:
                await message.answer('❌Не удалось получить актуальный курс валют')

    await message.answer(f'💰Курс валют в рублях: \n\n'
                         f'1$ (доллар) = {usd_to_rub:.2f}₽\n'
                         f'1€ (евро) = {eur_to_rub:.2f}₽\n'
                         f'1₸ (тенге) = {kzt_to_rub:.2f}₽', reply_markup=rates_keyboard())
