# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY src/requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY src/ /app/src/
COPY data/ /data/

# Copy the SQL schema file
COPY people_places.sql /docker-entrypoint-initdb.d/

# Command to run the Python script
CMD ["python", "src/main.py"]
