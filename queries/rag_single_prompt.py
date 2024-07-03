import os
import cohere
from dotenv import load_dotenv
from database.open_db_connection import client
from utils.vectorize import vectorize

# RAG query, aka Generative query ----->


load_dotenv()

co_token = os.getenv("COHERE_API_KEY")
co = cohere.Client(co_token)

client.connect()

movies = client.collections.get("MovieCustomVector")
query_text = "dystopian future"
query_vector = vectorize(co, [query_text])[0]
generate_prompt = "Write {overview} as a haiku poem"

try:
    response = movies.generate.near_vector(
        near_vector=query_vector,
        limit=5,
        single_prompt=generate_prompt
    )

    for o in response.objects:
        print(o.properties["title"])
        print(f'{o.generated}\n')

finally:
    client.close()
