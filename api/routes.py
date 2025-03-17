from flask import jsonify, request
from models.llm import generate_response
from utils.faiss_search import search_faiss
from database.queries import fetch_structured_data
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

def init_routes(app):
    @app.route("/chat", methods=["POST"])
    def chat():
        try:
            data = request.get_json()
            if not data or "query" not in data:
                logging.warning("Invalid request: No query provided")
                return jsonify({"error": "Query is required"}), 400

            query = data["query"].strip()
            logging.info(f"Processing query: {query}")

            # Tier 1: FAISS semantic search
            faiss_result = search_faiss(query)
            if faiss_result:
                logging.info("Found answer in FAISS")
                return jsonify({"response": faiss_result, "source": "faiss"})

            # Tier 2: Structured data lookup
            db_result = fetch_structured_data(query)
            if db_result:
                logging.info("Found answer in MongoDB")
                return jsonify({"response": db_result, "source": "db"})

            # Tier 3: LLM fallback
            llm_response = generate_response(query)
            logging.info("Generated response with LLM")
            return jsonify({"response": llm_response, "source": "llm"})

        except Exception as e:
            logging.error(f"Error processing query: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500