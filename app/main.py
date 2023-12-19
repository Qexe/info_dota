import json
import requests
import asyncpg
from .constants import *
from .settings import *
from fastapi import FastAPI
from .db import *

app = FastAPI()


@app.get("/players/{player_id}")
async def get_player_info(player_id):
    connect_db = Db(query_id=player_id)
    if res := await connect_db.check_item():
        py_logger.info(f'Find info about player id {player_id} in DB')
        return res
    else:
        api_url = f"https://api.opendota.com/api/players/{player_id}"
        res = requests.get(url=api_url, headers=HEADERS)
        py_logger.info(f'From url {api_url}Status = > {res.status_code}')
        item = MainData(query_id=player_id, url=api_url, res=res)
        connect_db.item = item
        await connect_db.record_request()
        py_logger.info(' => [Record to DB is successfully]')
        return res.json()


@app.get("/matches/{match_id}")
async def get_match_info(match_id):
    connect_db = Db(query_id=match_id)
    if res := await connect_db.check_item():
        py_logger.info(f'Find info about match id {match_id} in DB')
        return res
    else:
        api_url = f"https://api.opendota.com/api/matches/{match_id}"
        res = requests.get(url=api_url, headers=HEADERS)
        py_logger.info(f'From url {api_url} Status = > {res.status_code}')
        item = MainData(query_id=match_id, url=api_url, res=res)
        connect_db.item = item
        await connect_db.record_request()
        py_logger.info(' => [Record to DB is successfully]')
        return res.json()
