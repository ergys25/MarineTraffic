# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and main.py
COPY requirements.txt .
COPY main.py .

# Install Firefox, geckodriver, and required Python packages
RUN apt-get update && \
    apt-get install -y firefox-esr wget && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz && \
    tar -xvzf geckodriver* && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver-v0.34.0-linux64.tar.gz && \
    pip install -r requirements.txt

# Set environment variables for Firefox
ENV DISPLAY=:99

# Run the script
CMD ["python", "main.py"]
