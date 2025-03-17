from flask import Flask
from api.routes import init_routes
from database.db_setup import init_db
import logging
import os
import sys

# Add the parent directory (chat-cu-backend) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

# Initialize database and routes
init_db()
init_routes(app)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logging.info(f"Starting Flask application on port {port}")
    app.run(debug=False, host="0.0.0.0", port=port, threaded=True)
