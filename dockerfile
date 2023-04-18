FROM python:3.10.11-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    git \
    wget \
    nano

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

RUN touch /var/log/gunicorn/error.log
RUN chmod 666 /var/log/gunicorn/error.log

RUN touch /var/log/gunicorn/access.log
RUN chmod 666 /var/log/gunicorn/access.log


CMD ["gunicorn", "gunicorn.conf.py"]