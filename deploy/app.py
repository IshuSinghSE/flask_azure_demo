from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import numpy as np
import cv2
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = None

def load_model():
    global model
    try:
        logger.info("Loading YOLO model from local file: 'best.pt'")
        model = YOLO('best.pt')  # Load YOLO model from the local file
        logger.info("YOLO model loaded successfully from local file.")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return jsonify({"error": f"Failed to load model: {e}"}), 500

with app.app_context():
    logger.info("💮 Loading YOLO model...")
    load_model()

@app.route("/")
def home():
    logger.info("🌸 Welcome to the YOLOv5 API!")
    return jsonify({"message": "Welcome to the YOLOv5 API!", "host": request.host, "url": request.url})

@app.route("/predict", methods=["POST"])
def predict():
    """Receive an image from the frontend, run YOLO model, and return detections."""
    if "file" not in request.files:
        logger.warning("No file uploaded")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    try:
        logger.info("Predicting results...")
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
        logger.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

    logger.info(f"Predictions: {predictions}")
    return jsonify({"prediction": predictions})

if __name__ == "__main__":
    app.run()
