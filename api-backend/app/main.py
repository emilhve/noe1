from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from dotenv import load_dotenv
import os
import json
from urllib.request import urlopen
from pathlib import Path

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

API_KEY = os.getenv("API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API is running"}

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items")
def create_item(item: Item):
    return {"created": item}

@app.get("/weather")
def get_weather():
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Missing API_KEY")

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        "?lat=58.968178&lon=5.732902&units=metric&appid="
        + API_KEY
    )
    with urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        print("===" * 10)
        print(data)
    return data
