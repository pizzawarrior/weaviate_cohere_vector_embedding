import os
import cohere
from dotenv import load_dotenv
from typing import List
from cohere import Client as CohereClient
from database.open_db_connection import client
# from vector_search import query_vector

# RAG query, aka Generative query ----->


load_dotenv()

co_token = os.getenv("COHERE_API_KEY")
co = cohere.Client(co_token)

client.connect()

movies = client.collections.get("MovieCustomVector")


def vectorize(cohere_client: CohereClient, texts: List[str]) -> List[List[float]]:

    response = cohere_client.embed(
        texts=texts, model="embed-multilingual-v3.0", input_type="search_document"
    )

    return response.embeddings


query_text = "dystopian future"
query_vector = vectorize(co, [query_text])[0]
generate_prompt = "Write {overview} as a haiku poem"

try:
    response = movies.generate.near_text(
        near_vector=query_vector,
        limit=5,
        single_prompt=generate_prompt
    )

    for o in response.objects:
        print(o.properties["title"])
        print(f'{o.generated}\n')

finally:
    client.close()
