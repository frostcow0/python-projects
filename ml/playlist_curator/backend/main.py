"""Author: Jon Martin

Utilizes FastAPI to serve user's songs and recommendations"""

import uvicorn
import logging
import pandas as pd
from sys import stdout
from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from recommendation_engine import get_user_data, get_recommendations, save_playlist


class SongData(BaseModel):
    feature_saved: str
    feature_50: str

class Recommendations(BaseModel):
    formatted: dict
    raw: dict

class SongsToSave(BaseModel):
    recommended: str

app = FastAPI()

logger = logging.getLogger("FastAPI_Backend")
sh = logging.StreamHandler(stdout)
fh = logging.FileHandler(f"../logs/backend_errors_{date.today()}.log")
sh.setLevel(logging.INFO)
fh.setLevel(logging.WARNING)
logger.addHandler(sh)
logger.addHandler(fh)

@app.get("/user_data")
def user_data() -> dict:
    data = get_user_data()
    if "error_code" in data.keys():
        raise HTTPException(status_code=data["error_code"])
    return data

@app.post("/minkowski_recommend")
def mink_recommend(song_dict:SongData) -> dict:
    frames = {
        "feature_saved": pd.read_json(song_dict.feature_saved),
        "feature_50": pd.read_json(song_dict.feature_50),
    }
    formatted, raw = get_recommendations(song_data=frames, method="minkowski")
    return Recommendations(formatted=formatted.to_dict(), raw=raw.to_dict())

@app.post("/save_playlist")
def save_recommended(song_dict:SongsToSave) -> dict:
    recommended = pd.read_json(song_dict.recommended),
    save_playlist(recommended=recommended)
    return None


if __name__ == "__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8080)
    uvicorn.run("main:app")
