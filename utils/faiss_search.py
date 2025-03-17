import faiss
import numpy as np
from utils.preprocess import generate_embeddings
import logging
import pickle
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

INDEX_PATH = "data/faiss_index.bin"
FAQ_DICT_PATH = "data/faq_dict.pkl"

class FaissSearcher:
    def __init__(self):
        try:
            self.index = faiss.read_index(INDEX_PATH)
            with open(FAQ_DICT_PATH, "rb") as f:
                self.faq_dict = pickle.load(f)
            logging.info("FAISS index and FAQ dictionary loaded")
        except Exception as e:
            logging.error(f"FAISS init error: {str(e)}")
            raise

    def search(self, query):
        try:
            query_embedding = np.array([generate_embeddings(query)], dtype="float32")
            D, I = self.index.search(query_embedding, k=1)
            threshold = 0.5
            if D[0][0] < threshold:
                matched_question = list(self.faq_dict.keys())[I[0][0]]
                return self.faq_dict[matched_question]
            return None
        except Exception as e:
            logging.error(f"FAISS search error: {str(e)}")
            return None

searcher = None

def search_faiss(query):
    global searcher
    if searcher is None:
        searcher = FaissSearcher()
    return searcher.search(query)

# Script to build FAISS index
if __name__ == "__main__":
    logging.info("Starting FAISS index build process")
    try:
        from utils.pdf_extractor import extract_text_from_pdf, extract_faqs
        
        # Verify PDF file exists
        pdf_path = "data/university_faqs.pdf"
        logging.info(f"Checking if PDF exists: {pdf_path}")
        if not os.path.exists(pdf_path):
            logging.warning(f"PDF file not found: {pdf_path}")
        else:
            # Try extracting from PDF first
            text = extract_text_from_pdf(pdf_path)
            faqs = extract_faqs(text)
        # If no FAQs extracted, fall back to text file
        if not faqs:
            text_path = "data/university_faqs.txt"
            logging.warning("No FAQs extracted from PDF, falling back to university_faqs.txt")
            logging.info(f"Checking if text file exists: {text_path}")
            if not os.path.exists(text_path):
                logging.error(f"Text file not found: {text_path}")
                raise FileNotFoundError(f"Text file not found: {text_path}")
            with open(text_path, "r", encoding="utf-8") as f:
                text = f.read()
            faqs = extract_faqs(text)
        
        questions = list(faqs.keys())
        logging.info(f"Extracted {len(questions)} questions")
        if not questions:
            logging.error("No questions extracted after fallback")
            raise ValueError("No valid questions found")
        
        logging.info("Generating embeddings for questions")
        embeddings = np.array([generate_embeddings(q) for q in questions], dtype="float32")
        logging.info(f"Embeddings shape: {embeddings.shape}")
        if embeddings.size == 0:
            logging.error("No valid embeddings generated")
            raise ValueError("No valid embeddings generated")
        
        # Basic FAISS Index (can be replaced with advanced techniques below)
        dimension = embeddings.shape[1]
        logging.info(f"Creating FAISS index with dimension: {dimension}")
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        logging.info(f"Saving FAISS index to {INDEX_PATH}")
        faiss.write_index(index, INDEX_PATH)
        
        # Optional: Advanced FAISS Index (uncomment to use)
        # nlist = 100  # Number of clusters
        # quantizer = faiss.IndexFlatL2(dimension)
        # index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
        # index.train(embeddings)
        # index.add(embeddings)
        
        logging.info(f"Saving FAQ dictionary to {FAQ_DICT_PATH}")
        with open(FAQ_DICT_PATH, "wb") as f:
            pickle.dump(faqs, f)
        logging.info("FAISS index and FAQ dictionary built successfully")
        
        # Optional: Store in MongoDB (uncomment to use)
        # from pymongo import MongoClient
        # client = MongoClient(MONGO_URI)
        # db = client[MONGO_DB_NAME]
        # collection = db["raw_data"]
        # for q, a in faqs.items():
        #     collection.insert_one({"question": q, "answer": a, "embedding": embeddings[list(faqs.keys()).index(q)].tolist()})
        # client.close()
        # logging.info("Data stored in MongoDB")
        
        # Optional: Use Pinecone (uncomment to use, requires pinecone-client)
        # import pinecone
        # pinecone.init(api_key="YOUR_PINECONE_API_KEY", environment="YOUR_ENV")
        # index = pinecone.Index("cu-chatbot-index")
        # index.upsert(vectors=[(str(i), emb, {"question": q, "answer": a}) for i, (q, a), emb in enumerate(zip(faqs.keys(), faqs.values(), embeddings))])
        # logging.info("Data stored in Pinecone")
        
    except Exception as e:
        logging.error(f"Unexpected error during FAISS index build: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)