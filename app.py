import sqlite3

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import tracksFeatures
import recomSong
from recomSong import songRecom


app = FastAPI()

# Jinja2Templates ile HTML şablonları için bir şablon motoru ayarlayalım.
templates = Jinja2Templates(directory="templates")

# Static dosyaları için bir yol belirleyelim.
app.mount("/static", StaticFiles(directory="static"), name="static")

database_name = "spotify_track_features08.db"
column_names = ["instrumentalness", "acousticness", "duration_ms", "liveness", "loudness", "speechiness", "valence", "energy", "danceability", "tempo", "popularity"]
table_name = "track_features"
def clear_database(database_name, table_name):
    # SQLite veritabanına bağlanalım
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    cursor.execute(f"CREATE TABLE {table_name} (track_id TEXT PRIMARY KEY, instrumentalness REAL, acousticness REAL, duration_ms REAL, liveness REAL, loudness REAL, speechiness REAL, valence REAL, energy REAL, danceability REAL, tempo REAL, popularity REAL, genres TEXT)")

    connection.commit()

    connection.close()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/recommend", response_class=HTMLResponse)
async def recommend(request: Request, playlist_id: str = Form(...), limit: int = Form(...)):
    client_id = "83c35c346dec4232add9ba5fa8f5f707"
    client_secret = "760d512dcb9a47faa71989947e381105"
    database_name = "spotify_track_features08.db"
    column_names = ["instrumentalness", "acousticness", "duration_ms", "liveness", "loudness", "speechiness", "valence", "energy", "danceability", "tempo", "popularity"]
    table_name = "track_features"
    clear_database(database_name, table_name)

    tracksFeatures.auth_and_save_features(playlist_id, database_name, table_name, client_id, client_secret)

    recommended_songs = recomSong.songRecom(database_name, column_names, table_name, client_id, client_secret, limit)


    return templates.TemplateResponse("index.html", {"request": request, "recommended_songs": recommended_songs})



