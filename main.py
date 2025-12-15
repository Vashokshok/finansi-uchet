import asyncio
import logging
from aiogram import Dispatcher, Bot

from config import TOKEN_BOT

from handlers.starting import router_comm
from handlers.addex import router_addex

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())



async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN_BOT)
    dp = Dispatcher()


    dp.include_router(router_comm)
    dp.include_router(router_addex)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)




if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        print('Exit')