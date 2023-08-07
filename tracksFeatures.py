import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3

def auth_and_save_features(playlist_id, database_name, table_name , client_id , client_secret):

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Playlist'teki tüm şarkıları al
    def get_playlist_tracks(playlist_id):
        results = sp.playlist_tracks(playlist_id)
        tracks = results["items"]
        while results["next"]:
            results = sp.next(results)
            tracks.extend(results["items"])
        return tracks

    # Şarkıların "instrumentalness" özelliğini çek ve veritabanına kaydet
    def save_track_features_to_database(tracks):
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (track_id TEXT PRIMARY KEY, instrumentalness REAL, acousticness REAL, duration_ms REAL, liveness REAL, loudness REAL, speechiness REAL, valence REAL, energy REAL, danceability REAL, tempo REAL, popularity REAL, genres TEXT)")

        for track in tracks:
            if not track or not track.get("track") or not track["track"].get("id"):
                continue
            track_id = track["track"]["id"]
            track_features = sp.audio_features(track_id)[0]
            instrumentalness = track_features["instrumentalness"]
            acousticness = track_features["acousticness"]
            duration_ms = track_features["duration_ms"]
            liveness = track_features["liveness"]
            loudness = track_features["loudness"]
            speechiness = track_features["speechiness"]
            valence = track_features["valence"]
            energy = track_features['energy']
            danceability = track_features['danceability']
            tempo = track_features['tempo']
            artist_id = track["track"]["artists"][0]["id"]
            artist_info = sp.artist(artist_id)
            popularity = artist_info["popularity"]

            genres = artist_info.get("genres")
            genres_str = ', '.join(genres) if genres else ""

            c.execute(f"INSERT OR REPLACE INTO {table_name} (track_id, instrumentalness, acousticness, duration_ms, liveness, loudness, speechiness, valence, energy, danceability, tempo, popularity, genres) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (track_id, instrumentalness, acousticness, duration_ms, liveness, loudness, speechiness, valence, energy, danceability, tempo, popularity, ', '.join(genres)))

            time.sleep(0.5)

        conn.commit()
        conn.close()

    playlist_tracks = get_playlist_tracks(playlist_id)
    save_track_features_to_database(playlist_tracks)

