# app/services/face_service.py

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D as OriginalDepthwiseConv2D

# 커스텀 DepthwiseConv2D 정의 (모델 로딩 시 오류 방지용)
class CustomDepthwiseConv2D(OriginalDepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        if "groups" in kwargs:
            kwargs.pop("groups")
        super().__init__(*args, **kwargs)

# 얼굴 인식 모델 로드
def load_face_model(path: str):
    return load_model(path, custom_objects={"DepthwiseConv2D": CustomDepthwiseConv2D})

# 얼굴 예측 수행
def predict_face(model, image_array):
    preds = model.predict(image_array)
    class_id = int(preds.argmax())
    confidence = float(preds.max())
    return class_id, confidence
