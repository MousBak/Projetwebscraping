from pymongo import MongoClient

def get_collection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["books_db"]
    return db["books_collection"]
