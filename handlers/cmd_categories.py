import sqlite3
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router_categ = Router()

@router_categ.message(Command('categories'))
async def cmd_finans(message: Message):
    try:
        user_id = message.from_user.id
        with sqlite3.connect('finansi.db') as conn:
            
            cur = conn.cursor()
            
            cur.execute("""
                SELECT date, nazvanie, summa, opisanie 
                FROM finans 
                WHERE user_id = ?
                ORDER BY date DESC
                LIMIT 10
            """, (user_id,))
            
            records = cur.fetchall()
            
            if not records:
                await message.answer("Записей нет. Добавьте первую запись!")
                return
                
            response = "✍ Последние записи:\n\n"
            for date, nazvanie, summa, opisanie in records:
                response += f"📅 {date}\n"
                response += f"🎟️ {nazvanie}\n"
                response += f"💸 {summa} руб.\n"
                response += f"📝 {opisanie}\n"
                response += "─" * 20 + "\n\n"
                
            await message.answer(response)
            
    except sqlite3.Error as e:
        await message.answer(f"Ошибка базы данных: {e}")