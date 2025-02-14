import os

import aiohttp
import re
from aiogram.types import Message

from Bot.keyboard.inline_keyboard import exchange_rate_keyboard
from dotenv import load_dotenv

load_dotenv()
URL_EXCHANGE_RATES = os.getenv('URL_EXCHANGE_RATES')


# Получаем актуальные данные о валютах
async def get_exchange_cur():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_EXCHANGE_RATES) as response:
            data = await response.json()
            return {
                'USD': 1,
                'EUR': data['conversion_rates']['EUR'],
                'RUB': data['conversion_rates']['RUB'],
                'KZT': data['conversion_rates']['KZT'],
                'TRY': data['conversion_rates']['TRY']
            }


# Создаём словарь валют
def currency_name(text):
    currencies = {
        'евро': 'EUR',
        '€': 'EUR',
        'доллар': 'USD',
        'долар': 'USD',
        'долларов': 'USD',
        'доларов': 'USD',
        '$': 'USD',
        'рублей': 'RUB',
        'рубль': 'RUB',
        'руб': 'RUB',
        'р': 'RUB',
        '₽': 'RUB',
        '₸': 'KZT',
        'тенге': 'KZT',
        'т': 'KZT',
        'TRY': 'TRY',
        'лиры': 'TRY',
        '₺': 'TRY'
    }
    # Создаём регулярное выражение для вытаскивания суммы и валюты из сообщения
    numbers = re.findall(r'\d+(?:\.\d+)?', text.lower())
    # Если суммы и валюты нет, то функция не выполняется
    if not numbers:
        return None, None

    # берет первое число из списка, в float потому что числа могут быть дробными
    amount = float(numbers[0])
    detected_cur = None
    for curr_name, curr_code in currencies.items():
        if curr_name in text.lower():
            # валюта была найдена
            detected_cur = curr_code
            break
    return amount, detected_cur  # таким образом весь этот блок ищет число и определяет валюту


# Создаем функцию для конвертации валют
async def convert_cur(message: Message):
    amount, source_currency = currency_name(message.text)
    print(f'    Информация о пользователе: {message.from_user}')
    if amount and source_currency:  # сумма и исходное число
        conversion_rates = await get_exchange_cur()

        print(f'    Текущий курс по USD: {conversion_rates}')  # в терминал выводится текущий курс валют по USD
        # Если исходная валюта не доллары, то производиться следующие операции
        if source_currency != 'USD':
            amount_usd = amount / conversion_rates[source_currency]
        # Если доллары, то оставляем их
        else:
            amount_usd = amount
        # Словарь конвертации валют
        conversions = {'EUR': amount_usd * conversion_rates['EUR'],
                       'USD': amount_usd,
                       'RUB': amount_usd * conversion_rates['RUB'],
                       'KZT': amount_usd * conversion_rates['KZT'],
                       'TRY': amount_usd * conversion_rates['TRY']
                       }
        print(f'    Конвертация: {conversions}')  # сообщение для проверки работы функции конвертирования
        # Формирование итогового сообщения пользователю
        response = '💱Перевод по текущему курсу: \n\n'
        for curr, value in conversions.items():
            if curr == 'EUR':
                response += f'💶{value:.2f}€\n'
            elif curr == 'USD':
                response += f'💵{value:.2f}$\n'
            elif curr == 'RUB':
                response += f'💳{value:.2f}₽\n'
            elif curr == 'TRY':
                response += f'💳{value:.2f}₺\n'
            else:
                response += f'😭{value:.2f}₸\n'
        # Отправка сообщения вместе с кнопкой обновления курса
        update_cur = await message.reply(response, reply_markup=exchange_rate_keyboard())
        return update_cur.message_id
