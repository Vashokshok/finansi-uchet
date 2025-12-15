import sqlite3
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime


router_addex = Router()

class FinanceUser(StatesGroup):
    vibrat_nazvanie = State()
    vibrat_summa = State()
    vibrat_opicanie = State()
    vibrat_text_opicanie = State()


@router_addex.message(Command('addexpence'))
async def cmd_addexpebce(message: Message, state: FSMContext):
    keyboards = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🛍️ Продукты')], 
        [KeyboardButton(text='🚍 Транспорт')],
        [KeyboardButton(text='🥳 Развлечение')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
    )
    await message.answer('Пожалуйста выберите название траты: ', reply_markup=keyboards)
    await state.set_state(FinanceUser.vibrat_nazvanie)


@router_addex.message(FinanceUser.vibrat_nazvanie)
async def viborka(message: Message, state: FSMContext):
    await state.update_data(nazvanie=message.text)
    await message.answer('Пожалуйста введите сумму трат:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FinanceUser.vibrat_summa)


@router_addex.message(FinanceUser.vibrat_summa)
async def viborka3(message: Message, state: FSMContext):

        # Удаляем пробелы и заменяем запятые на точки
    text = message.text.strip().replace(' ', '').replace(',', '.')
        
        # Проверяем, что это число
    summa = float(text)
        
    if summa <= 0:
        await message.answer('Сумма должна быть больше нуля!')
        return
    if summa >= 1000000:
        await message.answer('Вы превысили максимальную сумму затрат (1,000,000)')
        return
        
    await state.update_data(summ=summa)

    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='✅ Добавить описание', callback_data='yes')],
            [InlineKeyboardButton(text='❌ Без описания', callback_data='no')]
        ])

    await message.answer(f'Вы ввели сумму: {summa:.2f}\n\nДобавить описание к этой трате?', reply_markup=inline_keyboard)
    await state.set_state(FinanceUser.vibrat_opicanie)



@router_addex.callback_query(FinanceUser.vibrat_opicanie)
async def process_description_choice(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    if callback.data == 'yes':
        await callback.message.answer('Введите описание траты:')
        await state.set_state(FinanceUser.vibrat_text_opicanie)
    elif callback.data == 'no':
        # Сохраняем без описания
        await save_expense(callback.message, state, '')
        await state.clear()


@router_addex.message(FinanceUser.vibrat_text_opicanie)
async def process_description_text(message: Message, state: FSMContext):
    description = message.text.strip()
    if len(description) > 500:
        await message.answer("Описание слишком длинное. Максимум 500 символов.")
        return
    
    await save_expense(message, state, description)


async def save_expense(message: Message, state: FSMContext, description: str = ''):
    try:
        # Получаем данные из состояния
        data = await state.get_data()
        nazvanie = data.get('nazvanie')
        summa = data.get('summ')
        
        if not nazvanie or not summa:
            await message.answer("❌ Ошибка: данные не найдены")
            await state.clear()
            return
        
        # Подключаемся к ПРАВИЛЬНОЙ базе данных
        conn = sqlite3.connect('finansi.db')  # Изменено с finance.db на finansi.db
        cursor = conn.cursor()
        
        # Получаем текущую дату
        current_date = datetime.now().strftime('%Y.%m.%d')
        
        # Вставляем данные в ПРАВИЛЬНУЮ таблицу
        cursor.execute('''
            INSERT INTO finans (date, nazvanie, summa, opisanie)
            VALUES (?, ?, ?, ?)
        ''', (current_date, nazvanie, summa, description))
        
        conn.commit()
        conn.close()
        
        # Отправляем подтверждение
        await message.answer(
            f"✅ Трата успешно сохранена!\n\n"
            f"📋 Категория: {nazvanie}\n"
            f"💰 Сумма: {summa:.2f} руб.\n"
            f"📅 Дата: {datetime.now().strftime('%d.%m.%Y')}\n"
            f"{f'📝 Описание: {description}' if description else '📝 Описание: не указано'}"
        )
        
        # Очищаем состояние
        await state.clear()
        
    except sqlite3.Error as e:
        await message.answer(f"❌ Ошибка базы данных: {str(e)}")
        await state.clear()



# Обработка отмены на любом этапе
@router_addex.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нет активной операции для отмены.")
        return
    
    await state.clear()
    await message.answer("✅ Операция отменена.", reply_markup=ReplyKeyboardRemove())