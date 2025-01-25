# Use an official Python runtime as a parent image
FROM python:3.9-slim

FROM python:3.9 AS builder

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY Inference.py .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV PATH=/root/.local/bin:$PATH

# Run the application
CMD python Inference.py