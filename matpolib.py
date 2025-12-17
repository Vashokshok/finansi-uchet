import sqlite3
import matplotlib.pyplot as plt
import io
from aiogram.types import Message, BufferedInputFile
from collections import defaultdict

async def show_report(message: Message):
    with sqlite3.connect('finansi.db') as conn:
        user_id = message.from_user.id
        cur = conn.cursor()
        
        cur.execute("""
            SELECT nazvanie, ABS(summa)
            FROM finans 
            WHERE summa > 0
            AND user_id = ?
            ORDER BY date DESC
            LIMIT 15
        """, (user_id,))
        
        data = cur.fetchall()
        
        if not data:
            await message.answer("📭 Нет данных о расходах")
            return

        expenses = defaultdict(int)
        
        for name, amount in data:
            expenses[name] += amount

        sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
        

        top_expenses = sorted_expenses[:8]
        labels = [name[:10] + '...' if len(name) > 10 else name 
                 for name, _ in top_expenses]
        values = [amount for _, amount in top_expenses]
        
  
        plt.figure(figsize=(8, 6))
        
        if len(sorted_expenses) > 8:
            other_total = sum(amount for _, amount in sorted_expenses[8:])
            labels.append('Прочее')
            values.append(other_total)
        
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title('📊 Ваши расходы')
        
 
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        plt.close()

        await message.answer_photo(
            BufferedInputFile(buf.getvalue(), filename="report.png"),
            caption="💸 <b>Ваш финансовый отчет</b>\n\n"
                   "✅ Оплата активна\n"
                   "📅 Доступ открыт на 30 дней\n\n"
                   "Для нового отчета введите /report", parse_mode='HTML'
        )