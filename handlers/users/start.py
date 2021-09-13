import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db

import logging
import emoji


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    chat_id = message.chat.id
    user_id = message.from_user.id
    logging.info(chat_id)
    if chat_id != user_id:
        group_check = await db.select_whitelist(chat_id=chat_id)
        if group_check == None:
            await message.answer("Finish! Пиши в лс @wowdubot")
            await dp.bot.leave_chat(chat_id=chat_id)
    """try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)"""

    count = await db.count_users()

    # Забираем как список или как словарь
    #user_data = list(user)
    #user_data_dict = dict(user)

    # Забираем напрямую как из списка или словаря
    #username = user.get("username")
    #full_name = user[1]

    """await message.answer(
        "\n".join(
            [
                f'Привет, {message.from_user.full_name}!',
                f'Ты был занесен в базу',
                f'В базе <b>{count}</b> пользователей',
                "",
                f"Жми /menu"
            ]))"""

    users_info = await db.select_user(telegram_id=user_id)
    logging.info(f"user_id:{user_id} \n users_info: {users_info}")
    if users_info == None:
        text = f"""Привет, {message.from_user.full_name}!
Добро пожаловать!
С нами уже <b>{count}</b> пользователей

Первым делым тебя надо зарегистрироать. Жми /registration"""
        await message.answer(text)
    else:
        text = f"""Привет, {message.from_user.full_name}!
Добро пожаловать!
С нами уже <b>{count}</b> пользователей

Жми /menu"""
        await message.answer(text)
