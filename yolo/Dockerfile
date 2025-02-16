# Use the official Python 3.12-slim image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt flask_yolo.py ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app

# Expose the port your app runs on
EXPOSE 5000

# Run the application with Gunicorn
ENTRYPOINT ["gunicorn", "--workers=3", "--bind=0.0.0.0:5000", "flask_yolo:app"]
