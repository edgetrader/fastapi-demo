from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

db = []

class City(BaseModel):
    name: str
    timezone: str

@app.get('/')
def index():
    return{'key':'value'}

@app.get('/cities')
def get_cities():
    results = []
    for city in db:
        r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
        city['current_time'] = r.json()['datetime']
        results.append(city)
    return results

@app.get('/cities/{city_id}')
def get_city(city_id: int):
    city = db[city_id-1]
    r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
    city['current_time'] = r.json()['datetime']
    return city

@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())
    return db[-1]

@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id-1)
    return {}
