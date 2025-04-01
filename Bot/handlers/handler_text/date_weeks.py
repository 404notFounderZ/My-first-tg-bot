import datetime

from aiogram import types


async def cmd_time(message: types.Message):
    date_source = message.text
    try:
        date_to_str = datetime.datetime.strptime(date_source, '%d.%m.%Y').date()
        date_week_en = date_to_str.strftime('%A')
        week_rus1 = (date_week_en.replace('Monday', 'понедельник')
                     .replace('Tuesday', 'вторник')
                     .replace('Wednesday', 'среда')
                     .replace('Thursday', 'четверг')
                     .replace('Friday', 'пятница')
                     .replace('Saturday', 'суббота')
                     .replace('Sunday', 'воскресенье')
                     )

        await message.answer(f'{date_source} это {week_rus1}')
    except ValueError:
        await message.reply('Ошибка: проверьте формат даты. Используйте ДД.ММ.ГГГГ')
