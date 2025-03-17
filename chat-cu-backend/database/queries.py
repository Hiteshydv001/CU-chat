from pymongo import MongoClient
from config.settings import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION
import logging
import sys
import os

# Add the parent directory (chat-cu-backend) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_structured_data(query):
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION]

        # Optimized text search with relevance scoring
        result = collection.find_one(
            {"$text": {"$search": query}},
            sort=[("score", {"$meta": "textScore"})],
            projection={"answer": 1, "_id": 0}
        )

        client.close()
        return result["answer"] if result else None
    except Exception as e:
        logging.error(f"MongoDB query error: {str(e)}")
        return None