from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["films_db"]
print(db.list_collection_names())
print(db.top_250_imdb.count_documents({}), "films dans la collection")