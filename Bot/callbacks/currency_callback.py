import os

import aiohttp
from aiogram import Router, types
from dotenv import load_dotenv

from Bot.handlers.handler_text.currency import get_exchange_cur
from Bot.keyboard.inline_keyboard import (exchange_rate_keyboard,
                                          rates_keyboard)

from Bot.handlers.handler_text.currency import currency_name
load_dotenv()
URL_EXCHANGE_RATES = os.getenv('URL_EXCHANGE_RATES')
router = Router()


@router.callback_query(lambda c: c.data == 'exchange_rate')
async def ex_callback(callback_query: types.CallbackQuery):
    amount, source_currency = currency_name(callback_query.message.text.lower())

    if amount and source_currency:
        conversion_rates = await get_exchange_cur()
        print(f'    Текущий курс по USD: {conversion_rates}')

        if source_currency != 'USD':
            amount_usd = amount / conversion_rates[source_currency]
        else:
            amount_usd = amount

        conversions = {
            'EUR': amount_usd * conversion_rates['EUR'],
            'USD': amount_usd,
            'RUB': amount_usd * conversion_rates['RUB'],
            'KZT': amount_usd * conversion_rates['KZT']
        }

        print(f'    Конвертация: {conversions}')

        response = '💱Обновление по текущему курсу: \n\n'
        for curr, value in conversions.items():
            if curr == 'EUR':
                response += f'💶{value:.2f}€\n'
            elif curr == 'USD':
                response += f'💵{value:.2f}$\n'
            elif curr == 'RUB':
                response += f'💳{value:.2f}₽\n'
            elif curr == 'KZT':
                response += f'😭{value:.2f}₸\n'

        # Проверяем, изменился ли текст сообщения
        if callback_query.message.text.lower() != response:
            await callback_query.message.edit_text(response)
            await callback_query.message.edit_text(response, reply_markup=exchange_rate_keyboard())

    await callback_query.answer()


@router.callback_query(lambda c: c.data == 'update_rates')
async def update_rates_callback(callback_query: types.CallbackQuery):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_EXCHANGE_RATES) as response:
            data = await response.json()

            if data['result'] == 'success':
                usd_to_rub = data['conversion_rates']['RUB']
                eur_to_usd = data['conversion_rates']['EUR']
                kzt_to_usd = data['conversion_rates']['KZT']

                eur_to_rub = (1 / eur_to_usd) * usd_to_rub
                kzt_to_rub = (1 / kzt_to_usd) * usd_to_rub

                # Обновленный текст с курсами
                updated_info = (
                    f'💰Курс валют в рублях: \n\n'
                    f'1$ (доллар) = {usd_to_rub:.2f}₽\n'
                    f'1€ (евро) = {eur_to_rub:.2f}₽\n'
                    f'1₸ (тенге) = {kzt_to_rub:.2f}₽')
            else:
                updated_info = '❌Не удалось обновить курс валют'

            update_text = callback_query.message.text.lower()
            if update_text != updated_info:
                await callback_query.message.edit_text(updated_info)

        await callback_query.message.edit_text(updated_info, reply_markup=rates_keyboard())
    await callback_query.answer()
