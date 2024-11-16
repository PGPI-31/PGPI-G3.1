# Use the official Python image with Python 3.12
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory to the root of the project
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
       postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install gunicorn


# Install Python dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (everything in the root directory)
COPY . /usr/src/app/

# Expose port 8000
EXPOSE 8000

# Copy the entrypoint script from the docker folder to the container's app directory
COPY docker-entrypoint.sh /usr/src/app/

# Set permissions to make the script executable
RUN chmod +x /usr/src/app/docker-entrypoint.sh

# Use the script as the entrypoint
ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]


