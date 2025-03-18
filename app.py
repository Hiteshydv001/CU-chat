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
logging.info("Flask application initialized")

# Defer database initialization to the first request
def init_app():
    with app.app_context():
        init_db()
        init_routes(app)
        logging.info("Database and routes initialized")

# Initialize on first request
init_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default to 5000 for Railway/Render
    logging.info(f"Starting Flask application on port {port} for development")
    app.run(debug=False, host="0.0.0.0", port=port)