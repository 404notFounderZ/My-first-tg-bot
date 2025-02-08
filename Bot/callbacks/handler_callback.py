from aiogram.enums import ParseMode
from aiogram import Router, types

from Bot.running import SUPPORTED_FORMATS
from Bot.keyboard.inline_keyboard import get_keyboard, back_keyboard

router = Router()


# обработка нажатий на инлайн кнопки
@router.callback_query(lambda c: c.data in ['convert_image', 'convert_currency',
                                            'make_qr', 'decode_qr'])
async def process_callback(callback_query: types.CallbackQuery):
    reply = callback_query.data
    if reply == 'convert_image':
        await callback_query.message.edit_text(
            '<b><i>♻️Конвертация фото или файлов:</i></b>\n\n'
            '    Отправь мне изображение или файл и укажи формат для конвертации.\n'
            f'\n<b>📌Поддерживаемые форматы: {',  '.join(SUPPORTED_FORMATS)}.</b>\n\n',
            parse_mode=ParseMode.HTML, reply_markup=back_keyboard())

    elif reply == 'convert_currency':
        await callback_query.message.edit_text(
            '<b><i>💱Конвертация валют:</i></b>\n\n'
            '    Отправь мне сообщение с указанием суммы и валюты, обязательно добавив '
            '<u>восклицательный знак</u> в начало сообщения.\n '
            '<b>📌Например: !14.88$</b>\n\n'
            '    Также я могу прислать вам актуальный курс валют, для этого отправьте /rates',
            parse_mode=ParseMode.HTML, reply_markup=back_keyboard())

    elif reply == 'make_qr':
        await callback_query.message.edit_text(
            '<b><i>📥Создание QR-кода:</i></b>\n\n'
            '    Отправь мне текст или ссылку и я создам QR-код.\n\n',
            parse_mode=ParseMode.HTML, reply_markup=back_keyboard())

    elif reply == 'decode_qr':
        await callback_query.message.edit_text(
            '<b><i>🔒Расшифровка QR-кода:</i></b>\n\n'
            '    Отправь мне фото QR-кода без подписи и я расшифрую его.\n\n'
            '<b>📌Только стандартные (черно-белые) QR-коды.</b>',
            parse_mode=ParseMode.HTML, reply_markup=back_keyboard())

    await callback_query.answer()  # убираем анимацию кнопки


@router.callback_query(lambda c: c.data == 'return')
async def new_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        f'👋Привет!\nЯ многофункциональный бот. Все мои возможности отмечены ниже.',
        reply_markup=get_keyboard())
    await callback_query.answer()


@router.callback_query(lambda c: c.data == 'recognize_cmd')
async def rec_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        '   <b><i>📝Распознание текста с фото:</i></b>\n\n'
        '    Отправь мне фото и добавь подпись <u>распознать</u> в любом регистре '
        'и я смогу распознать текст с вашего изображения.\n\n',
        #'<b>📌Функция ещё <u>сырая</u> поэтому может не очень хорошо работать, обучу её попозже.</b>',
        parse_mode=ParseMode.HTML, reply_markup=back_keyboard()
    )
    await callback_query.answer()
