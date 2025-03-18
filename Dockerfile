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
    && pip install --upgrade pip \
    && pip install --no-cache-dir torch==2.6.0+cpu torchvision==0.21.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Pre-download the SentenceTransformer model to avoid runtime download
RUN . /opt/venv/bin/activate && python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('paraphrase-MiniLM-L3-v2', device='cpu')"

# Pre-build FAISS index with logging
RUN . /opt/venv/bin/activate && python -m utils.faiss_search || { echo "FAISS index build failed"; cat chatbot.log; exit 1; }

# Expose port
EXPOSE 5000

# Run the application with optimized settings
CMD ["sh", "-c", ". /opt/venv/bin/activate && gunicorn --bind 0.0.0.0:5000 --workers 1 --timeout 600 --graceful-timeout 600 --log-level debug app:app"]
