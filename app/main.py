import json
import requests
import asyncpg
from fastapi import FastAPI, Request
from .constants import *
from .settings import *
from .db import *
from .pages.router import router as router_pages

app = FastAPI()

app.include_router(router_pages)

@app.get("/players/{player_id}")
async def get_player_info(player_id):
    db_connection = Db(query_id=player_id)
    await db_connection.connect()

    if res := await db_connection.check_item():
        py_logger.info(f'Find info about player id {player_id} in DB')
        return json.loads(res)
    else:
        api_url = f"{PLAYERS_ROUT}{player_id}"
        res = requests.get(url=api_url, headers=HEADERS)
        py_logger.info(f'From url {api_url} Status = > {res.status_code}')
        db_connection.item = MainData(query_id=player_id, url=api_url, res=res)
        await db_connection.record_request()
        py_logger.info(' => [Record to DB is successfully]')
        await db_connection.disconnect()
        return res.json()

@app.get("/matches/{match_id}")
async def get_match_info(match_id):
    db_connection = Db(query_id=match_id)
    await db_connection.connect()

    if res := await db_connection.check_item():
        py_logger.info(f'Find info about match id {match_id} in DB')
        return json.loads(res)
    else:
        api_url = f"{MATCHES_ROUT}{match_id}"
        res = requests.get(url=api_url, headers=HEADERS)
        py_logger.info(f'From url {api_url} Status = > {res.status_code}')
        db_connection.item = MainData(query_id=match_id, url=api_url, res=res)
        await db_connection.record_request()
        py_logger.info(' => [Record to DB is successfully]')
        await db_connection.disconnect()
        return res.json()
