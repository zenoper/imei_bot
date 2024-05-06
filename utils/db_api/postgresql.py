from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
import pandas as pd

from data import config
from datetime import datetime, timedelta


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

    async def create_table_vba(self):
        sql = """
        CREATE TABLE IF NOT EXISTS VBA (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        employee_id VARCHAR(255) NOT NULL UNIQUE,
        shop_name VARCHAR(255) NOT NULL,
        phone_number VARCHAR(255) NOT NULL UNIQUE,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_vba(self, full_name, employee_id, shop_name, phone_number, telegram_id):
        sql = "INSERT INTO VBA(full_name, employee_id, shop_name, phone_number, telegram_id) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, full_name, employee_id, shop_name, phone_number, telegram_id, fetchrow=True)

    async def select_all_vbas(self):
        sql = "SELECT * FROM VBA"
        return await self.execute(sql, fetch=True)

    async def select_vba(self, **kwargs):
        sql = "SELECT * FROM VBA WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_vbas(self):
        sql = "SELECT COUNT(*) FROM VBA"
        return await self.execute(sql, fetchval=True)

    async def update_vba_username(self, username, telegram_id):
        sql = "UPDATE VBA SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_vba(self):
        await self.execute("DELETE FROM VBA WHERE TRUE", execute=True)

    async def drop_vbas(self):
        await self.execute("DROP TABLE VBA", execute=True)

# TABLE IMEI

    async def create_table_imei(self):
        sql = """
        CREATE TABLE IF NOT EXISTS IMEI (
        id SERIAL PRIMARY KEY,
        IMEI VARCHAR(255) NOT NULL UNIQUE,
        Model VARCHAR(255) NOT NULL,
        Sticker VARCHAR(255) NOT NULL,
        Date_month VARCHAR(255) NOT NULL,
        Time_day VARCHAR(255) NOT NULL,
        Telegram_id BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_imei(self, IMEI, Model, Sticker, Date_month, Time_day, Telegram_id):
        sql = "INSERT INTO IMEI(IMEI, Model, Sticker, Date_month, Time_day, Telegram_id) VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, IMEI, Model, Sticker, Date_month, Time_day, Telegram_id, fetchrow=True)

    async def select_all_imei(self):
        sql = "SELECT * FROM IMEI"
        return await self.execute(sql, fetch=True)

    async def select_imei(self, **kwargs):
        sql = "SELECT * FROM IMEI WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_imei(self):
        sql = "SELECT COUNT(*) FROM IMEI"
        return await self.execute(sql, fetchval=True)

    async def delete_imei(self):
        await self.execute("DELETE FROM IMEI WHERE TRUE", execute=True)

    async def drop_imei(self):
        await self.execute("DROP TABLE IMEI", execute=True)

    async def join_tables_and_export(self):

        yesterday = datetime.now() - timedelta(days=1)
        yesterday_date = yesterday.strftime('%Y-%m-%d')
        join_query = f"""
                SELECT VBA.full_name, VBA.shop_name, IMEI.Model, IMEI.Date_month, IMEI.Time_day 
                FROM VBA
                JOIN IMEI ON VBA.telegram_id = IMEI.Telegram_id 
                WHERE IMEI.Date_month = '{yesterday_date}';
                """
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(join_query)
                if result:
                    column_names = ['full_name', 'shop_name', 'model', 'date_month', 'time_day']
                    df = pd.DataFrame([dict(rec) for rec in result], columns=column_names)

                    return df
                else:
                    print("No data found for the specified date.")
                    return None

# TABLE STOCK

    async def create_table_stock_count(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Stock (
            telegram_id BIGINT NOT NULL UNIQUE,
            shop_name VARCHAR(255) NOT NULL,
            V30 INTEGER NOT NULL DEFAULT 0,
            V29 INTEGER NOT NULL DEFAULT 0,
            V29e INTEGER NOT NULL DEFAULT 0,
            V27 INTEGER NOT NULL DEFAULT 0,
            V27e INTEGER NOT NULL DEFAULT 0,
            V25 INTEGER NOT NULL DEFAULT 0,
            V25pro INTEGER NOT NULL DEFAULT 0,
            V25e INTEGER NOT NULL DEFAULT 0,
            V23 INTEGER NOT NULL DEFAULT 0,
            V23e INTEGER NOT NULL DEFAULT 0,
            V21 INTEGER NOT NULL DEFAULT 0,
            V21e INTEGER NOT NULL DEFAULT 0,
            Y100 INTEGER NOT NULL DEFAULT 0,
            Y53S_6GB INTEGER NOT NULL DEFAULT 0,
            Y53S_8GB INTEGER NOT NULL DEFAULT 0,
            Y36 INTEGER NOT NULL DEFAULT 0,
            Y35 INTEGER NOT NULL DEFAULT 0,
            Y33S_128GB INTEGER NOT NULL DEFAULT 0,
            Y33S_64GB INTEGER NOT NULL DEFAULT 0,
            Y31 INTEGER NOT NULL DEFAULT 0,
            Y27 INTEGER NOT NULL DEFAULT 0,
            Y27s INTEGER NOT NULL DEFAULT 0,
            Y22 INTEGER NOT NULL DEFAULT 0,
            Y21 INTEGER NOT NULL DEFAULT 0,
            Y17s_4_128 INTEGER NOT NULL DEFAULT 0,
            Y17s_6_128 INTEGER NOT NULL DEFAULT 0,
            Y16 INTEGER NOT NULL DEFAULT 0,
            Y15S INTEGER NOT NULL DEFAULT 0,
            Y12S INTEGER NOT NULL DEFAULT 0,
            Y03_64GB INTEGER NOT NULL DEFAULT 0,
            Y03_128GB INTEGER NOT NULL DEFAULT 0,
            Y02T INTEGER NOT NULL DEFAULT 0,
            Y1S INTEGER NOT NULL DEFAULT 0,
            X100 INTEGER NOT NULL DEFAULT 0
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_stock_vba(self, telegram_id, shop_name):
        sql = "INSERT INTO Stock(telegram_id, shop_name) VALUES($1, $2);"
        return await self.execute(sql, telegram_id, shop_name, fetchrow=True)

    async def select_all_stock(self):
        sql = "SELECT * FROM Stock"
        return await self.execute(sql, fetch=True)

    async def select_stock(self, **kwargs):
        sql = "SELECT * FROM Stock WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_stock_count(self, model_name, count, telegram_id):
        # Safely build the SQL command to prevent SQL injection
        # You cannot use parameterized queries directly for column names.
        model_name = model_name.replace(" ", "_").replace("/", "_")
        # You must validate or whitelist the column names to ensure security.
        allowed_columns = [
            'V30', 'V29', 'V29e', 'V27', 'V27e', 'V25', 'V25pro', 'V25e',
            'V23', 'V23e', 'V21', 'V21e', 'Y100', 'Y53S_6GB', 'Y53S_8GB', 'Y36',
            'Y35', 'Y33S_128GB', 'Y33S_64GB', 'Y31', 'Y27', 'Y27s', 'Y22', 'Y21',
            'Y17s_4_128', 'Y17s_6_128', 'Y16', 'Y15S', 'Y12S', 'Y03_64GB', 'Y03_128GB',
            'Y02T', 'Y1S', 'X100'
        ]

        if model_name not in allowed_columns:
            raise ValueError("Invalid model name provided")

        # Using string formatting for column names which is safe since we have validated it above
        sql = f"UPDATE Stock SET {model_name}=$1 WHERE Telegram_id=$2"

        # Execute the SQL command
        return await self.execute(sql, count, telegram_id, execute=True)

    async def count_stock(self):
        sql = "SELECT COUNT(*) FROM Stock"
        return await self.execute(sql, fetchval=True)

    async def delete_stock(self):
        await self.execute("DELETE FROM Stock WHERE TRUE", execute=True)

    async def drop_stock(self):
        await self.execute("DROP TABLE Stock", execute=True)

