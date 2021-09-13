from typing import List
from utils.db_api.models import Item, Adminss, Basket
from utils.db_api.database import db_gino
from sqlalchemy import and_

# BASKET table


async def get_items_id(user_id) -> List[Basket]:
    return await Basket.query.where(Basket.id == user_id).gino.all()


async def get_shop_items(user_id, admin_id) -> List[Basket]:
    return await Basket.query.where(and_(Basket.id == user_id, Basket.admin_id == admin_id)).gino.all()


async def add_item_to_basket(**kwargs):
    newitem = await Basket(**kwargs).create()
    return newitem


# ITEM table
async def add_item(**kwargs):
    newitem = await Item(**kwargs).create()
    return newitem


async def get_categories() -> List[Item]:
    return await Item.query.distinct(Item.category_code).gino.all()


async def get_subcategories(category) -> List[Item]:
    return await Item.query.distinct(Item.subcategory_code).where(Item.category_code == category).gino.all()


async def count_items(category_code, subcategory_code=None):
    conditions = [Item.category_code == category_code]

    if subcategory_code:
        conditions.append(Item.subcategory_code == subcategory_code)

    total = await db_gino.select([db_gino.func.count()]).where(
        and_(*conditions)
    ).gino.scalar()
    return total


async def get_items(category_code, subcategory_code) -> List[Item]:
    items = await Item.query.where(
        and_(Item.category_code == category_code,
             Item.subcategory_code == subcategory_code)
    ).gino.all()
    return items


async def get_item(item_id) -> Item:
    item = await Item.query.where(Item.id == item_id).gino.first()
    return item

# ADMINSS table


async def add_admin(**kwargs):
    newadmin = await Adminss(**kwargs).create()
    return newadmin


async def get_admin_id(admin_id) -> List[Adminss]:
    admin_id = await Adminss.query.where(Adminss.id == admin_id).gino.first()
    return admin_id
