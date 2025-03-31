# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies for MariaDB client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Update pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables with default values
ENV DB_USERNAME=root
ENV DB_PASSWORD=
ENV DB_HOST=localhost
ENV DB_PORT=3306
ENV DB_NAME=user_management

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]