from handlers.users.admin_pay_cash import cash_pay_keyboard
from sqlalchemy.sql.expression import null
from data.config import SUPERADMIN_ID, TESTPAY_TOKEN
from typing import Union
from aiogram import types
from aiogram.types import invoice
from aiogram.types.message import ContentTypes
from aiogram.dispatcher.filters import Command
from utils.db_api.db_commands import get_items_id, get_shop_items

from keyboards.inline.menu_keyboards import basket, show_basket_keyboard
from loader import dp, db

import logging

from keyboards.inline.basket_keyboard import basket_keyboard, basket_keyboard02, basket_keyboard2, admins_notify, basket1, basket2, order_ready, shipping, basket_keyboard3, shipping_delete, shipping_edit_keyboard, shipping_edit_keyboard2, shipping_keyboard, shipping_keyboard2


# показ корзины\
@dp.callback_query_handler(basket.filter(show_basket="my_basket"))
async def show_basket(query: types.CallbackQuery, callback_data: dict):
    await query.message.answer("==========КОРЗИНА==========")
    user_id = query.from_user.id
    item_in_card = await db.select_item_in_card(id=user_id)
    logging.info(item_in_card)

    items = await get_items_id(user_id)
    x = 0
    summ_price = 0

    shipping_price = 50
    shops = []

    if items is not None:
        for item1 in items:
            x = x+1
            logging.info(item1.items_id)
            logging.info(f"item1: {item1}")
            item_info = await db.select_item(id=int(item1.items_id))
            item_name = item_info.get('name')
            item_price = item_info.get('price')
            description = item_info.get('description')

            shop_name = item_info.get('category_name')

            if shop_name not in shops:
                shops.append(shop_name)
                shipping_price += 50
                shipping_description = f"доставка с точек: {shops}"

            summ_price = summ_price+item_price*item1.quantity
            logging.info(f"summ_price: {summ_price}")

            text = f"""Товар №{item1.items_id} {item_name}, 
Описание: {description}
Количество: {item1.quantity} 
Цена: {item_price*item1.quantity}₽              
                """
            markup = basket_keyboard(
                item_id=item1.items_id, quantity_count=item1.quantity)
            await query.message.answer(text=text, parse_mode="markdown", reply_markup=markup)
            logging.info(text)
            if item1 == None:
                await query.message.answer("Корзина пуста. Нажмите /menu для возврата")
        else:
            if x == 0:
                await query.message.answer("Корзина пуста. Нажмите /menu для возврата")
            elif x != 0:
                text = f"=========КОНЕЦ========== \n Общая сумма: {summ_price}₽ \n========================="

                if item1.items_id == int(-1):
                    markup = basket_keyboard02(user_id, shipping_price)
                else:
                    markup = basket_keyboard2(user_id, shipping_price)
                await query.message.answer(text, reply_markup=markup)
    else:
        await query.message.answer("Корзина пуста. Нажмите /menu для возврата")


