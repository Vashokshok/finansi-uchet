from aiogram import Router
from aiogram.types import Message, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

from matpolib import show_report
from utils.config import PYMENTS_TOKEN
from utils.constants import PRICE

router_pay = Router()


paid_users = set()

@router_pay.message(Command('report'))
async def cmd_report(message: Message):
    user_id = message.from_user.id
    
    if user_id in paid_users:
        await show_report(message)
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить доступ", callback_data="pay_access")]
            ]
        )
        
        await message.answer(
            "📊 <b>Доступ к отчетам</b>\n\n"
            "Для просмотра финансовых отчетов необходимо приобрести доступ.\n\n"
            "Что вы получите:\n"
            "✅ Детальные графики расходов\n"
            "✅ Анализ по категориям\n"
            "✅ Визуализацию данных\n\n"
            "Стоимость: 100 руб.\n"
            "Срок действия: 1 месяц",
            reply_markup=keyboard, parse_mode='HTML'
        )

@router_pay.callback_query(lambda c: c.data == "pay_access")
async def process_pay_callback(callback_query: CallbackQuery):

    await callback_query.answer()  
    await callback_query.message.delete()  

    await callback_query.bot.send_invoice(
        chat_id=callback_query.message.chat.id,
        title='📊 Доступ к финансовым отчетам',
        description='Полный доступ к графикам и аналитике на 1 месяц',
        payload='premium-access',
        provider_token=PYMENTS_TOKEN,
        currency='RUB',
        prices=PRICE
    )


@router_pay.pre_checkout_query()
async def checkout_handlers(query: PreCheckoutQuery):
    await query.answer(ok=True)


@router_pay.message(lambda message: message.successful_payment is not None)
async def successful_payment_handler(message: Message):
    user_id = message.from_user.id
    paid_users.add(user_id)

    await message.answer('✅ Оплата прошла успешно! Создаю ваш отчет...')

    await show_report(message)
