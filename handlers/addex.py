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
        [KeyboardButton(text='🛒 Продукты')], 
        [KeyboardButton(text='🚍 Транспорт')],
        [KeyboardButton(text='🥳 Развлечение')],
        [KeyboardButton(text='🛍️ Shoping')]
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
       
    text = message.text.strip().replace(' ', '').replace(',', '.')
        
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
        await save_expense_from_callback(callback, state, '')


@router_addex.message(FinanceUser.vibrat_text_opicanie)
async def process_description_text(message: Message, state: FSMContext):
    description = message.text.strip()
    if len(description) > 500:
        await message.answer("Описание слишком длинное. Максимум 500 символов.")
        return
    
    await save_expense(message, state, description)


async def save_expense(message: Message, state: FSMContext, description: str = ''):
    try:
        data = await state.get_data()
        nazvanie = data.get('nazvanie')
        summa = data.get('summ')
        
        if not nazvanie or not summa:
            await message.answer("❌ Ошибка: данные не найдены")
            await state.clear()
            return
        
        conn = sqlite3.connect('finansi.db') 
        cursor = conn.cursor()
        
        current_date = datetime.now().strftime('%Y.%m.%d')
        users_id = message.from_user.id
        
        print(f"✅ DEBUG save_expense: user_id = {users_id}")
        
        cursor.execute('''
            INSERT INTO finans (user_id, date, nazvanie, summa, opisanie)
            VALUES (?, ?, ?, ?, ?)
        ''', (users_id, current_date, nazvanie, summa, description))
        
        conn.commit()
        conn.close()
        
        await message.answer(
            f"✅ Трата успешно сохранена!\n\n"
            f"📋 Категория: {nazvanie}\n"
            f"💰 Сумма: {summa:.2f} руб.\n"
            f"📅 Дата: {datetime.now().strftime('%d.%m.%Y')}\n"
            f"{f'📝 Описание: {description}' if description else '📝 Описание: не указано'}"
        )
        
        await state.clear()
        
    except sqlite3.Error as e:
        await message.answer(f"❌ Ошибка базы данных: {str(e)}")
        await state.clear()



async def save_expense_from_callback(callback: CallbackQuery, state: FSMContext, description: str = ''):
    try:
        data = await state.get_data()
        nazvanie = data.get('nazvanie')
        summa = data.get('summ')
        
        if not nazvanie or not summa:
            await callback.message.answer("❌ Ошибка: данные не найдены")
            await state.clear()
            return
        
        conn = sqlite3.connect('finansi.db') 
        cursor = conn.cursor()
        
        current_date = datetime.now().strftime('%Y.%m.%d')
        # ВАЖНО: user_id берем из callback.from_user
        users_id = callback.from_user.id
        
        print(f"✅ DEBUG save_expense_from_callback: user_id = {users_id}")
        
        cursor.execute('''
            INSERT INTO finans (user_id, date, nazvanie, summa, opisanie)
            VALUES (?, ?, ?, ?, ?)
        ''', (users_id, current_date, nazvanie, summa, description))
        
        conn.commit()
        conn.close()
        
        await callback.message.answer(
            f"✅ Трата успешно сохранена!\n\n"
            f"📋 Категория: {nazvanie}\n"
            f"💰 Сумма: {summa:.2f} руб.\n"
            f"📅 Дата: {datetime.now().strftime('%d.%m.%Y')}\n"
            f"{f'📝 Описание: {description}' if description else '📝 Описание: не указано'}"
        )
        
        await state.clear()
        
    except sqlite3.Error as e:
        await callback.message.answer(f"❌ Ошибка базы данных: {str(e)}")
        await state.clear()



@router_addex.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нет активной операции для отмены.")
        return
    
    await state.clear()
    await message.answer("✅ Операция отменена.", reply_markup=ReplyKeyboardRemove())