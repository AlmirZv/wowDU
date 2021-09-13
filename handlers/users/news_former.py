import logging

from aiogram.dispatcher.storage import FSMContext

from loader import dp, db
from states.news_form import NewsForm

from aiogram import Dispatcher,  types
from aiogram.dispatcher.filters import Command

from data.config import SUPERADMIN_ID

from utils.db_api.database import create_db

import asyncio
import emoji


@dp.message_handler(Command("drop_news"), state=None)
async def add_admins(message: types.Message):
    superadmin_id = SUPERADMIN_ID
    if message.from_user.id == superadmin_id:
        await message.answer("Процесс пошел, Введите название темы")
        await NewsForm.Q1.set()
    else:
        await message.answer("Вы не являетесь администратором")


@dp.message_handler(state=NewsForm.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    await message.answer("Введите текст сообщения")
    await NewsForm.next()


@dp.message_handler(state=NewsForm.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    await message.answer("Введите ссылку на фото")
    await NewsForm.next()


@dp.message_handler(state=NewsForm.Q3)
async def answer_q5(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer3=answer)
    # Достаем переменные
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    answer3 = data.get("answer3")

    await message.answer("Спасибо за ваши ответы!")

    users = await db.select_all_users()
    for one_user in users:
        user_id = one_user.get("telegram_id")
        text = f"""**{answer1}**

*{answer2}*
[{emoji.emojize(":T-Rex:")}]({answer3})
"""
        try:
            await dp.bot.send_message(user_id, text=text, parse_mode="MARKDOWN", reply_markup=None)
        except:
            logging.info("bot blocked")
            logging.info(user_id)
            pass
    # await message.answer(text=text, parse_mode="MARKDOWN", reply_markup=None)
    # Вариант 1
    await state.finish()
    await state.reset_state()


loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
