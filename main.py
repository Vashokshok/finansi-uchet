import asyncio
import logging
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand

from utils.config import TOKEN_BOT
from middleware.middle import LoggingInfoMiddleware

from handlers.starting import router_comm
from handlers.addex import router_addex
from handlers.cmd_categories import router_categ
from handlers.payment import router_pay


from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())



async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN_BOT)
    dp = Dispatcher()

    dp.update.outer_middleware(LoggingInfoMiddleware())

    dp.include_router(router_comm)
    dp.include_router(router_addex)
    dp.include_router(router_categ)
    dp.include_router(router_pay)

    

    await bot.set_my_commands([
        BotCommand(command='/start', description='Запуск бота'),
        BotCommand(command='/addexpence', description='Ввод трат'),
        BotCommand(command='/categories', description='Просмотр всех категорий'),
        BotCommand(command='/report', description='Генерация отчета')
    ])

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)




if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print('Exit')