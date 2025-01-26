# Use slim Python image with specific version
FROM python:3.9-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies and clean in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with minimal cache
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy application code
COPY Inference.py .

# Expose application port
EXPOSE 5000

# Use non-root user for security
RUN useradd -m appuser
USER appuser

COPY models ./models/
COPY scalers ./scalers/

RUN ls -l 
# Run application
CMD python Inference.py