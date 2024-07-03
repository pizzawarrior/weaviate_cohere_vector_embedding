from cohere import Client as CohereClient
from typing import List


def vectorize(cohere_client: CohereClient, texts: List[str]) -> List[List[float]]:
    response = cohere_client.embed(
        texts=texts, model="embed-multilingual-v3.0", input_type="search_document"
    )

    return response.embeddings
