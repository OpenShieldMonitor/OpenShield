import os
import json
from pymongo import MongoClient
from config import settings
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

class MongoStorage:
    def __init__(self):
        MONGO_URI = os.getenv("MONGODB_URI", "")
        DB_NAME = os.getenv("MONGODB_DB_NAME", "")
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]

    def insert_documents(self, collection, docs):
        if docs:
            self.db[collection].insert_many(docs)

    def find_documents(self, collection, projection=None):
        return list(self.db[collection].find({}, projection))

    def delete_all(self, collection):
        return self.db[collection].delete_many({})

class LocalStorage:
    def __init__(self):
        os.makedirs(settings.DATA_PATH, exist_ok=True)

    def _path(self, collection):
        return os.path.join(settings.DATA_PATH, f"{collection}.json")

    def _load(self, collection):
        path = self._path(collection)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, collection, data):
        path = self._path(collection)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def insert_documents(self, collection, docs):
        if not docs:
            return
        data = self._load(collection)
        data.extend(docs)
        self._save(collection, data)

    def find_documents(self, collection, projection=None):
        return self._load(collection)

    def delete_all(self, collection):
        self._save(collection, [])
        class FakeResult: deleted_count = 1
        return FakeResult()

# Selecciona backend según settings
if settings.STORAGE_MODE == "mongo":
    storage = MongoStorage()
else:
    storage = LocalStorage()
