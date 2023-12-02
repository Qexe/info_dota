from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

import json

import requests

import psycopg2

app = FastAPI()


@app.get("/players/{player_id}")
def get_player_info(player_id):
    api_url = f"https://api.opendota.com/api/players/{player_id}"
    res = requests.get(url=api_url)
    print(res)
    rec = Db(url=api_url, query_id=player_id, res=res).record_request(
    return res.json

@app.get("/matches/{match_id}")
def get_match_info(match_id):
    api_url = f"https://api.opendota.com/api/matches/{match_id}"
    res = requests.get(url=api_url)
    print(res)
    rec = Db(query=api_url, query_id=match_id, res=res).record_request()
    return res.json()



class Db:

    def __init__(self, query_id, res, url):
      self.query_id = query_id
      self.res = res
      self.url = url

    def record_request(self):
     conn = psycopg2.connect(host='localhost', port='5432', database = 'infodota_db', user = 'app', password = '3226')
     cur = conn.cursor()
     main = (self.url, self.query_id, self.res.text)
     cur.execute("INSERT INTO main_data (url, request_body, response) VALUES (%s,%s,%s);", main)
     metadata = (self.res.headers['date'], self.res.status_code, self.res.elapsed.total_seconds())
     cur.execute("INSERT INTO metadata (date, status, req_timing) VALUES (%s,%s,%s);", metadata)
     conn.commit()
     cur.close()
     conn.close()
