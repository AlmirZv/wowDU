from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result


# Таблица юзеров
# ____________________________________________________________________________________-

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE, 
        phone_number BIGINT NULL,
        user_adress varchar(255) NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id, phone_number, user_adress):
        sql = "INSERT INTO users (full_name, username, telegram_id, phone_number, user_adress) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, username, telegram_id, phone_number, user_adress, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_full_name(self, full_name, telegram_id):
        sql = "UPDATE Users SET full_name=$1 WHERE telegram_id=$2"
        return await self.execute(sql, full_name, telegram_id, execute=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_user_phone_number(self, phone_number, telegram_id):
        sql = "UPDATE Users SET phone_number=$1 WHERE telegram_id=$2"
        return await self.execute(sql, phone_number, telegram_id, execute=True)

    async def update_user_user_adress(self, user_adress, telegram_id):
        sql = "UPDATE Users SET user_adress=$1 WHERE telegram_id=$2"
        return await self.execute(sql, user_adress, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

# ________________________________________________________________________________________________________________________________
# admins table

    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Admins (
        id BIGINT PRIMARY KEY NOT NULL UNIQUE,
        shop_name varchar(255) NULL,
        shop_code varchar(255) NULL,
        notify_id BIGINT NULL,
        adress varchar(255) NULL,
        open_close BOOLEAN NOT NULL,
        TOKEN carchar(255) NOT NULL,
        summ_cash BIGINT NULL,
        wow_cash BIGINT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_admin(self, id, shop_name, shop_code, notify_id, adress, open_close, TOKEN, summ_cash, wow_cash):
        sql = "INSERT INTO admins (id, shop_name, shop_code, notify_id, adress, open_close, TOKEN) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) returning *"
        return await self.execute(sql, id, shop_name, shop_code, notify_id, adress, open_close, TOKEN, fetchrow=True)

    async def select_all_admins(self):
        sql = "SELECT * FROM Admins"
        return await self.execute(sql, fetch=True)

    async def select_admin(self, **kwargs):
        sql = "SELECT * FROM Admins WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_admins(self):
        sql = "SELECT COUNT(*) FROM Admins"
        return await self.execute(sql, fetchval=True)

    async def update_open_close(self, id, open_close):
        sql = "UPDATE Admins SET open_close=$2 WHERE id=$1"
        return await self.execute(sql, id, open_close, execute=True)

    async def update_admin_shop_name(self, shop_name, shop_code):
        sql = "UPDATE Admins SET shop_name=$1 WHERE shop_code=$2"
        return await self.execute(sql, shop_name, shop_code, execute=True)

    async def delete_admins(self):
        await self.execute("DELETE FROM Admins WHERE TRUE", execute=True)

    async def drop_admins(self):
        await self.execute("DROP TABLE Admins", execute=True)

    async def update_summ_cash(self, id, summ_cash):
        sql = "UPDATE Admins SET summ_cash=$2 WHERE id=$1"
        return await self.execute(sql, id, summ_cash, execute=True)

    async def update_wow_cash(self, id, wow_cash):
        sql = "UPDATE Admins SET wow_cash=$2 WHERE id=$1"
        return await self.execute(sql, id, wow_cash, execute=True)

# ________________________________________________________________________________________________________________________________
# table category

    async def create_table_categories(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Categories (
        id BIGINT PRIMARY KEY NOT NULL UNIQUE,
        shop_name varchar(255) NULL,
        shop_code varchar(255) NULL,
        category_name(255) NULL,
        category_code(255) NULL 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_category(self, id, shop_name, shop_code, category_code, category_name):
        sql = "INSERT INTO categories (id, shop_name, shop_code, category_code, category_name) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, id, shop_name, shop_code, category_code, category_name, fetchrow=True)

    async def select_category(self, **kwargs):
        sql = "SELECT * FROM Categories WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_admin_category_name(self, category_name, shop_code):
        sql = "UPDATE Categories SET category_name=$1 WHERE shop_code=$2"
        return await self.execute(sql, category_name, shop_code, execute=True)

    async def delete_category(self):
        await self.execute("DELETE FROM Categories WHERE TRUE", execute=True)

    async def drop_categories(self):
        await self.execute("DROP TABLE Categories", execute=True)

# ________________________________________________________________________________________________________________________________
# table items
    async def select_item(self, **kwargs):
        sql = "SELECT * FROM items WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)


# __________________________________
# table bascket

    async def create_table_basket(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Basket (
        id BIGINT NOT NULL,
        items_id integer NULL,
        quantity integer NULL, 
        admin_id integer NULL
        );
        """
        await self.execute(sql, execute=True)

    async def delete_item_in_card(self, id, items_id, **kwargs):
        sql = "DELETE FROM Basket WHERE id = $1 AND items_id=$2"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, id, items_id, *parameters, fetchrow=True)

    async def clear_card(self, id, **kwargs):
        sql = "DELETE FROM Basket WHERE id = $1 "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, id, *parameters, fetchrow=True)

    async def add_items_to_basket(self, id, items_id, quantity, admin_id):
        sql = "INSERT INTO Basket (id, items_id, quantity, admin_id) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, id, items_id, quantity, admin_id, fetchrow=True)

    async def add_new_items_to_basket(self, items_id, id):
        sql = "INSERT INTO Basket items_id=$1 WHERE id=$2"
        return await self.execute(sql, items_id, id, execute=True)

    async def select_item_in_card(self, id, **kwargs):
        sql = "SELECT items_id FROM Basket WHERE  id = $1"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, id, *parameters, fetch=True)

    async def select_item_id_in_card(self, id, items_id, **kwargs):
        sql = "SELECT * FROM Basket WHERE id=$1 AND items_id = $2"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, id, items_id, *parameters, fetchrow=True)

    async def select_shop_items_in_card(self, id, admin_id, **kwargs):
        sql = "SELECT * FROM Basket WHERE id=$1 AND admin_id = $2"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, id, admin_id, *parameters, fetchrow=True)

    async def update_item_quantity(self, id, items_id, quantity):
        sql = "UPDATE Basket SET quantity=$3 WHERE items_id=$2 AND id=$1"
        return await self.execute(sql, id, items_id, quantity, execute=True)


# table shipping

    async def create_table_shipping(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Shipping (
            orderer_id BIGINT NOT NULL,
            shipper_id BIGINT NULL,
            shops varchar(255) ARRAY NULL, 
            shipping_adress varchar(255) NULL, 
            shipping_price integer NULL,
            shipping_time integer NULL,
            orderer_phone_number varchar(255) NULL
            );
            """
        await self.execute(sql, execute=True)

    async def add_shipping(self, orderer_id, shipper_id, shops, shipping_adress, shipping_price, shipping_time, orderer_phone_number):
        sql = "INSERT INTO Shipping (orderer_id, shipper_id, shops, shipping_adress, shipping_price, shipping_time, orderer_phone_number) VALUES($1, $2, $3, $4, $5, $6, $7) returning *"
        return await self.execute(sql, orderer_id, shipper_id, shops, shipping_adress, shipping_price, shipping_time, orderer_phone_number, fetchrow=True)

    async def select_shipping(self, **kwargs):
        sql = "SELECT * FROM Shipping WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_shipping_time(self, orderer_id, shipping_time):
        sql = "UPDATE Shipping SET shipping_time=$2 WHERE orderer_id=$1"
        return await self.execute(sql, orderer_id, shipping_time, execute=True)

    async def update_shipping_price(self, orderer_id, shipping_price):
        sql = "UPDATE Shipping SET shipping_price=$2 WHERE orderer_id=$1"
        return await self.execute(sql, orderer_id, shipping_price, execute=True)

    async def update_shipping_shops(self, orderer_id, shops):
        sql = "UPDATE Shipping SET shops=$2 WHERE orderer_id=$1"
        return await self.execute(sql, orderer_id, shops, execute=True)

    async def update_shipping_shops_to_null(self, orderer_id):
        sql = "UPDATE Shipping SET shops= null WHERE orderer_id=$1"
        return await self.execute(sql, orderer_id, execute=True)

    async def update_shipping_shipper(self, orderer_id, shipper_id):
        sql = "UPDATE Shipping SET shipper_id=$2 WHERE orderer_id=$1"
        return await self.execute(sql, orderer_id, shipper_id, execute=True)

    async def delete_shipping(self, orderer_id, **kwargs):
        sql = "DELETE FROM Shipping WHERE orderer_id = $1"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, orderer_id, *parameters, fetchrow=True)

# table white groups list

    async def create_table_whitelist(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Whitelist (
            chat_id BIGINT PRIMARY KEY NOT NULL,
            chat_name varchar(255) NOT NULL
            );
            """
        await self.execute(sql, execute=True)

    async def add_group_to_whitelist(self, chat_id, chat_name):
        sql = "INSERT INTO Whitelist (chat_id, chat_name) VALUES($1, $2) returning *"
        return await self.execute(sql, chat_id, chat_name, fetchrow=True)

    async def select_whitelist(self, **kwargs):
        sql = "SELECT * FROM Whitelist WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
