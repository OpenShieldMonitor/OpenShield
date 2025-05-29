from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

# Conexión a MongoDB
MONGO_URI = os.getenv("MONGODB_URI", "")
DB_NAME = os.getenv("MONGODB_DB_NAME", "")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def insert_document(collection_name, document):
    """Inserta un documento en una colección."""
    return db[collection_name].insert_one(document)

def insert_documents(collection_name, documents):
    """Inserta múltiples documentos en una colección."""
    return db[collection_name].insert_many(documents)

def find_documents(collection_name, query={}, projection=None):
    """Devuelve una lista de documentos que cumplen el filtro."""
    return list(db[collection_name].find(query, projection))

def find_one(collection_name, query={}, projection=None):
    """Devuelve un único documento que cumple el filtro."""
    return db[collection_name].find_one(query, projection)

def delete_documents(collection_name, query):
    """Elimina documentos según un filtro."""
    return db[collection_name].delete_many(query)

def delete_all(collection_name):
    """Elimina todos los documentos de una colección."""
    return db[collection_name].delete_many({})

def count_documents(collection_name, query={}):
    """Cuenta cuántos documentos cumplen el filtro."""
    return db[collection_name].count_documents(query)
