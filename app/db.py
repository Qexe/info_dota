import asyncpg
import asyncio
from pydantic import BaseModel
import json


class MainData(BaseModel):
    query_id: str
    res: object
    url: str


class Db:
    _connection = None
    item = None

    def __init__(self, query_id=None):
        self.query_id = query_id


    async def connect(self):
        if not Db._connection:
            self._connection = await asyncpg.connect(host='db',
                                                     port='5432',
                                                     database='infodota_db',
                                                     user='postgres',
                                                     password='postgres')

    async def disconnect(self):
        if self._connection:
            await self._connection.close()
            self._connection = None

    async def check_item(self):
        row = await self._connection.fetchval(f'SELECT response FROM main_data WHERE main_data.request_body = $1;',
                                              self.query_id)
        if row:
            return row

    async def record_request(self):
        await self._connection.execute("INSERT INTO main_data (url, request_body, response) VALUES ($1,$2,$3);",
                                       self.item.url,
                                       self.item.query_id,
                                       self.item.res.text)
        await self._connection.execute("INSERT INTO metadata (datetime, status, req_timing) VALUES ($1,$2,$3);",
                                       str(self.item.res.headers['date']),
                                       str(self.item.res.status_code),
                                       str(self.item.res.elapsed.total_seconds()))
