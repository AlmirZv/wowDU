import logging

from aiogram.dispatcher.storage import FSMContext
from aiogram.types.base import Integer

from loader import dp, db
from states.registration import Registr

from aiogram import Dispatcher,  types
from aiogram.dispatcher.filters import Command

from data.config import SUPERADMIN_ID

from utils.db_api.database import create_db

import asyncio


@dp.message_handler(Command("registration"), state=None)
async def add_admins(message: types.Message):

    chat_id = message.chat.id
    user_id = message.from_user.id
    logging.info(chat_id)
    if chat_id != user_id:
        group_check = await db.select_whitelist(chat_id=chat_id)
        if group_check == None:
            await message.answer("Смотри тут какая очередь на регистрацию! Но я могу пропустить тебя без очереди в лс @wowdybot")
            await dp.bot.leave_chat(chat_id=chat_id)

    users_info = await db.select_user(telegram_id=user_id)
    if users_info == None:
        await message.answer("Регистрация началась")
        full_name = message.from_user.full_name
        username = message.from_user.username
        telegram_id = message.from_user.id
        await message.answer(f"""Взяли данные из телеграма:
telegramID: {telegram_id} 
Имя: {full_name}
username: {username}
Введите номер телефона для связи(только цифры). В целях вашей безопасности, база данных закрыта и ваши данные будут передаваться только для доставки товара. Если не хотите указывать, просто введите любое число. Но в последствии, это может привести к затруднениям.""")
        await Registr.Q1.set()
    else:
        user = await db.select_user(telegram_id=message.from_user.id)
        phone = user.get('phone_number')
        adress = user.get('user_adress')
        await message.answer(f"""Вы уже зарегестрированы, жмите:
{message.from_user.full_name} - /full_name - для изменения имени
{message.from_user.username} - /username - для изменения username
{phone} - /phone_number - для изменения номера телефона
{adress} - /user_adress - для изменения адреса""")
        pass


@dp.message_handler(state=Registr.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    if answer is Integer:
        await state.update_data(phone=answer)
    else:
        await state.update_data(answer1=0)
    await message.answer("Введите адресс доставки")
    await Registr.next()


@dp.message_handler(state=Registr.Q2)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(adress=answer)

    # Достаем переменные
    data = await state.get_data()
    phone = data.get("phone")
    adress = data.get("adress")

    await message.answer(f"""Спасибо за ваши ответы!
Вы успешно зарегистрировались
Если хотите изменить данные, жмите: 
{message.from_user.full_name} - /full_name - для изменения имени
{message.from_user.username} - /username - для изменения username
{phone} - /phone_number - для изменения номера телефона
{adress} - /user_adress - для изменения адреса""")

    await db.add_user(telegram_id=message.from_user.id,
                      full_name=message.from_user.full_name,
                      username=message.from_user.username,
                      phone_number=phone,
                      user_adress=adress)

    # Вариант 1
    await state.finish()
    await state.reset_state()
