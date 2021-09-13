from aiogram.types.message import ContentTypes
from sqlalchemy.sql.expression import false
from data.config import SUPERADMIN_ID, SUPERADMIN_TOKEN
from aiogram import types
from loader import db, dp
from aiogram.types import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cash = CallbackData("cash", "pay", "admin_id")


def cash_pay_cd(pay, admin_id):
    return cash.new(pay=pay, admin_id=admin_id)


async def cash_pay_keyboard(admin_id):

    markup = InlineKeyboardMarkup()
    # markup.row(InlineKeyboardButton(text="Добавить в корзину", callback_data=))
    markup.row(
        InlineKeyboardButton("Оплатить", callback_data=cash_pay_cd(
            pay="pay_cash", admin_id=admin_id))
    )
    return markup


@dp.callback_query_handler(cash.filter(pay="pay_cash"))
async def pay_cash1(query: types.CallbackQuery, callback_data: dict):
    admin_id = query.from_user.id
    shop_admin_info = await db.select_admin(id=admin_id)
    shop_name = shop_admin_info.get("shop_name")
    adress = shop_admin_info.get("adress")
    summ_cash = shop_admin_info.get("summ_cash")
    wow_cash = shop_admin_info.get("wow_cash")
    text = f"""В сумме заказов сделано на {summ_cash}₽, комиссия бота {wow_cash}₽"""
    await dp.bot.send_invoice(query.from_user.id,
                              title=shop_name,
                              description=text,
                              provider_token=SUPERADMIN_TOKEN,
                              currency='rub',
                              prices=[types.LabeledPrice(
                                  label=shop_name, amount=int(wow_cash)*100)],
                              payload=SUPERADMIN_ID,
                              start_parameter=12312431421231,
                              need_phone_number=False,
                              need_shipping_address=False)
    await query.message.edit_text(text=text, reply_markup=None)
