from database import client


client.close()
print('Weaviate connection terminated')
