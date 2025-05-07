# app/utils/image_utils.py
import numpy as np
from PIL import Image

def preprocess_image(image: Image.Image, target_size=(224, 224)):
    """
    PIL Image → numpy array, 0~1 정규화, 배치 차원 추가
    """
    image = image.resize(target_size)
    arr   = np.array(image) / 255.0
    return np.expand_dims(arr, axis=0)
