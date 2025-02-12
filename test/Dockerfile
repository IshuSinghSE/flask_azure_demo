# Use the official Python 3.9-slim image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies for OpenCV
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY app.py .
COPY run.sh .

# Define environment variable
RUN chmod +x ./run.sh

# Expose the port your app runs on
EXPOSE 8000

# Run the application with Gunicorn
CMD ["./run.sh"]
