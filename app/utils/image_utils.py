import numpy as np
from PIL import Image

def preprocess_image(image: Image.Image, target_size=(224, 224)):
 
    image = image.resize(target_size)
    arr   = np.array(image) / 255.0
    return np.expand_dims(arr, axis=0)
