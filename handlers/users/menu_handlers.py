
from typing import Union
from aiogram import types
import typing
from aiogram.types import CallbackQuery
import logging

from aiogram.dispatcher.filters import Command

from keyboards.inline.menu_keyboards import categories_keyboard, subcategories_keyboard,  items_keyboard, item_keyboard, menu_cd, add_to_card, item_add_done_keyboard
from keyboards.inline.basket_keyboard import save_quantity, basket_keyboard
from utils.db_api.db_commands import get_item
from loader import dp, db

from keyboards.inline.menu_keyboards import buy_item, card

import emoji


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):

    chat_id = message.chat.id
    user_id = message.from_user.id
    logging.info(chat_id)
    if chat_id != user_id:
        group_check = await db.select_whitelist(chat_id=chat_id)
        if group_check == None:
            await message.answer("Хочешь увидеть товар? Хорошо, но не здесь. Много лишних глаз. Напиши мне в лс @wowdubot")
            await dp.bot.leave_chat(chat_id=chat_id)

    users_info = await db.select_user(telegram_id=user_id)
    logging.info(f"user_id:{user_id} \n users_info: {users_info}")
    if users_info == None:
        await message.answer("Вы не зарегестрированы, пожалуйста пройдите регистрацию нажав /registration")
        pass
    else:
        await list_categories(message)


async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await categories_keyboard()

    if isinstance(message, types.Message):
        await message.answer("Выберите магазин:", reply_markup=markup)

    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def list_subcategories(callback: types.CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)
    text = "Выберите категорию:"
    await callback.message.edit_text(text=text, reply_markup=markup)


async def list_items(callback: types.CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category=category, subcategory=subcategory)
    text = "Выберите товар:"
    await callback.message.edit_text(text=text, reply_markup=markup)


async def show_item(callback: types.CallbackQuery, category, subcategory, item_id):
    markup = item_keyboard(category, subcategory, item_id)

    item = await get_item(item_id)
    text = f"{item}"
    # await сюда функцию по отправке фото через item.photo
    await callback.message.edit_text(text=text, parse_mode="markdown", reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    item_id = int(callback_data.get('item_id'))

    levels = {
        "0": list_categories,
        "1": list_subcategories,
        "2": list_items,
        "3": show_item
    }
    current_level_function = levels[current_level]

    await current_level_function(
        call,
        category=category,
        subcategory=subcategory,
        item_id=item_id
    )


@dp.callback_query_handler(buy_item.filter(quantity=["+1", "-1"]))
async def buy_item_quantity(query: types.CallbackQuery, callback_data: typing.Dict[int, int]):

    await query.answer()
    callback_data_quantity = callback_data["quantity"]

    quantity_count = int(callback_data.get("quantity_count"))

    if callback_data_quantity == "+1":
        quantity_count += 1
    else:
        quantity_count -= 1

    item_id = callback_data.get('item_id')

    quantity = quantity_count

    item_info = await db.select_item(id=int(item_id))
    item_name = item_info.get('name')
    category1 = item_info.get('category_code')
    subcategory1 = item_info.get('subcategory_code')
    price1 = item_info.get('price')

    markup = add_to_card(category=category1, subcategory=subcategory1,
                         item_id=item_id, quantity_count=quantity_count)
    text = f"""УаУ
Добавляем в корзину: {item_name}
Введите количество: {quantity}
Цена: {quantity*price1}"""
    await query.message.edit_text(text, reply_markup=markup)
    logging.info(f"Готово.{item_id}:{quantity}")


# не показ корзины, а добавление количества и товара в корзину
@dp.callback_query_handler(card.filter(show_card="show_card"))
async def show_card(query: types.CallbackQuery, callback_data: dict):
    item_id = int(callback_data.get('item_id'))
    user_id = query.from_user.id

    item_info = await db.select_item(id=item_id)
    category1 = item_info.get('category_code')
    subcategory1 = item_info.get('subcategory_code')
    admin_id = item_info.get('telegram_id')

    item_in_card = await db.select_item_id_in_card(id=user_id, items_id=item_id)

    if (item_in_card == None):
        quantity_count = int(callback_data.get("quantity_count"))
        await db.add_items_to_basket(id=user_id, items_id=item_id, quantity=quantity_count, admin_id=admin_id)
        markup = item_add_done_keyboard(
            category=category1, subcategory=subcategory1, item_id=item_id)
        text = "Готово. Товар добавлен в корзину."
        await query.message.edit_text(text, reply_markup=markup)
    else:
        quantity_count = int(callback_data.get("quantity_count"))
        await db.update_item_quantity(id=user_id, items_id=item_id, quantity=quantity_count)
        markup = item_add_done_keyboard(
            category=category1, subcategory=subcategory1, item_id=item_id)
        text = "Готово. Количество изменено."
        await query.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(buy_item.filter(quantity=["change", "change+1", "change-1"]))
async def buy_item_quantity_change(query: types.CallbackQuery, callback_data: typing.Dict[int, int]):

    await query.answer()
    callback_data_quantity = callback_data["quantity"]

    quantity_count = int(callback_data.get("quantity_count"))

    if callback_data_quantity == "change+1":
        quantity_count += 1
    else:
        quantity_count -= 1

    item_id = callback_data.get('item_id')

    quantity = quantity_count

    item_info = await db.select_item(id=int(item_id))
    item_name = item_info.get('name')
    category1 = item_info.get('category_code')
    subcategory1 = item_info.get('subcategory_code')
    price1 = item_info.get('price')

    markup = save_quantity(category=category1, subcategory=subcategory1,
                           item_id=item_id, quantity_count=quantity_count)
    text = f"""
Изменяем: {item_name}
Количество: {quantity}
Цена: {quantity*price1}"""
    await query.message.edit_text(text, reply_markup=markup)
    logging.info(f"Готово.{item_id}:{quantity}")


# не показ корзины, а добавление количества и товара в корзину
@dp.callback_query_handler(card.filter(show_card="save_card"))
async def save_card(query: types.CallbackQuery, callback_data: dict):
    item_id = int(callback_data.get('item_id'))
    user_id = query.from_user.id

    item_info = await db.select_item(id=item_id)
    category1 = item_info.get('category_code')
    subcategory1 = item_info.get('subcategory_code')
    item_name = item_info.get('name')
    description = item_info.get('description')
    price = item_info.get('price')
    photo = item_info.get('photo')

    item_in_card = await db.select_item_id_in_card(id=user_id, items_id=item_id)

    quantity_count = int(callback_data.get("quantity_count"))
    await db.update_item_quantity(id=user_id, items_id=item_id, quantity=quantity_count)
    markup = basket_keyboard(item_id=item_id, quantity_count=quantity_count)
    #markup = item_add_done_keyboard(category= category1, subcategory= subcategory1, item_id=item_id)
    text = f"""Товар №{item_id} {item_name}, 
Описание: {description}
Количество: {quantity_count} 
Цена: {price*quantity_count}₽"""
    await query.message.edit_text(text, parse_mode="markdown", reply_markup=markup)
