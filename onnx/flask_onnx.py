from flask import Flask, request, jsonify
from flask_cors import CORS
import onnxruntime as ort
import numpy as np
import cv2

# Initialize Flask app
app = Flask(__name__)
CORS(app)

model = None

def load_model():
    global model
    try:
        print(f"Loading ONNX model from local file: 'best.onnx'")
        model = ort.InferenceSession("best.onnx")  # Load ONNX model from the local file
        print("ONNX model loaded successfully from local file.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return jsonify({"error": f"Failed to load model: {e}"}), 500

with app.app_context():
    print("💮 Loading ONNX model...")
    load_model()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the YOLOv5 API!", "host": request.host, "url": request.url})

@app.route("/predict", methods=["POST"])
def predict():
    """Receive an image from the frontend, run ONNX model, and return detections."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    try:
        input_data = np.expand_dims(image_array, axis=0).astype(np.float32)  # Modify according to your model's input shape
        results = model.run(None, {"input": input_data})  # Modify according to your model's input name
        predictions = {}

        # Process detections (example)
        for detection in results[0]:  # Modify according to your model's output format
            class_id = int(detection[1])
            confidence = round(float(detection[2]), 2)
            x1, y1, x2, y2 = map(int, detection[3:7])

            prediction = {
                "bbox": [x1, y1, x2, y2],
                "class_id": class_id,
                "confidence": confidence
            }
            label = f"class_{class_id}".replace(" ", "_").lower()  # Modify according to your model's class labels
            if label not in predictions:
                predictions[label] = []
            predictions[label].append(prediction)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"prediction": predictions})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
