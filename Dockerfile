# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for FAISS and PyMuPDF)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN python -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Pre-build FAISS index with logging
RUN . /opt/venv/bin/activate && python -m utils.faiss_search || { echo "FAISS index build failed"; cat chatbot.log; exit 1; }

# Expose port
EXPOSE 5000

# Run the application with reduced workers and increased timeout
CMD ["sh", "-c", ". /opt/venv/bin/activate && gunicorn --bind 0.0.0.0:8080 --workers 1 --timeout 300 --log-level debug app:app"]
