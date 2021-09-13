from typing import Union
from aiogram import types
from aiogram.dispatcher.filters import Command
from utils.db_api.db_commands import get_items_id

from keyboards.inline.menu_keyboards import basket
from loader import dp, db

import logging

from keyboards.inline.basket_keyboard import admins_notify, buy_all_card


@dp.callback_query_handler(buy_all_card.filter(all_card="buy_all_card1"))
async def buy_all_card1(query: types.CallbackQuery, callback_data: dict):
    logging.info("Кнопка нажата")
    user_id = query.from_user.id

    user_info = await db.select_user(telegram_id=user_id)
    user_name = user_info.get("full_name")

    items = await get_items_id(user_id)
    for item1 in items:

        item_info = await db.select_item(id=int(item1.items_id))
        item_name = item_info.get('name')
        item_price = item_info.get('price')
        admin_id = item_info.get('telegram_id')

        text = f"""=====================
Заказ: №{item1.items_id} {item_name}, 
Количество: {item1.quantity} 
Цена: {item_price*item1.quantity}₽   
=====================
Заказчик:{user_name}
ID:{user_id}
                """

        markup = admins_notify(
            item_id=item1.items_id, quantity_count=item1.quantity)
        await dp.bot.send_message(admin_id, text, parse_mode="markdown", reply_markup=markup)


@dp.callback_query_handler(buy_all_card.filter(all_card="all_card2"))
async def buy_all_card1(query: types.CallbackQuery, callback_data: dict):
    logging.info("Кнопка нажата")
