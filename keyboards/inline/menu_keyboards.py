from aiogram.types import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

from utils.db_api.db_commands import get_categories, count_items, get_subcategories, get_items

menu_cd = CallbackData("show_menu", "level", "category",
                       "subcategory", "item_id")
buy_item = CallbackData("buy", "item_id", "quantity", "quantity_count")
card = CallbackData("show", "show_card", "item_id", "quantity_count")
basket = CallbackData("show", "show_basket")


def basket_cd(show_basket):
    return basket.new(show_basket=show_basket)


def card_cd(show_card, item_id, quantity_count):
    return card.new(show_card=show_card, item_id=item_id, quantity_count=quantity_count)


def buy_item_cd(item_id, quantity, quantity_count):
    return buy_item.new(item_id=item_id, quantity=quantity, quantity_count=quantity_count)


def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(level=level, category=category, subcategory=subcategory, item_id=item_id)


async def categories_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)

    categories = await get_categories()
    for category in categories:
        button_text = f"{category.category_name}"
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1, category=category.category_code)

        shop_info = await db.select_admin(shop_name=category.category_name)
        open_close = shop_info.get('open_close')
        if open_close == True:
            markup.insert(InlineKeyboardButton(
                text=button_text, callback_data=callback_data))
        else:
            pass
    markup.row(
        InlineKeyboardButton(
            "Корзина", callback_data=basket_cd(show_basket="my_basket"))
    )
    return markup


async def show_basket_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            "Корзина", callback_data=basket_cd(show_basket="my_basket"))
    )
    return markup


async def subcategories_keyboard(category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)

    subcategories = await get_subcategories(category)
    for subcategory in subcategories:
        number_of_items = await count_items(category_code=category, subcategory_code=subcategory.subcategory_code)
        # button_text = f"{subcategory.subcategory_name} ({number_of_items} шт)"
        button_text = f"{subcategory.subcategory_name}"
        callback_data = make_callback_data(
            level=CURRENT_LEVEL+1, category=category, subcategory=subcategory.subcategory_code)
        markup.insert(InlineKeyboardButton(
            text=button_text, callback_data=callback_data))

    markup.row(
        InlineKeyboardButton(
            text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL-1)
        )
    )
    return markup


async def items_keyboard(category, subcategory):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)

    items = await get_items(category, subcategory)
    for item in items:
        button_text = f"{item.name} - {item.price}₽"
        callback_data = make_callback_data(
            level=CURRENT_LEVEL+1, category=category, subcategory=subcategory, item_id=item.id)
        markup.insert(InlineKeyboardButton(
            text=button_text, callback_data=callback_data))

    markup.row(
        InlineKeyboardButton(
            text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL-1, category=category)
        )
    )
    return markup


def item_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL = 3
    quantity_count = 0
    markup = InlineKeyboardMarkup()
    # markup.row(InlineKeyboardButton(text="Добавить в корзину", callback_data=))
    markup.row(
        InlineKeyboardButton(text="Выбрать количество", callback_data=buy_item_cd(
            item_id=item_id, quantity="+1", quantity_count=0))
    )

    markup.row(
        InlineKeyboardButton(
            text="Назад", callback_data=make_callback_data(level=CURRENT_LEVEL-1, category=category, subcategory=subcategory)
        )
    )

    return markup


def add_to_card(category, subcategory, item_id, quantity_count):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("+ 1", callback_data=buy_item_cd(
            item_id=item_id, quantity="+1", quantity_count=quantity_count)),
        InlineKeyboardButton("- 1", callback_data=buy_item_cd(item_id=item_id, quantity="-1", quantity_count=quantity_count)))

    markup.row(
        InlineKeyboardButton("Добавить в корзину", callback_data=card_cd(
            show_card="show_card", item_id=item_id, quantity_count=quantity_count))
    )
    markup.row(
        InlineKeyboardButton(
            text="Отмена", callback_data=make_callback_data(level=CURRENT_LEVEL-1, category=category, subcategory=subcategory)
        ))
    return markup


def item_add_done_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    # markup.row(InlineKeyboardButton(text="Добавить в корзину", callback_data=))
    markup.row(
        InlineKeyboardButton(
            text="Назад к товарам", callback_data=make_callback_data(level=CURRENT_LEVEL-1, category=category, subcategory=subcategory)
        )
    )
    markup.row(
        InlineKeyboardButton(
            "Корзина", callback_data=basket_cd(show_basket="my_basket"))
    )
    return markup
