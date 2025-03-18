import faiss
import numpy as np
from utils.preprocess import generate_embeddings
import logging
import pickle
import os

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
        
        # Default fallback data if files are missing
        default_text = """
        What is the hostel curfew?
        10 PM on weekdays, 11 PM on weekends
        When are exams scheduled?
        Check the university website for the latest schedule.
        """
        faqs = {}
        
        # Try extracting from PDF first
        pdf_path = "data/university_faqs.pdf"
        logging.info(f"Checking if PDF exists: {pdf_path}")
        if os.path.exists(pdf_path):
            text = extract_text_from_pdf(pdf_path)
            faqs = extract_faqs(text)
        
        # If no FAQs, try text file or use default
        if not faqs:
            text_path = "data/university_faqs.txt"
            logging.warning("No FAQs extracted from PDF, falling back to university_faqs.txt or default")
            logging.info(f"Checking if text file exists: {text_path}")
            if os.path.exists(text_path):
                with open(text_path, "r", encoding="utf-8") as f:
                    text = f.read()
            else:
                logging.warning(f"Text file not found, using default data")
                text = default_text
            faqs = extract_faqs(text)
        
        questions = list(faqs.keys())
        logging.info(f"Extracted {len(questions)} questions: {questions}")
        if not questions:
            logging.error("No questions extracted after fallback")
            raise ValueError("No valid questions found")
        
        logging.info("Generating embeddings for questions")
        embeddings = np.array([generate_embeddings(q) for q in questions], dtype="float32")
        logging.info(f"Embeddings shape: {embeddings.shape}")
        if embeddings.size == 0:
            logging.error("No valid embeddings generated")
            raise ValueError("No valid embeddings generated")
        
        dimension = embeddings.shape[1]
        logging.info(f"Creating FAISS index with dimension: {dimension}")
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        logging.info(f"Saving FAISS index to {INDEX_PATH}")
        faiss.write_index(index, INDEX_PATH)
        
        logging.info(f"Saving FAQ dictionary to {FAQ_DICT_PATH}")
        with open(FAQ_DICT_PATH, "wb") as f:
            pickle.dump(faqs, f)
        logging.info("FAISS index and FAQ dictionary built successfully")
    except Exception as e:
        logging.error(f"Unexpected error during FAISS index build: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)