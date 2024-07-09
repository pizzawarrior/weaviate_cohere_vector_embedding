from open_db_connection import client

try:
    client.close()
finally:
    print('Weaviate connection terminated')
