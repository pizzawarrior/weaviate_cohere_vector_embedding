import weaviate.classes.query as wq
import os
import cohere
from dotenv import load_dotenv
from database.open_db_connection import client
from utils.vectorize import vectorize

# Vector Search ---->

load_dotenv()

co_token = os.getenv("COHERE_API_KEY")
co = cohere.Client(co_token)

client.connect()

movies = client.collections.get("MovieCustomVector")
query_text = 'comedy'
query_vector = vectorize(co, [query_text])[0]

response = movies.query.near_vector(
    near_vector=query_vector,
    limit=5,
    return_metadata=wq.MetadataQuery(distance=True),
)

# Inspect response
for o in response.objects:
    print(
        o.properties["title"], o.properties["release_date"].year
    )
    print(
        f'Distance to query: {o.metadata.distance:.3f}\n'
    )

client.close()
