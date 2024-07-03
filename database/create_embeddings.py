import requests
import pandas as pd
import os
import cohere
from dotenv import load_dotenv
from utils.vectorize import vectorize


load_dotenv()

co_token = os.getenv("COHERE_APIKEY")
co = cohere.Client(co_token)

data_url = "https://raw.githubusercontent.com/weaviate-tutorials/edu-datasets/main/movies_data_1990_2024.json"
resp = requests.get(data_url)
df = pd.DataFrame(resp.json())

emb_dfs = []
src_texts = []

for i, row in enumerate(df.itertuples(index=False)):
    src_text = "Title" + row.title + "; Overview: " + row.overview
    src_texts.append(src_text)

    if (len(src_texts) == 50) or (i + 1 == len(df)):
        output = vectorize(co, src_texts)
        index = list(range(i - len(src_texts) + 1, i + 1))
        emb_df = pd.DataFrame(output, index=index)
        emb_dfs.append(emb_df)
        src_texts = []

emb_df = pd.concat(emb_dfs)

os.makedirs("scratch", exist_ok=True)
emb_df.to_csv(
    "scratch/movies_data_1990_2024_embeddings.csv",
    index=False,
)
