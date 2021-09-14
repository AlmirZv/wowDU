from sqlalchemy import sql, Column, Sequence, Integer
import requests

from utils.db_api.database import db_gino

import emoji


class Item(db_gino.Model):
    __tablename__ = "items"
    query: sql.Select

    telegram_id = Column(db_gino.Integer)
    id = Column(db_gino.Integer, Sequence("user_id_seq"), primary_key=True)
    category_code = Column(db_gino.String(20))
    category_name = Column(db_gino.String(50))

    subcategory_code = Column(db_gino.String(20))
    subcategory_name = Column(db_gino.String(50))

    name = Column(db_gino.String(50))
    photo = Column(db_gino.String(250))
    description = Column(db_gino.String(250))
    price = Column(Integer)

    def __repr__(self):
        return f"""
Товар №{self.id} - {self.name}
Описание:{self.description}
Цена: {self.price} ₽
[{emoji.emojize(":thumbs_up:")}]({self.photo})
        """


class Adminss(db_gino.Model):
    __tablename__ = "admins"
    query: sql.Select

    id = Column(db_gino.Integer,  Sequence("user_id_seq"), primary_key=True)
    shop_name = Column(db_gino.String)
    shop_code = Column(db_gino.String)
    notify_id = Column(db_gino.Integer)
    adress = Column(db_gino.String)
    open_close = Column(db_gino.Boolean)
    TOKEN = Column(db_gino.String(255))
    summ_cash = Column(db_gino.String(255))
    wow_cash = Column(db_gino.String(255))


class Basket(db_gino.Model):
    __tablename__ = "basket"
    query: sql.Select

    id = Column(db_gino.BigInteger())
    items_id = Column(db_gino.Integer)
    quantity = Column(db_gino.Integer)
    admin_id = Column(db_gino.Integer)
