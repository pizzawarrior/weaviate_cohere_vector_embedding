import weaviate
import os
from dotenv import load_dotenv

load_dotenv()

WCD_URL = os.getenv("WCD_URL")
API_KEY = os.getenv("WCD_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not WCD_URL or not API_KEY or not COHERE_API_KEY:
    raise ValueError("Please set WCD_URL, WCD_API_KEY, and COHERE_API_KEY in your .env file")

headers = {
    "X-Cohere-Api-Key": COHERE_API_KEY
}

client = weaviate.connect_to_wcs(
    cluster_url=WCD_URL,
    auth_credentials=weaviate.auth.AuthApiKey(API_KEY),
    headers=headers
)

try:
    meta = client.get_meta()
    print(meta)
except weaviate.exceptions.UnexpectedStatusCodeError as e:
    print(f'Error:{e}')

finally:
    client.close()
