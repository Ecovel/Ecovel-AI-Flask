import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D as OriginalDepthwiseConv2D

# Define custom DepthwiseConv2D (to prevent errors when loading the model)
class CustomDepthwiseConv2D(OriginalDepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        if "groups" in kwargs:
            kwargs.pop("groups")
        super().__init__(*args, **kwargs)

# Load face recognition model
def load_face_model(path: str):
    return load_model(path, custom_objects={"DepthwiseConv2D": CustomDepthwiseConv2D})

# Perform face prediction
def predict_face(model, image_array):
    preds = model.predict(image_array)
    class_id = int(preds.argmax())
    confidence = float(preds.max())
    return class_id, confidence
