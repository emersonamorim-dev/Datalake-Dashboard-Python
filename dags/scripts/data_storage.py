from pymongo import MongoClient
import json

def store_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['meteomatics_db']
    collection = db['processed_data']
    
    with open('/data/processed/data.json', 'r') as f:
        data = json.load(f)
    
    collection.insert_many(data)
    print("Dados armazenados no MongoDB com sucesso!")
