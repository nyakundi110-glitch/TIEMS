FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py .

# Create directory for logs and state
RUN mkdir -p /app/logs /app/data

# Environment variables
ENV PYTHONUNBUFFERED=1

# Expose port for web interface
EXPOSE 5000

# Run the application
CMD ["python", "run_monitor.py"]
