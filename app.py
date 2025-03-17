import os
import logging
from flask import Flask
from api.routes import init_routes
from database.db_setup import init_db

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
    port = int(os.getenv("PORT", 8080))  # Render assigns PORT dynamically
    logging.info(f"Starting Flask application on port {port}")
    app.run(debug=False, host="0.0.0.0", port=port, threaded=True)
