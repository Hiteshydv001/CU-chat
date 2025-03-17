# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Ensure correct port usage
ENV PORT=8080

# Pre-build FAISS index if needed (optional)
RUN . /opt/venv/bin/activate && python -m utils.faiss_search || echo "FAISS index prebuild failed, continuing..."

# Expose the required port for Railway
EXPOSE 8080

# Command to run the application
CMD ["/opt/venv/bin/gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
