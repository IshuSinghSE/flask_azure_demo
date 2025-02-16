from ultralytics import YOLO

# Load your YOLOv11 model
model = YOLO("best.pt")
model.eval()  # Set the model to evaluation mode

# Export the model to ONNX
model.dynamo_export = False  # Disable Dynamic ONNX Export
model.export(format="onnx", imgsz=(640, 640), opset=11, simplify=True)  # Adjust the image size if needed
print("Model has been converted to ONNX")
