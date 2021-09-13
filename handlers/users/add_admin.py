import logging

from aiogram.dispatcher.storage import FSMContext

from loader import dp, db
from states.add_admin import Add_admin

from aiogram import Dispatcher,  types
from aiogram.dispatcher.filters import Command

from data.config import SUPERADMIN_ID

from utils.db_api.database import create_db

import asyncio


@dp.message_handler(Command("add_admin"), state=None)
async def add_admins(message: types.Message):
    superadmin_id = SUPERADMIN_ID
    if message.from_user.id == superadmin_id:
        await message.answer("Процесс пошел, Введите ID админа:")
        await Add_admin.Q1.set()
    else:
        await message.answer("Вы не являетесь администратором")


@dp.message_handler(state=Add_admin.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    await message.answer("Введите название магазина")
    await Add_admin.next()


@dp.message_handler(state=Add_admin.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    await message.answer("Введите код магазина, на английском")
    await Add_admin.next()


@dp.message_handler(state=Add_admin.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer3=answer)
    await message.answer("Введите ID человека или группы куда будут приходить заказы, для принятия заказов")
    await Add_admin.next()


@dp.message_handler(state=Add_admin.Q4)
async def answer_q4(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer4=answer)
    await message.answer("Введите адрес магазина")
    await Add_admin.next()


@dp.message_handler(state=Add_admin.Q5)
async def answer_q4(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer5=answer)
    await message.answer("Введите TOKEN оплаты")
    await Add_admin.next()


@dp.message_handler(state=Add_admin.Q6)
async def answer_q5(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer6=answer)
    # Достаем переменные
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    answer3 = data.get("answer3")
    answer4 = data.get("answer4")
    answer5 = data.get("answer5")
    answer6 = data.get("answer6")

    await message.answer("Спасибо за ваши ответы!")

    await db.add_admin(id=int(answer1),
                       shop_name=str(answer2),
                       shop_code=str(answer3),
                       notify_id=int(answer4),
                       adress=str(answer5),
                       open_close="false",
                       TOKEN=str(answer6),
                       summ_cash=0,
                       wow_cash=0)

    # Вариант 1
    await state.finish()
    await state.reset_state()


loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
# loop.run_until_complete(answer_q3())
