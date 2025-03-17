from sentence_transformers import SentenceTransformer
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

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(text):
    try:
        embedding = model.encode(text, convert_to_tensor=False, show_progress_bar=False)
        return embedding.tolist()
    except Exception as e:
        logging.error(f"Embedding generation error: {str(e)}")
        return None

def batch_generate_embeddings(texts):
    try:
        embeddings = model.encode(texts, batch_size=32, convert_to_tensor=False, show_progress_bar=False)
        return embeddings.tolist()
    except Exception as e:
        logging.error(f"Batch embedding error: {str(e)}")
        return None