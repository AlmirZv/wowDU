import sys
sys.path.append("d:/Python/wow Du/utils/")
from utils.db_api.db_commands  import add_item
from utils.db_api.database import create_db
import asyncio

"""async def add_items():
    await add_item(name="Гавайская пицца",
                    category_name="Название магазина пиццы", category_code="PizzaTime",
                    subcategory_name="Пиццы", subcategory_code="Pizza",
                    price=100, photo="https://img.fresh.ru/unsafe/560x/https%3A%2F%2Fimg.fresh.ru%2Ffresh-20190603%2Fc872727ea823b4a53750676fe8ee327b98b58cfd.png")
    await add_item(name="Пепперони",
                    category_name="Название магазина пиццы", category_code="PizzaTime",
                    subcategory_name="Пиццы", subcategory_code="Pizza",
                    price=100, photo="-")
    await add_item(name="Сырная пицца",
                    category_name="Название магазина пиццы", category_code="PizzaTime",
                    subcategory_name="Пиццы", subcategory_code="Pizza",
                    price=100, photo="-")
    await add_item(name="Четыре сезона",
                    category_name="Название магазина пиццы", category_code="PizzaTime",
                    subcategory_name="Пиццы", subcategory_code="Pizza",
                    price=100, photo="-")
    await add_item(name="Coca Cola",
                    category_name="Название магазина пиццы", category_code="PizzaTime",
                    subcategory_name="Напитки", subcategory_code="Drink",
                    price=100, photo="-")
    await add_item(name="Pepsi",
                    category_name="Название магазина пиццы", category_code="PizzaTime",
                    subcategory_name="Напитки", subcategory_code="Drink",
                    price=100, photo="-")
    await add_item(name="Сет Своя компания",
                    category_name="СушиВесла", category_code="SushiVesla",
                    subcategory_name="суши", subcategory_code="sushi",
                    price=100, photo="-")
    await add_item(name="Суе Кинг",
                    category_name="СушиВесла", category_code="SushiVesla",
                    subcategory_name="суши", subcategory_code="sushi",
                    price=100, photo="-")
    await add_item(name="Сет Фудзияма",
                    category_name="СушиВесла", category_code="SushiVesla",
                    subcategory_name="суши", subcategory_code="sushi",
                    price=100, photo="-")
    await add_item(name="Сет Оригами",
                    category_name="СушиВесла", category_code="SushiVesla",
                    subcategory_name="суши", subcategory_code="sushi",
                    price=100, photo="-")
    await add_item(name="Pepsi",
                    category_name="СушиВесла", category_code="SushiVesla",
                    subcategory_name="Напитки", subcategory_code="Drink",
                    price=100, photo="-")
    await add_item(name="Sprite",
                    category_name="СушиВесла", category_code="SushiVesla",
                    subcategory_name="Напитки", subcategory_code="Drink",
                    price=100, photo="-")

loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
loop.run_until_complete(add_items())"""