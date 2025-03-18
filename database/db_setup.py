from pymongo import MongoClient, TEXT
from config.settings import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION
import logging
import os

# Configure logging
logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def init_db():
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION]

        # Create text index for question and category
        collection.create_index([("question", TEXT), ("category", TEXT)], default_language="english")

        # Sample data
        sample_data = [
            {
                "category": "hostel",
                "question": "What is the hostel curfew?",
                "answer": "10 PM on weekdays, 11 PM on weekends",
                "last_updated": {"$date": "2025-03-16T00:00:00Z"},
                "source": "university_faqs.pdf"
            },
            {
                "category": "academics",
                "question": "When are exams scheduled?",
                "answer": "Check the university website for the latest schedule.",
                "last_updated": {"$date": "2025-03-16T00:00:00Z"},
                "source": "university_website"
            }
        ]

        # Insert only if collection is empty
        if collection.count_documents({}) == 0:
            collection.insert_many(sample_data)
            logging.info("Inserted sample data into MongoDB")

        logging.info("MongoDB initialized successfully")
        client.close()
    except Exception as e:
        logging.error(f"MongoDB setup error: {str(e)}")

if __name__ == "__main__":
    init_db()