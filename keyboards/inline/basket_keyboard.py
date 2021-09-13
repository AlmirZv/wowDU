from loader import db
from aiogram.types import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from keyboards.inline.menu_keyboards import buy_item_cd, card_cd

basket1 = CallbackData("basket", "basket_edit", "item_id")
basket2 = CallbackData("basket", "basket_edit", "user_id")
shipping = CallbackData("shipping", "shippings", "shipping_price")


def shipping_cd(shippings, shipping_price):
    return shipping.new(shippings=shippings, shipping_price=shipping_price)


def basket_cd(basket_edit, item_id):
    return basket1.new(basket_edit=basket_edit, item_id=item_id)


def basket2_cd(basket_edit, user_id):
    return basket2.new(basket_edit=basket_edit, user_id=user_id)


buy_all_card = CallbackData("buy", "all_card", "item_id")


def buy_all_cd(all_card, item_id):
    return buy_all_card.new(all_card=all_card, item_id=item_id)


def basket_keyboard(item_id, quantity_count):

    markup = InlineKeyboardMarkup()
    # markup.row(InlineKeyboardButton(text="Добавить в корзину", callback_data=))
    markup.row(
        InlineKeyboardButton(
            text="Изменить количество", callback_data=buy_item_cd(item_id=item_id, quantity="change", quantity_count=quantity_count+1)),
        InlineKeyboardButton("Удалить", callback_data=basket_cd(
            basket_edit="delete_item", item_id=item_id))
    )
    return markup


def basket_keyboard2(user_id, shipping_price):

    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text="Перейти к оплате", callback_data=basket_cd(
                basket_edit="buy_all_card", item_id=user_id))
    )
    markup.row(
        InlineKeyboardButton("Очистить корзину", callback_data=basket_cd(
            basket_edit="clear_card", item_id=user_id))
    )
    return markup


def basket_keyboard02(user_id, shipping_price):

    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text="Перейти к оплате", callback_data=basket_cd(
                basket_edit="buy_all_card", item_id=user_id))
    )
    markup.row(
        InlineKeyboardButton("Очистить корзину", callback_data=basket_cd(
            basket_edit="clear_card", item_id=user_id))
    )
    return markup


def save_quantity(category, subcategory, item_id, quantity_count):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("+ 1", callback_data=buy_item_cd(
            item_id=item_id, quantity="change+1", quantity_count=quantity_count)),
        InlineKeyboardButton("- 1", callback_data=buy_item_cd(item_id=item_id, quantity="change-1", quantity_count=quantity_count)))

    markup.row(
        InlineKeyboardButton("Сохранить", callback_data=card_cd(
            show_card="save_card", item_id=item_id, quantity_count=quantity_count))
    )

    return markup


def admins_notify(user_id):

    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text="Принять заказ", callback_data=basket2_cd(
                basket_edit="order_info", user_id=user_id))
    )
    return markup


def basket_keyboard3(user_id):

    markup = InlineKeyboardMarkup(row_width=2)
    # markup.row(InlineKeyboardButton(text="Добавить в корзину", callback_data=))
    markup.row(
        InlineKeyboardButton(
            text="5", callback_data=basket2_cd(
                basket_edit="5", user_id=user_id)),
        InlineKeyboardButton("10", callback_data=basket2_cd(
            basket_edit="10", user_id=user_id))

    )
    markup.row(
        InlineKeyboardButton("15", callback_data=basket2_cd(
            basket_edit="15", user_id=user_id)),
        InlineKeyboardButton("30", callback_data=basket2_cd(
            basket_edit="30", user_id=user_id))
    )
    markup.row(
        InlineKeyboardButton("60", callback_data=basket2_cd(
            basket_edit="60", user_id=user_id))
    )
    return markup


async def shipping_keyboard(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text="Добавить доставку", callback_data=shipping_cd(
                shippings="shipping_info", shipping_price=user_id))
    )
    markup.row(
        InlineKeyboardButton(
            text="Без доставки", callback_data=shipping_cd(
                shippings="without_shipping", shipping_price=user_id))
    )
    return markup


async def shipping_keyboard2(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text="Оформить доставку", callback_data=shipping_cd(
                shippings="shipping_edit", shipping_price=user_id))
    )
    markup.row(
        InlineKeyboardButton(
            text="Без доставки", callback_data=shipping_cd(
                shippings="without_shipping", shipping_price=user_id))
    )
    return markup


async def order_ready(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text="Заказ готов", callback_data=shipping_cd(
                shippings="order_ready", shipping_price=user_id))
    )
    return markup


async def shipping_keyboard3(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    shipping_info = await db.select_shipping(orderer_id=user_id)
    shops = shipping_info.get('shops')
    for one in shops:
        button_text = f"{one}"
        callback_data = shipping_cd(
            shippings=one, shipping_price=user_id)
        markup.insert(InlineKeyboardButton(
            text=button_text, callback_data=callback_data))
    return markup


async def shipping_edit_keyboard(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text="Заказать", callback_data=shipping_cd(
                shippings="shipping_ordering", shipping_price=user_id))
    )
    markup.row(
        InlineKeyboardButton(
            text="Добавить точку доставки", callback_data=shipping_cd(
                shippings="go_to_basket", shipping_price=user_id))
    )
    markup.row(
        InlineKeyboardButton(
            text="Отмена", callback_data=shipping_cd(
                shippings="cancel_shipping", shipping_price=user_id))
    )
    return markup


async def shipping_edit_keyboard2(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text="Принять заказ", callback_data=shipping_cd(
                shippings="shipper_accept", shipping_price=user_id))
    )

    return markup


async def shipping_delete(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text="Принять", callback_data=shipping_cd(
                shippings="shipper_delete", shipping_price=user_id))
    )

    return markup
