from aiogram import executor
import logging

from loader import dp, db
import middlewares
import filters
import handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.database import create_db


async def on_startup(dispatcher):
    logging.info("Создаем подключение к базе данных")
    await db.create()

    # await db.drop_users()

    logging.info("Создаем таблицу пользователей")
    await db.create_table_users()
    logging.info("Готово.")

    logging.info("Создаем таблицу admins")
    await db.create_table_admins()
    logging.info("Готово.")

    logging.info("Создаем таблицу basket")
    await db.create_table_basket()
    logging.info("Готово.")

    logging.info("Создаем таблицу Shipping")
    await db.create_table_shipping()
    logging.info("Готово.")

    logging.info("Создаем таблицу Whitelist")
    await db.create_table_whitelist()
    logging.info("Готово.")

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    await create_db()

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
