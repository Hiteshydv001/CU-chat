from sentence_transformers import SentenceTransformer
import logging
import os

# Configure logging
logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Use a lighter model to reduce memory usage
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")  # Explicitly set to CPU

def generate_embeddings(text):
    try:
        logging.info(f"Generating embedding for text: {text[:50]}...")
        embedding = model.encode(text, convert_to_tensor=False, show_progress_bar=False)
        logging.info("Embedding generated successfully")
        return embedding.tolist()
    except Exception as e:
        logging.error(f"Embedding generation error: {str(e)}")
        return None

def batch_generate_embeddings(texts):
    try:
        logging.info(f"Generating batch embeddings for {len(texts)} texts")
        embeddings = model.encode(texts, batch_size=32, convert_to_tensor=False, show_progress_bar=False)
        logging.info("Batch embeddings generated successfully")
        return embeddings.tolist()
    except Exception as e:
        logging.error(f"Batch embedding error: {str(e)}")
        return None