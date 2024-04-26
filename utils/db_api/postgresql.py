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





    async def create_table_imei(self):
        sql = """
        CREATE TABLE IF NOT EXISTS IMEI (
        id SERIAL PRIMARY KEY,
        model VARCHAR(255) NOT NULL,
        imei VARCHAR(255) NOT NULL UNIQUE,
        sticker VARCHAR(255) NOT NULL,
        now_date VARCHAR(255) NOT NULL,
        telegram_id BIGINT NOT NULL
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

    async def add_imei(self, model, imei, sticker, now_date, telegram_id):
        sql = "INSERT INTO IMEI(model, imei, sticker, now_date, telegram_id) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, model, imei, sticker, now_date, telegram_id, fetchrow=True)


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