from open_db_connection import client


client.close()
print('Weaviate connection terminated')