@dp.callback_query_handler(basket1.filter(basket_edit="delete_item"))
async def delete_item(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    item_id = int(callback_data.get("item_id"))
    logging.info(item_id)
    await db.delete_item_in_card(id=user_id, items_id=item_id)
    text = "Готово. Товар удален."
    await query.message.edit_text(text=text, reply_markup=None)


@dp.callback_query_handler(basket1.filter(basket_edit="clear_card"))
async def clear_card(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    item_id = int(callback_data.get("item_id"))
    logging.info(item_id)
    await db.clear_card(id=user_id)
    text = "Готово. Корзина очищена."
    await query.message.edit_text(text=text, reply_markup=None)


@dp.callback_query_handler(basket1.filter(basket_edit="buy_all_card"))
async def buy_all_card1(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id

    user_info = await db.select_user(telegram_id=user_id)
    user_name = user_info.get("full_name")

    items = await get_items_id(user_id)

    y = []
    z = {}  # создает список библиотек с admin_id и привязанным к ним текстом товара

    # Для инвойса, создания счета для оплаты для каждого магазина
    x = {}
    amount = {}
    # ----------------------------------------------------------------

    for item1 in items:

        item_info = await db.select_item(id=int(item1.items_id))
        item_name = item_info.get('name')
        item_price = item_info.get('price')
        admin_id = item_info.get('telegram_id')

        shop_name = item_info.get('category_name')

        admins_info = await db.select_admin(id=admin_id)
        notify_id = admins_info.get('notify_id')
        shop_name = admins_info.get('shop_name')

# Распределие товаров в корзине по аминистраторам:
        if admin_id not in z:

            # Для инвойса, создания счета для оплаты для каждого магазина
            description = f"""|| {item_name} - {item1.quantity}шт. - {item_price*item1.quantity}₽ || 
"""
            x[notify_id] = description
            amount[notify_id] = item_price*item1.quantity
            # ----------------------------------------------------------------

            # Для создания чека отправки магазину и покупателю
            text = f"""=====================
Заказ: №{item1.items_id} {item_name}, 
Количество: {item1.quantity} 
Цена: {item_price*item1.quantity}₽   
=====================
"""
            #order_text = "Поступил заказ:"
            # await dp.bot.send_message(notify_id, order_text, parse_mode="markdown")
            z[notify_id] = text
            #z[admin_id] = 1
            y.append(notify_id)
            summ_price = item_price*item1.quantity
            # -------------------------------
        else:

            # Для инвойса, создания счета для оплаты для каждого магазина
            description = f"""{item_name} - {item1.quantity}шт. - {item_price*item1.quantity}₽ || 
"""
            x[notify_id] += description
            amount[notify_id] += item_price*item1.quantity
            # -------------------------------

            # Для создания чека отправки магазину и покупателю
            text = f"""Заказ: №{item1.items_id} {item_name}, 
Количество: {item1.quantity} 
Цена: {item_price*item1.quantity}₽   
=====================
"""
            z[notify_id] += text
            summ_price += item_price*item1.quantity
            # ------------------------------

        # await dp.bot.send_message(notify_id, text, parse_mode="markdown")
    else:
        for one in x:

            # Для инвойса, создания счета для оплаты для каждого магазина
            #description = f"""Общая стоимость заказа: {amount[one]}₽"""
            #x[one] += description
            # -------------------------------

            # Для создания чека отправки магазину и покупателю
            text = f"""Общая стоимость заказа: {amount[one]}₽
=====================            
Заказчик:{user_name} \nID:{user_id}"""
            z[one] += text
            user_id = query.from_user.id

            # await dp.bot.send_message(one, z[one], parse_mode="markdown", reply_markup=markup)
            # await query.message.answer(text=x[one])

            admins_info = await db.select_admin(notify_id=one)
            shop_name = admins_info.get('shop_name')
            open_close = admins_info.get('open_close')
            pay_TOKEN = admins_info.get('TOKEN')

            if open_close == True:
                shipping_info = await db.select_shipping(orderer_id=user_id)
                if shipping_info != None:
                    shops = shipping_info.get('shops')
                    if shop_name not in shops:
                        await dp.bot.send_invoice(query.from_user.id,
                                                  title=shop_name,
                                                  description=x[one],
                                                  provider_token=pay_TOKEN,
                                                  currency='rub',
                                                  prices=[types.LabeledPrice(
                                                      label=shop_name, amount=int(amount[one])*100)],
                                                  payload=one+1,
                                                  start_parameter=12312431421231,
                                                  need_phone_number=True,
                                                  need_shipping_address=True)
                    else:
                        await dp.bot.send_message(user_id, f"{shop_name} - оплачено.", reply_markup=None)
                else:
                    await dp.bot.send_invoice(query.from_user.id,
                                              title=shop_name,
                                              description=x[one],
                                              provider_token=pay_TOKEN,
                                              currency='rub',
                                              prices=[types.LabeledPrice(
                                                  label=shop_name, amount=int(amount[one])*100)],
                                              payload=one+1,
                                              start_parameter=12312431421231,
                                              need_phone_number=True,
                                              need_shipping_address=True)
            else:
                await dp.bot.send_message(user_id, f"{shop_name} - магазин закрыт, сделайте заказ позже", reply_markup=None)
            # await query.message.edit_text("Готово. Заказ принят в обработку, ожидайте.", reply_markup=None)
            # -------------------------------
        y = []
        # await db.clear_card(id=user_id)


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await dp.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                           error_message="Aliens tried to steal your card's CVV,"
                                           " but we successfully protected your credentials,"
                                           " try to pay again in a few minutes, we need a small rest.")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    ivoice_payload = message.successful_payment.invoice_payload
    if ivoice_payload == str(SUPERADMIN_ID):
        admin_id = message.from_user.id
        admins_info = await db.select_admin(id=admin_id)
        shop_name = admins_info.get('shop_name')
        summ_cash = int(admins_info.get('summ_cash'))
        wow_cash = int(admins_info.get('wow_cash'))
        total_amount = int(message.successful_payment.total_amount)
        wow_cash -= (total_amount/100)
        if wow_cash < 0:
            wow_cash = 0

        await db.update_wow_cash(id=admin_id, wow_cash=wow_cash)
        text = """Оплата прошла успешно. Комиссия обнулена."""
        await dp.bot.send_message(admin_id, text, reply_markup=None)
    else:
        user_id = message.from_user.id
        shop_admin_id = int(message.successful_payment.invoice_payload)
        admins_info = await db.select_admin(notify_id=shop_admin_id)
        admin_id = admins_info.get('id')
        shop_name = admins_info.get('shop_name')
        summ_cash = int(admins_info.get('summ_cash'))
        wow_cash = int(admins_info.get('wow_cash'))

        user_info = await db.select_user(telegram_id=user_id)
        user_name = user_info.get("full_name")

        # добавление шиппинга к юзеру
        shipping_info = await db.select_shipping(orderer_id=user_id)

        if shipping_info == None:
            shipping_price = 100
            shipping_adress = f"{message.successful_payment.order_info.shipping_address.state}, {message.successful_payment.order_info.shipping_address.city}, {message.successful_payment.order_info.shipping_address.street_line1}, {message.successful_payment.order_info.shipping_address.street_line2}"
            orderer_phone_number = message.successful_payment.order_info.phone_number
            await db.add_shipping(orderer_id=user_id, shipper_id=None, shops={shop_name}, shipping_adress=shipping_adress, shipping_price=shipping_price, shipping_time=0, orderer_phone_number=orderer_phone_number)

        user_phone_number = message.successful_payment.order_info.phone_number
        shipping_info = await db.select_shipping(orderer_id=user_id)
        shipping_price = shipping_info.get('shipping_price')
        shops = shipping_info.get('shops')
        if shop_name not in shops:
            shops += {shop_name}
            shipping_price += 50
            await db.update_shipping_shops(orderer_id=user_id, shops=shops)
            await db.update_shipping_price(orderer_id=user_id, shipping_price=shipping_price)
        # -------------------------------

        # отправка чека магазину
        shop_items_in_card = await get_shop_items(user_id=message.from_user.id, admin_id=admin_id)
        summ_price = 0
        text = f"{shop_name}\n=====================\n"
        wow_cash2 = 0
        for item in shop_items_in_card:

            item_id = item.items_id
            item_quantity = item.quantity
            item_info = await db.select_item(id=int(item_id))
            item_name = item_info.get('name')
            item_price = item_info.get('price')

            summ_price += item_quantity * item_price
            wow_cash2 += 5*item_quantity

            text += f"""Заказ: №{item_id} {item_name}, 
Количество: {item.quantity} 
Цена: {item_price*item.quantity}₽   
=====================
"""
        else:
            text += f"""Общая стоимость заказа: {summ_price}₽
=====================            
Заказчик:{user_name} 
Номер телефона: {user_phone_number}
ID:{user_id}"""
            # добавление в базу данных сумму оплаты summ_cash and wow_cash
            summ_cash += summ_price
            wow_cash += wow_cash2
            if wow_cash >= 500:
                await dp.bot.send_message(admin_id, '100 заказов сделано через бота, оплатите комиссию', reply_markup=await cash_pay_keyboard(admin_id))
            await db.update_summ_cash(id=admin_id, summ_cash=summ_cash)
            await db.update_wow_cash(id=admin_id, wow_cash=wow_cash)
            await dp.bot.send_message(shop_admin_id, text, reply_markup=basket_keyboard3(user_id))

        # удаление товаров с корзины
        for item in shop_items_in_card:
            item_id = item.items_id
            await db.delete_item_in_card(id=user_id, items_id=item_id)
        # -------------------------------

        markup = await shipping_keyboard(user_id=admin_id)
        await dp.bot.send_message(user_id, f"{shop_name} - Готово. Оплата прошла. Ожидайте ответа магазина.", reply_markup=None)


@dp.callback_query_handler(basket2.filter(basket_edit="order_info"))
async def buy_all_card1(query: types.CallbackQuery, callback_data: dict):
    user_id = callback_data.get("user_id")
    admin_id = query.from_user.id
    shop_admin_info = await db.select_admin(id=admin_id)
    shop_name = shop_admin_info.get("shop_name")
    adress = shop_admin_info.get("adress")
    text = f"""{query.message.text}
=====================
Магазин:{shop_name}
Адрес: {adress}"""
    logging.info(user_id)
    await query.message.edit_text(text=text, reply_markup=basket_keyboard3(user_id))


@dp.callback_query_handler(basket2.filter(basket_edit=["5", "10", "15", "30", "60"]))
async def buy_all_card1(query: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data.get("user_id"))

    await query.answer()
    callback_data_time = callback_data["basket_edit"]

    order_time = 0

    if callback_data_time == "5":
        order_time = "5 минут"
        shipping_time = 10
    elif callback_data_time == "10":
        order_time = "10 минут"
        shipping_time = 15
    elif callback_data_time == "15":
        order_time = "15 минут"
        shipping_time = 20
    elif callback_data_time == "30":
        order_time = "30 минут"
        shipping_time = 35
    elif callback_data_time == "60":
        order_time = "1 часа"
        shipping_time = 65

    text = f"""{query.message.text} 
Заказ  будет готов в течении: {order_time} 
====================="""
    logging.info(user_id)
    text2 = f"""{text} 
=====================
Готово, чек отправлен заказчику.
====================="""

    shipping_info = await db.select_shipping(orderer_id=user_id)
    time_of_shipping = shipping_info.get('shipping_time')
    if time_of_shipping == 0:
        await db.update_shipping_time(orderer_id=user_id, shipping_time=shipping_time)
    elif time_of_shipping >= shipping_time:
        pass
    elif time_of_shipping < shipping_time:
        await db.update_shipping_time(orderer_id=user_id, shipping_time=shipping_time)

    markup1 = await order_ready(user_id)
    # сюда добавить кнопку готовности заказа
    await query.message.edit_text(text=text2, reply_markup=markup1)
    # сюда кнопку оформить доставку
    markup2 = await shipping_keyboard2(user_id)
    await dp.bot.send_message(user_id, text, parse_mode="markdown", reply_markup=markup2)


@dp.callback_query_handler(shipping.filter(shippings="order_ready"))
async def order_ready1(query: types.CallbackQuery, callback_data: dict):
    await query.message.edit_reply_markup(reply_markup=None)
    text = f"""Заказ  готов.
=====================
{query.message.text} 
"""
    text2 = """
=====================
Готово, чек отправлен заказчику.
====================="""
    text = text.replace(text2, '')
    user_id = int(callback_data.get("shipping_price"))
    shipper_text = text + \
        'Жмите кнопку "Принять" только после того как все точки отпишутся о готовности товара.'

    shipping_info = await db.select_shipping(orderer_id=user_id)
    if shipping_info != None:
        shipper_id = shipping_info.get("shipper_id")
        if shipper_id != None:
            await dp.bot.send_message(shipper_id, shipper_text, parse_mode="markdown", reply_markup=await shipping_delete(user_id))
        else:
            shipping_admin_info = await db.select_admin(shop_code="Shipping")
            shipping_admin_id = shipping_admin_info.get("notify_if")
            # сюда notify_id доставки
            await dp.bot.send_message(-591361255, shipper_text, parse_mode="markdown", reply_markup=await shipping_delete(user_id))
        await dp.bot.send_message(user_id, text, parse_mode="markdown", reply_markup=None)
    elif shipping_info == None:
        await dp.bot.send_message(user_id, text, parse_mode="markdown", reply_markup=None)


@dp.callback_query_handler(shipping.filter(shippings="shipping_edit"))
async def shipping_edit(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id

    shipping_info = await db.select_shipping(orderer_id=user_id)
    shops = shipping_info.get('shops')
    shipping_price = shipping_info.get('shipping_price')
    shipping_time = shipping_info.get('shipping_time')
    text = f"""Точки:{shops} 
Стоимость доставки:{shipping_price}₽
Время доставки: {shipping_time} минут
=====================
После оплаты товаров, магазин автоматически добавляется в список точек.
Если вам нужна доставка, нажмите "заказать".
Для отмены, нажмите "отмена".
=====================
Оплата доставки осуществялется при получении заказа. """
    markup = await shipping_edit_keyboard(user_id)
    await dp.bot.send_message(user_id, text, parse_mode="markdown", reply_markup=markup)


@dp.callback_query_handler(shipping.filter(shippings="shipping_ordering"))
async def shipping_edit(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id

    user_info = await db.select_user(telegram_id=user_id)
    user_name = user_info.get('full_name')

    shipping_info = await db.select_shipping(orderer_id=user_id)
    shops = shipping_info.get('shops')
    shipping_price = shipping_info.get('shipping_price')
    shipping_time = shipping_info.get('shipping_time')
    shipping_adress = shipping_info.get('shipping_adress')
    orderer_phone_number = shipping_info.get('orderer_phone_number')
    text = f"""Заказ
=====================
Точки:{shops} 
Стоимость доставки:{shipping_price}₽
Время доставки: {shipping_time} минут
=====================
Заказчик: {user_name}
Номер телефона: {orderer_phone_number}
Адрес: {shipping_adress}
ID: {user_id}"""

    await dp.bot.send_message(-591361255, text, parse_mode="markdown", reply_markup=await shipping_edit_keyboard2(user_id))
    await query.message.edit_text(text="Заказ отправлен в службу доставки ожидайте.", reply_markup=None)


@dp.callback_query_handler(shipping.filter(shippings="shipper_accept"))
async def shipping_edit(query: types.CallbackQuery, callback_data: dict):
    shipper_id = query.from_user.id
    orderer_id = int(callback_data.get('shipping_price'))

    shipper_info = await db.select_user(telegram_id=shipper_id)
    shipper_name = shipper_info.get('full_name')
    shipper_phone_number = shipper_info.get('phone_number')
    await db.update_shipping_shipper(orderer_id=orderer_id, shipper_id=shipper_id)
    text = f"""{query.message.text} 
=====================
Заказ принят
Перевозчик: {shipper_name}
Номер телефона: {shipper_phone_number}
ID: {shipper_id}
=====================
"""
    await dp.bot.send_message(shipper_id, text, reply_markup=None)
    await dp.bot.send_message(orderer_id, text, reply_markup=None)
    await query.message.edit_text(text="Заказ принят.", reply_markup=None)


@dp.callback_query_handler(shipping.filter(shippings="without_shipping"))
async def shipping_edit(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    text = f"""Доставка отменена"""

    await db.delete_shipping(orderer_id=user_id)
    await dp.bot.send_message(user_id, text, parse_mode="markdown", reply_markup=None)


@dp.callback_query_handler(shipping.filter(shippings="shipper_delete"))
async def shipping_edit(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    orderer_id = callback_data.get("shipping_price")
    text = f"""Доставка в пути"""
    await db.delete_shipping(orderer_id=int(orderer_id))
    await query.message.edit_reply_markup(None)
    await dp.bot.send_message(user_id, text, parse_mode="markdown", reply_markup=None)
    await dp.bot.send_message(orderer_id, text, parse_mode="markdown", reply_markup=None)


@dp.callback_query_handler(shipping.filter(shippings="go_to_basket"))
async def shipping_edit(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    orderer_id = callback_data.get("shipping_price")
    text = f"""Для того чтобы добавить точку доставки, оплатите выбранный товар в корзине"""
    await dp.bot.send_message(user_id, text, parse_mode="markdown", reply_markup=await show_basket_keyboard())
