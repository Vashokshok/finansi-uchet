import asyncio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router_comm = Router()


@router_comm.message(Command('start'))
async def cmd_start(message: Message):
    await message.reply(f'👋Привет, Я БОТ для отслеживания финансов и учёта\n'
                         f'🤩Я помгу ввести учет расходов, добавлять категории затрат\n'
                         f'и получать отчет за определенный период!\n\n'
                         f'У меня есть такие команды как:\n\n'
                         f'/addexpence - сможете ввести траты за день\n\n'
                         f'/categories - просмотр всех категорий\n\n'
                         f'/report - генерация отчета за определенный период')
    