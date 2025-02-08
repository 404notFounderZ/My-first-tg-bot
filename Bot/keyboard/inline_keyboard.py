from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Создаем кнопки
def get_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text='♻️Конвертация фото', callback_data='convert_image'),
        ],

        [
            InlineKeyboardButton(text='💱Конвертация валют', callback_data='convert_currency')
        ],

        [
            InlineKeyboardButton(text='📥Создание QR', callback_data='make_qr'),
            InlineKeyboardButton(text="🔒Расшифровка QR", callback_data="decode_qr")
        ],
        [
            InlineKeyboardButton(text='📝Распознание текста с фото', callback_data='recognize_cmd')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def back_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text='⬅️Назад', callback_data='return')
        ]

    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def exchange_rate_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text='💱Обновить курс', callback_data='exchange_rate')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def rates_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text='🆕Обновить курс валют', callback_data='update_rates')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
