import sqlite3

import tracksFeatures
import recomSong

def main():
    client_id = "83c35c346dec4232add9ba5fa8f5f707"
    client_secret = "760d512dcb9a47faa71989947e381105"
    limit = "5"
    playlist_id = "3s6Vi7hBE4dFEZdYqud0Rm"
    database_name = "spotify_track_features08.db"
    column_names = ["instrumentalness", "acousticness", "duration_ms", "liveness", "loudness", "speechiness", "valence", "energy", "danceability", "tempo", "popularity"]
    table_name = "track_features"


    clear_database(database_name, table_name)

    tracksFeatures.auth_and_save_features(playlist_id, database_name, table_name , client_id , client_secret)

    recomSong.songRecom(database_name, column_names, table_name , client_id , client_secret , limit)

def clear_database(database_name, table_name):
    # SQLite veritabanına bağlanalım
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    cursor.execute(f"CREATE TABLE {table_name} (track_id TEXT PRIMARY KEY, instrumentalness REAL, acousticness REAL, duration_ms REAL, liveness REAL, loudness REAL, speechiness REAL, valence REAL, energy REAL, danceability REAL, tempo REAL, popularity REAL, genres TEXT)")

    connection.commit()

    connection.close()


if __name__ == "__main__":
    main()

