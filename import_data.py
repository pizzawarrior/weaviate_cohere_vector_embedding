import pandas as pd
import requests
from datetime import datetime, timezone
import json
from weaviate.util import generate_uuid5
# from tqdm import tqdm
from database import client

client.connect()

data_url = "https://raw.githubusercontent.com/weaviate-tutorials/edu-datasets/main/movies_data_1990_2024.json"
data_resp = requests.get(data_url)
df = pd.DataFrame(data_resp.json())

embs_path = "scratch/movies_data_1990_2024_embeddings.csv"
emb_df = pd.read_csv(embs_path)

movies = client.collections.get("MovieCustomVector")

# Context manager
with movies.batch.dynamic() as batch:
    for i, movie in enumerate(df.itertuples(index=False)):
        # Convert json string to datetime and add timezone info
        release_date = datetime.strptime(movie.release_date, "%Y-%m-%d").replace(
            tzinfo=timezone.utc
        )
        # convert json array to list of integers
        genre_ids = json.loads(movie.genre_ids)
        # Build obj payload
        movie_obj = {
            "title": movie.title,
            "overview": movie.overview,
            "vote_average": movie.vote_average,
            "genre_ids": genre_ids,
            "release_date": release_date,
            "tmdb_id": movie.id
        }

        # get the vector
        vector = emb_df.iloc[i].to_list()

        batch.add_object(
            properties=movie_obj,
            uuid=generate_uuid5(movie.id),
            vector=vector
        )

if len(movies.batch.failed_objects) > 0:
    print(f'Failed to import {len(movies.batch.failed_objects)} objects')

client.close()
