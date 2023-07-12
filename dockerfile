FROM python:3.10.12-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    git \
    wget \
    nano

# Set working directory
WORKDIR /app

# Create log directory
RUN mkdir -p /var/log/gunicorn

# Copy source code
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# handle error log gunicorn
RUN touch /var/log/gunicorn/error.log && \
    chmod 777 /var/log/gunicorn/error.log

# Create model Directory in home
RUN mkdir -p /home/data

# Download File (config, tokenizer, vocabulary, model)
RUN wget -P /home/data https://huggingface.co/guillaumekln/faster-whisper-small/resolve/main/config.json
RUN wget -P /home/data https://huggingface.co/guillaumekln/faster-whisper-small/resolve/main/tokenizer.json
RUN wget -P /home/data https://huggingface.co/guillaumekln/faster-whisper-small/resolve/main/vocabulary.txt
RUN wget -P /home/data https://huggingface.co/guillaumekln/faster-whisper-small/resolve/main/model.bin