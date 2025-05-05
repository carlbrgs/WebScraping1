from pymongo import MongoClient

def get_mongo_client():
    client = MongoClient("mongodb://localhost:27017/")
    return client

def save_to_mongo(data):
    try:
        client = get_mongo_client()
        db = client['blog_scraper']
        collection = db['articles']
        collection.insert_one(data)
        print("Data saved to MongoDB")
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")