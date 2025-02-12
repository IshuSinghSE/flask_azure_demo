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
        print("Model Input Names:", [input.name for input in model.get_inputs()])
        print("Model Output Names:", [output.name for output in model.get_outputs()])
    except Exception as e:
        print(f"Error loading model: {e}")
        return jsonify({"error": f"Failed to load model: {e}"}), 500

# with app.app_context():


@app.route("/")
def home():
    return jsonify({"message": "Welcome to the YOLOv5 API!", "host": request.host, "url": request.url})

@app.route("/predict", methods=["POST"])
def predict():
    print("💮 Loading ONNX model...")
    load_model()
    """Receive an image from the frontend, run ONNX model, and return detections."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    try:
        # Preprocess the input image as needed by your ONNX model
        input_data = cv2.resize(image_array, (640, 640))  # Resize the image to your model's input size
        input_data = np.transpose(input_data, (2, 0, 1))  # Change data format from HWC to CHW
        input_data = np.expand_dims(input_data, axis=0)  # Add batch dimension
        input_data = input_data.astype(np.float32)  # Convert to float32

        # Normalize the input data (if required by your model)
        input_data /= 255.0

        # Debugging: Print input data shape and type
        print("Input Data Shape:", input_data.shape)
        print("Input Data Type:", input_data.dtype)

        # Run the model
        ort_inputs = {model.get_inputs()[0].name: input_data}
        ort_outs = model.run(None, ort_inputs)

        # Debugging: Print model output
        print("Model Output:", ort_outs)

        # Process the model's output (modify as needed based on your model's output format)
        # Process the model's output
        predictions = {}
        for result in ort_outs[0]:  # Assuming the first output contains detection results
            for detection in result:
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
        print(f"Error processing prediction: {e}")  # Debugging: Print error
        return jsonify({"error": str(e)}), 500

    return jsonify({"predictions": predictions})

if __name__ == "__main__":
    # Remove the app.run() call to use Gunicorn instead
    pass
