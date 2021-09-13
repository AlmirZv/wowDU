from logging import exception
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hcode

from loader import dp, db


@dp.message_handler(Command("info"))
async def user_info(message: types.Message):
    user = await db.select_user(telegram_id=message.from_user.id)
    phone = user.get('phone_number')
    adress = user.get('user_adress')
    await message.answer(f"""Данные. Запись в БД:
{message.from_user.full_name} - /full_name - для изменения имени
{message.from_user.username} - /username - для изменения username
{phone} - /phone_number - для изменения номера телефона
{adress} - /user_adress - для изменения адреса""")


@dp.message_handler(Command("username"))
async def change_username(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id != user_id:
        group_check = await db.select_whitelist(chat_id=chat_id)
        if group_check == None:
            await dp.bot.leave_chat(chat_id=chat_id)
    await message.answer("Пришли мне свой новый username")
    await state.set_state("username")


@dp.message_handler(state="username")
async def enter_username(message: types.Message, state: FSMContext):
    await db.update_user_username(username=message.text, telegram_id=message.from_user.id)
    user = await db.select_user(telegram_id=message.from_user.id)
    user = dict(user)
    phone = user.get('phone_number')
    adress = user.get('user_adress')
    await message.answer(f"""Данные обновлены. Запись в БД:
{message.from_user.full_name} - /full_name - для изменения имени
{message.from_user.username} - /username - для изменения username
{phone} - /phone_number - для изменения номера телефона
{adress} - /user_adress - для изменения адреса""")
    await state.reset_state()


@dp.message_handler(Command("full_name"))
async def change_username(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id != user_id:
        group_check = await db.select_whitelist(chat_id=chat_id)
        if group_check == None:
            await dp.bot.leave_chat(chat_id=chat_id)
    await message.answer("Пришли мне свое имя")
    await state.set_state("full_name")


@dp.message_handler(state="full_name")
async def enter_username(message: types.Message, state: FSMContext):
    await db.update_user_full_name(full_name=message.text, telegram_id=message.from_user.id)
    user = await db.select_user(telegram_id=message.from_user.id)
    user = dict(user)
    phone = user.get('phone_number')
    adress = user.get('user_adress')
    await message.answer(f"""Данные обновлены. Запись в БД:
{message.from_user.full_name} - /full_name - для изменения имени
{message.from_user.username} - /username - для изменения username
{phone} - /phone_number - для изменения номера телефона
{adress} - /user_adress - для изменения адреса""")
    await state.reset_state()


@dp.message_handler(Command("phone_number"))
async def change_username(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id != user_id:
        group_check = await db.select_whitelist(chat_id=chat_id)
        if group_check == None:
            await dp.bot.leave_chat(chat_id=chat_id)
    await message.answer("Пришли мне свой номер телефона")
    await state.set_state("phone_number")


@dp.message_handler(state="phone_number")
async def enter_username(message: types.Message, state: FSMContext):
    if True:
        try:
            x = int(message.text)
            await db.update_user_phone_number(phone_number=x, telegram_id=message.from_user.id)
            user = await db.select_user(telegram_id=message.from_user.id)
            user = dict(user)
            phone = user.get('phone_number')
            adress = user.get('user_adress')
            await message.answer(f"""Данные обновлены. Запись в БД:
{message.from_user.full_name} - /full_name - для изменения имени
{message.from_user.username} - /username - для изменения username
{phone} - /phone_number - для изменения номера телефона
{adress} - /user_adress - для изменения адреса""")
            await state.reset_state()
            pass
        except ValueError:
            await message.answer("Вы ввели не числовое значение, попробуйте заново: /phone_number")
            x = 0
            await state.reset_state()


@dp.message_handler(Command("user_adress"))
async def change_username(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id != user_id:
        group_check = await db.select_whitelist(chat_id=chat_id)
        if group_check == None:
            await dp.bot.leave_chat(chat_id=chat_id)
    await message.answer("Пришли мне свой адрес")
    await state.set_state("user_adress")


@dp.message_handler(state="user_adress")
async def enter_username(message: types.Message, state: FSMContext):
    await db.update_user_user_adress(user_adress=message.text, telegram_id=message.from_user.id)
    user = await db.select_user(telegram_id=message.from_user.id)
    user = dict(user)
    phone = user.get('phone_number')
    adress = user.get('user_adress')
    await message.answer(f"""Данные обновлены. Запись в БД:
{message.from_user.full_name} - /full_name - для изменения имени
{message.from_user.username} - /username - для изменения username
{phone} - /phone_number - для изменения номера телефона
{adress} - /user_adress - для изменения адреса""")
    await state.reset_state()
