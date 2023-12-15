import json
import requests
import asyncio
import asyncpg
from .constants import *
from .settings import *
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/players/{player_id}")
async def get_player_info(player_id):
    api_url = f"https://api.opendota.com/api/players/{player_id}"
    res = requests.get(url=api_url, headers=HEADERS)
    py_logger.info(f'From url {api_url}Status = > {res.status_code}')
    await Db(url=api_url, query_id=player_id, res=res).record_request()
    return res.json



@app.get("/matches/{match_id}")
async def get_match_info(match_id):
    api_url = f"https://api.opendota.com/api/matches/{match_id}"
    res = requests.get(url=api_url, headers=HEADERS)
    py_logger.info(f'From url {api_url} Status = > {res.status_code}')
    await Db(url=api_url, query_id=match_id, res=res).record_request()
    return res.json()


class Db:

    def __init__(self, query_id, res, url):
        self.query_id = query_id
        self.res = res
        self.url = url

    async def record_request(self):
        conn = await asyncpg.connect(host='db', port='5432', database='infodota_db', user='postgres', password='postgres')
        main = (self.url, self.query_id, self.res.text)
        await conn.execute("INSERT INTO main_data (url, request_body, response) VALUES ($1,$2,$3);", main[0], main[1], main[2])
        metadata = (self.res.headers['date'], self.res.status_code, self.res.elapsed.total_seconds())
        await conn.execute("INSERT INTO metadata (datetime, status, req_timing) VALUES ($1,$2,$3);", metadata[0], str(metadata[1]), str(metadata[2]))
        await conn.close()
