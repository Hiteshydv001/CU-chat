import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Points to chat-cu-backend

FLASK_ENV = os.getenv("FLASK_ENV", "production")
DEBUG = FLASK_ENV == "development"
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "your-default-secret-key")
HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 5000))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = "cu_chatbot"
MONGO_COLLECTION = "info"

FAISS_INDEX_PATH = BASE_DIR / "data" / "faiss_index.bin"
FAQ_DICT_PATH = BASE_DIR / "data" / "faq_dict.pkl"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_MAX_TOKENS = 200
GEMINI_TEMPERATURE = 0.7
GEMINI_TOP_P = 0.9

LOG_FILE = BASE_DIR / "chatbot.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

DATA_DIR = BASE_DIR / "data"
PDF_PATH = DATA_DIR / "university_faqs.pdf"

DATA_DIR.mkdir(exist_ok=True)