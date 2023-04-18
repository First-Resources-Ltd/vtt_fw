FROM python:3.10.11-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    git \
    wget \
    nano

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt