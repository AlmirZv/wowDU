from data.config import SUPERADMIN_ID
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp, db


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    admin = await db.select_admin(id=message.from_user.id)
    if chat_id != user_id:
        group_check = await db.select_whitelist(chat_id=chat_id)
        if group_check == None:
            await message.answer("Что за паника? Помощь в пути.")
            await dp.bot.leave_chat(chat_id=chat_id)
    if user_id == SUPERADMIN_ID:
        text = ("Список команд: ",
                "/start - Начать диалог",
                "/help - Получить справку",
                "/add_admin - Добавить админа",
                "/drop_news - Отправить новость",
                "/open_shop - Открыть магазин",
                "/close_shop - Закрыть магазин")
    elif admin != None:
        text = ("Список команд: ",
                "/start - Начать диалог",
                "/help - Получить справку",
                "/open_shop - Открыть магазин",
                "/close_shop - Закрыть магазин")
    else:
        text = ("Список команд: ",
                "/start - Начать диалог",
                "/help - Получить справку"
                )

    await message.answer("\n".join(text))
