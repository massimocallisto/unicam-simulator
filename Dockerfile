# Use Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9093 KAFKA_TOPIC=sample_data

# Set the default entry point
CMD ["python", "-u", "app.py"]
