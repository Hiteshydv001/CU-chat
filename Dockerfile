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
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure FAISS index is built without breaking the build
RUN /opt/venv/bin/python -m utils.faiss_search || echo "FAISS index build failed. Check chatbot.log"

# Expose the Render-assigned port
EXPOSE 8080

# Use absolute path for Gunicorn
CMD ["/opt/venv/bin/gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "300", "--log-level", "debug", "app:app"]
