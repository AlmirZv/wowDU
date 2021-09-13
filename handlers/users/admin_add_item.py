from typing import List


from utils.db_api.db_commands import add_item
from utils.db_api.database import db_gino
from utils.db_api.models import Item, Adminss

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from states.admin_add_item import Admin_add_item

from loader import dp, db
from states.admin_add_item import Admin_add_item

from data.config import ADMINS
import logging

from utils.db_api.database import create_db

import asyncio


@dp.message_handler(Command("add_item"), state=None)
async def enter_adding(message: types.Message):
    admin = await db.select_admin(id=message.from_user.id)
    shop_name = admin.get("shop_name")
    shop_code = admin.get("shop_code")

    if admin != None:
        await message.answer("добавим товар, введите категорию продукта " + str(message.from_user.full_name))
        logging.info(f"Готово. {shop_name} != " + str(shop_code))
        await Admin_add_item.s_subcategory_name.set()
    else:
        await message.answer("не добавим товар, потому что вы не админ")
        logging.info("Готово." + str(admin))


@dp.message_handler(state=Admin_add_item.s_subcategory_name)
async def s_subcategory_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer_category=answer)
    await message.answer("Введите код категории на английском")
    await Admin_add_item.next()


@dp.message_handler(state=Admin_add_item.s_subcategory_code)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer_category_code=answer)
    await message.answer("Введите название товара")
    await Admin_add_item.next()


@dp.message_handler(state=Admin_add_item.s_name_item)
async def answer_q3(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer_item_name=answer)
    await message.answer("Введите цену товара")
    await Admin_add_item.next()


@dp.message_handler(state=Admin_add_item.s_price)
async def answer_q3(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer_item_price=answer)
    await message.answer("Введите ссылку на фото")
    await Admin_add_item.next()


@dp.message_handler(state=Admin_add_item.s_photo)
async def answer_q3(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer_photo=answer)

    # Достаем переменны
    admin = await db.select_admin(id=message.from_user.id)
    shop_name = admin.get("shop_name")
    shop_code = admin.get("shop_code")
    admin_id = int(admin.get("id"))

    data = await state.get_data()
    answer_category = data.get("answer_category")
    answer_category_code = data.get("answer_category_code")
    answer_item_name = data.get("answer_item_name")
    answer_item_price = int(data.get("answer_item_price"))
    answer_photo = data.get("answer_photo")

    await message.answer("Спасибо за ваши ответы!")

    await add_item(telegram_id=admin_id, name=answer_item_name,
                   category_name=shop_name, category_code=shop_code,
                   subcategory_name=answer_category, subcategory_code=answer_category_code,
                   price=answer_item_price, photo=answer_photo)

    # Вариант 1
    await state.finish()
    await state.reset_state()


loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
# loop.run_until_complete(answer_q3())


@dp.message_handler(Command("open_shop"), state=None)
async def enter_adding(message: types.Message):
    admin = await db.select_admin(id=message.from_user.id)
    if admin == None:
        admin = await db.select_admin(notify_id=message.chat.id)
    shop_name = admin.get("shop_name")
    shop_code = admin.get("shop_code")
    open_close = True

    if admin != None:
        await message.answer("Магазин открыт, " + str(message.from_user.full_name))
        await db.update_open_close(id=message.from_user.id, open_close=open_close)

    else:
        await message.answer("вы не админ")


@dp.message_handler(Command("close_shop"), state=None)
async def enter_adding(message: types.Message):
    admin = await db.select_admin(id=message.from_user.id)
    if admin == None:
        admin = await db.select_admin(notify_id=message.chat.id)
    shop_name = admin.get("shop_name")
    shop_code = admin.get("shop_code")
    open_close = False

    if admin != None:
        await message.answer("Магазин закрыт, " + str(message.from_user.full_name))
        await db.update_open_close(id=message.from_user.id, open_close=open_close)

    else:
        await message.answer("вы не админ")
