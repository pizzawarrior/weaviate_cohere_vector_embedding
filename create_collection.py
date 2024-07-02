import weaviate.classes.config as wc
from database import client

# raise exception if not connected
assert client.is_live()

client.collections.create(
    name="MovieCustomVector",
    properties=[
        wc.Property(name='title', data_type=wc.DataType.TEXT),
        wc.Property(name="overview", data_type=wc.DataType.TEXT),
        wc.Property(name="vote_average", data_type=wc.DataType.NUMBER),
        wc.Property(name="genre_ids", data_type=wc.DataType.INT_ARRAY),
        wc.Property(name="release_date", data_type=wc.DataType.DATE),
        wc.Property(name="tmdb_id", data_type=wc.DataType.INT),
    ],
    vectorizer_config=wc.Configure.Vectorizer.none(),
    generative_config=wc.Configure.Generative.cohere()
)

client.close()
