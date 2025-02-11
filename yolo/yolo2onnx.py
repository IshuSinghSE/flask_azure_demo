from ultralytics import YOLO

# Load your YOLOv11 model
model = YOLO("best.pt")
model.eval()  # Set the model to evaluation mode

# Export the model to ONNX
model.export(format="onnx", imgsz=(640, 640))  # Adjust the image size if needed
print("Model has been converted to ONNX")
