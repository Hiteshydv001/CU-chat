# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for FAISS and PyMuPDF)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Ensure pip is available before creating a virtual environment
RUN python -m ensurepip

# Create a virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements file & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the application port
EXPOSE 8080

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "300", "--preload", "--log-level", "debug", "app:app"]
