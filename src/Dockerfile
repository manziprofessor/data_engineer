# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the source code into the container at /app
COPY . .

# Install Dockerize
RUN apt-get update && apt-get install -y wget
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz
RUN tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz

# Use Dockerize to wait for PostgreSQL to be ready
CMD ["dockerize", "-wait", "tcp://db:5432", "-timeout", "60s", "python", "main.py"]
