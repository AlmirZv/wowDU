from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin_add_item(StatesGroup):
    s_subcategory_name=State()
    s_subcategory_code=State()
    s_name_item=State()
    s_price=State()
    s_photo=State()



