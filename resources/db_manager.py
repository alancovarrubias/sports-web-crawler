from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
class DbManager:
    def __init__(self):
        self.db = client.crawler_db
        self.collections = list(self.db.list_collection_names())
    
    def file_exists(self):
        return self.collections

    def insert_collection(self, content):
        self.db
        pass

    def read_json(self):
        pass
