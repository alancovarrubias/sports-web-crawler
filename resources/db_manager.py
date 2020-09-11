from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
class DbManager:
    def __init__(self, key_store):
        db = client[key_store.sport]
        collection_names = db.list_collection_names()
        self.collection = db[key_store.resource_type]
        self.resource_exists = key_store.resource_type in collection_names

    def fetch_resource(self):
        return self.collection.findOne({})

    def save_resource(self, data):
        self.collection.insert_one(data).inserted_id
        self.resource_exists = True