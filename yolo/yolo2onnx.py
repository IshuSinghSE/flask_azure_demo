import torch
from ultralytics.nn.tasks import SegmentationModel

# Allowlist the SegmentationModel class
torch.serialization.add_safe_globals([SegmentationModel])

# Load the checkpoint
checkpoint = torch.load('best.pt', map_location=torch.device('cpu'))

# Extract the model state dictionary
if 'model' in checkpoint and checkpoint['model'] is not None:
    state_dict = checkpoint['model'].state_dict()
else:
    raise ValueError("The checkpoint does not contain a valid model state dictionary")

# Create an instance of SegmentationModel with default parameters or specify necessary parameters
model = SegmentationModel()  # Adjust parameters as needed
model.load_state_dict(state_dict)
model.eval()  # Set the model to evaluation mode

# Create a dummy input tensor
dummy_input = torch.randn(1, 3, 640, 640)  # Adjust the shape according to your model's input

# Export the model to ONNX
torch.onnx.export(model,  # model being run
                  dummy_input,  # model input (or a tuple for multiple inputs)
                  "best.onnx",  # where to save the model
                  export_params=True,  # store the trained parameter weights inside the model file
                  opset_version=10,  # the ONNX version to export the model to
                  do_constant_folding=True,  # whether to execute constant folding for optimization
                  input_names=['input'],  # the model's input names
                  output_names=['output'])  # the model's output names

print("Model has been converted to ONNX")
