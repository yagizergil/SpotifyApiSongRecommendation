import base64
import json
import requests
import sqlite3
import re
import main
def songRecom(database_name, column_names, table_name , client_id , client_secret,limit):
    if __name__ == '__main__':
        database_name = database_name
        client_id = client_id
        client_secret = client_secret
        table_name = table_name
        column_names = column_names
        limit = limit

    def get_token():
        auth_string = client_id + ':' + client_secret
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = requests.post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token

    token = get_token()


    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()


    table_name = table_name
    column_names = column_names

    column_info = {}


    def get_most_common_genre():
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        cursor.execute(f"SELECT genres FROM {table_name} GROUP BY genres ORDER BY COUNT(*) DESC LIMIT 1")
        most_common_genre_row = cursor.fetchone()

        connection.close()

        # Check if the query returned any result
        if most_common_genre_row:
            most_common_genre, = most_common_genre_row
            if most_common_genre:
                return most_common_genre.split(",")[0].strip()

        return None

    most_common_genre = get_most_common_genre()
    print(most_common_genre)


    def round_to_decimal(value, decimal_places=2):
        return round(value, decimal_places)
    def get_random_track_id_for_genre(genre):
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        cursor.execute(f"SELECT track_id FROM  {table_name} WHERE genres LIKE ? ORDER BY RANDOM() LIMIT 1", ('%' + genre + '%',))
        track_id_row = cursor.fetchone()

        connection.close()

        # Check if the query returned any result
        if track_id_row:
            track_id, = track_id_row
            return track_id

        return None

    random_track_id = get_random_track_id_for_genre(most_common_genre)
    print(random_track_id)


    for column_name in column_names:

        cursor.execute(f"SELECT MIN({column_name}) FROM {table_name}")
        min_value = cursor.fetchone()[0]

        cursor.execute(f"SELECT MAX({column_name}) FROM {table_name}")
        max_value = cursor.fetchone()[0]

        cursor.execute(f"SELECT AVG({column_name}) FROM {table_name}")
        target_value = cursor.fetchone()[0]

        column_info[column_name] = {
            "min": round_to_decimal(min_value),
            "max": round_to_decimal(max_value),
            "target": round_to_decimal(target_value)
        }

    connection.close()
    # print(column_info)

    params = {
        "seed_genres" :most_common_genre,
        "seed_tracks" :random_track_id,
        "limit": limit,
        "min_acousticness": column_info["acousticness"]["min"],
        "max_acousticness": column_info["acousticness"]["max"],
        "target_acousticness": column_info["acousticness"]["target"],
        "min_danceability": column_info["danceability"]["min"],
        "max_danceability": column_info["danceability"]["max"],
        "target_danceability": column_info["danceability"]["target"],
        "min_duration_ms": int(column_info["duration_ms"]["min"]),
        "max_duration_ms": int(column_info["duration_ms"]["max"]),
        "target_duration_ms": int(column_info["duration_ms"]["target"]),
        "min_energy": column_info["energy"]["min"],
        "max_energy": column_info["energy"]["max"],
        "target_energy": column_info["energy"]["target"],
        "min_instrumentalness": column_info["instrumentalness"]["min"],
        "max_instrumentalness": column_info["instrumentalness"]["max"],
        "target_instrumentalness": column_info["instrumentalness"]["target"],
        "min_liveness": column_info["liveness"]["min"],
        "max_liveness": column_info["liveness"]["max"],
        "target_liveness": column_info["liveness"]["target"],
        "min_loudness": column_info["loudness"]["min"],
        "max_loudness": column_info["loudness"]["max"],
        "target_loudness": column_info["loudness"]["target"],
        "min_popularity": int(column_info["popularity"]["min"]),
        "max_popularity": int(column_info["popularity"]["max"]),
        "target_popularity":int(column_info["popularity"]["target"]),
        "min_speechiness": column_info["speechiness"]["min"],
        "max_speechiness": column_info["speechiness"]["max"],
        "target_speechiness": column_info["speechiness"]["target"],
        "min_tempo": column_info["tempo"]["min"],
        "max_tempo": column_info["tempo"]["max"],
        "target_tempo": column_info["tempo"]["target"],
        "min_valence": column_info["valence"]["min"],
        "max_valence": column_info["valence"]["max"],
        "target_valence": column_info["valence"]["target"],
    }

    url = "https://api.spotify.com/v1/recommendations"


    headers = {
        "Authorization": "Bearer " + token
    }

    result = requests.get(url, headers=headers, params=params)
    recommendations = json.loads(result.content)
    # print(json.dumps(recommendations, indent=5))
    print(json.dumps(recommendations, indent=5))
    tracks = recommendations.get("tracks", [])


    printed_urls = set()
    printed_names = set()
    recommended_songs = []

    for first_track in tracks:
        desired_name = first_track.get("name", "")
        desired_photo = first_track.get("album", {}).get("images", [])[0].get("url", "")
        desired_info = first_track.get("external_urls", {}).get("spotify", "")
        if desired_name not in printed_names:
            printed_names.add(desired_name)
            recommended_songs.append({"name": desired_name, "photo": desired_photo, "info": desired_info})

    return recommended_songs
