import asyncpg
from pydantic import BaseModel
import json


class MainData(BaseModel):
    query_id: str
    res: object
    url: str


class Db:

    item = None

    def __init__(self, query_id=None):
        self.query_id = query_id

    async def check_item(self):
        conn = await asyncpg.connect(host='db', port='5432', database='infodota_db', user='postgres',
                                     password='postgres')
        # TODO: сделать одним коннектом для обоих методов
        row = await conn.fetchval(f'SELECT response FROM main_data WHERE main_data.request_body = $1;', self.query_id)
        # TODO: изменить формат выдачи на json
        await conn.close()
        if row:
            return json.loads(row)
        else:
            return row

    async def record_request(self):
        conn = await asyncpg.connect(host='db', port='5432', database='infodota_db', user='postgres',
                                     password='postgres')
        await conn.execute("INSERT INTO main_data (url, request_body, response) VALUES ($1,$2,$3);",
                           self.item.url,
                           self.item.query_id,
                           self.item.res.text)
        await conn.execute("INSERT INTO metadata (datetime, status, req_timing) VALUES ($1,$2,$3);",
                           str(self.item.res.headers['date']),
                           str(self.item.res.status_code),
                           str(self.item.res.elapsed.total_seconds()))
        await conn.close()
