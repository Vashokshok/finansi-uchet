import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from middleware.middle import LoggingfInfoMiddleware

router_comm = Router()
router_comm.message.outer_middleware(LoggingfInfoMiddleware())


@router_comm.message(Command('start'))
async def cmd_start(message: Message):
    await message.reply(f'👋Привет, Я БОТ для отслеживания финансов и учёта\n\n'
                         f'🤩Я помгу ввести учет расходов, добавлять категории затрат\n'
                         f'и получать отчет за определенный период!')
    