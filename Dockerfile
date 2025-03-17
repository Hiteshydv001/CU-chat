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

# Pre-build FAISS index (optional, adjust path if needed)
RUN . /opt/venv/bin/activate && python -m utils.faiss_search

# Expose port
EXPOSE 5000

# Run the application
CMD ["sh", "-c", ". /opt/venv/bin/activate && gunicorn --bind 0.0.0.0:5000 app:app"]
