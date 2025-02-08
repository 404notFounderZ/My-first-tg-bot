import asyncio
from aiogram import Dispatcher, Bot

from running import BOT_TOKEN

from handlers import handler_commands
from Bot.handlers.handler_photo import main_photo
from Bot.callbacks import handler_callback, currency_callback
from Bot.handlers.handler_text import main_text


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_routers(
        handler_commands.router,
        main_text.router,
        main_photo.router,
        handler_callback.router,
        currency_callback.router

    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
