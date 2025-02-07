from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import numpy as np
import cv2
import io
import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import tempfile

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.getenv("ORIGINS")}})  # Allow requests from specified origins

# Get Azure Blob Storage connection string from environment variable
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")
blob_name = os.getenv("AZURE_BLOB_MODEL_PATH")  # Path to your model within the container

model = None

def load_model():
    global model
    try:
        temp_model_path = None
        if os.getenv("ENVIRONMENT") == "production":
            print(f"Connecting to Azure Blob Storage with connection string: {connect_str}")
            container_client = blob_service_client.get_container_client(container_name)
            print(f"Checking for container: {container_name}")
            if not container_client.exists():
                raise Exception(f"Container '{container_name}' does not exist.")
            
            blob_client = container_client.get_blob_client(blob_name)
            print(f"Checking for blob: {blob_name}")
            if not blob_client.exists():
                raise Exception(f"Blob '{blob_name}' does not exist in container '{container_name}'.")
            
            model_data = blob_client.download_blob().readall()
            print(f"Successfully downloaded model data from blob: {blob_name}")
            
            # Save model data to a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_model_file:
                temp_model_file.write(model_data)
                temp_model_path = temp_model_file.name
        else:
            print(f"Loading YOLO model from local file: {blob_name}")
            temp_model_path = 'best.pt'
        model = YOLO(temp_model_path)  # Load YOLO model from the temporary file
        
        print("YOLO model loaded successfully from Azure Blob Storage.")
    except Exception as e:
        print(f"Error loading model from Azure Blob Storage: {e}")
        print(f"Container Name: {container_name}") 
        print(f"Blob Name: {blob_name}")
        return jsonify({"error": f"Failed to load model: {e}"}), 500


with app.app_context():
    # def before_first_request():
    print("💮 Loading YOLO model...")
    load_model()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the YOLOv5 API!", "host": request.host, "url": request.url})

@app.route("/predict", methods=["POST"])
def predict():
    """Receive an image from the frontend, run YOLO model, and return detections."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    # Read image file as a byte stream and convert to numpy array using OpenCV
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    try:
        results = model.predict(image_array)
        predictions = {}

        # Process detections
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0].item())  # Class ID
                label = model.names[class_id]  # Class name
                confidence = round(box.conf[0].item(), 2)  # Confidence score
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates

                prediction = {
                    "bbox": [x1, y1, x2, y2],
                    "class_id": class_id,
                    "confidence": confidence
                }
                # Ensure the label name doesn't contain spaces and is lowercase e.g. "root_piece"
                label = label.replace(" ", "_").lower()
                if label not in predictions: 
                    predictions[label] = []
                predictions[label].append(prediction)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"prediction": predictions})

if __name__ == "__main__":
    if os.getenv("ENVIRONMENT") == "production":
        # Use Gunicorn to run the app in production
        from gunicorn.app.wsgiapp import run
        run()
    else:
        # Use Flask's built-in server for local development
        app.run(debug=True, host='0.0.0.0', port=5000)