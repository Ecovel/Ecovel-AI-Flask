# app/routes/profile.py

from flask import Blueprint, request, Response
import os, io, json
from PIL import Image
from ..services.face_service import load_face_model, predict_face
from ..utils.image_utils import preprocess_image

profile_bp = Blueprint("profile", __name__)
model = load_face_model("model/model.h5")


@profile_bp.route("/profile-image", methods=["POST"])
def upload_profile_image():
    user_id = request.form.get("userId")
    file    = request.files.get("file")

    # 실패: userId 없거나 파일 없음 혹은 AI 판별 실패
    if not user_id or not file:
        payload = {
            "httpStatus": "OK",
            "success": False,
            "result": None,
            "error": "사용자를 찾을 수 없습니다."
        }
        return Response(
            json.dumps(payload, ensure_ascii=False),
            status=200,
            content_type="application/json; charset=utf-8"
        )

    # AI 얼굴 판별
    img = Image.open(io.BytesIO(file.read())).convert("RGB")
    arr = preprocess_image(img)
    class_id, confidence = predict_face(model, arr)
    if class_id != 0 or confidence < 0.5:
        payload = {
            "httpStatus": "OK",
            "success": False,
            "result": None,
            "error": "사용자를 찾을 수 없습니다."
        }
        return Response(
            json.dumps(payload, ensure_ascii=False),
            status=200,
            content_type="application/json; charset=utf-8"
        )

    # 성공
    save_dir = os.path.join("uploads", "faces", user_id)
    os.makedirs(save_dir, exist_ok=True)
    img.save(os.path.join(save_dir, "face.jpg"))

    payload = {
        "httpStatus": "OK",
        "success": True,
        "result": f"http://34.64.210.130:5000/uploads/faces/{user_id}/face.jpg", 
        "error": None
    }
    return Response(
        json.dumps(payload, ensure_ascii=False),
        status=200,
        content_type="application/json; charset=utf-8"
    )


@profile_bp.route("/profile-image", methods=["GET"])
def get_profile_image():
    user_id = request.args.get("userId")
    img_path = os.path.join("uploads", "faces", user_id or "", "face.jpg")

    # 실패: userId 없거나 파일이 없으면
    if not user_id or not os.path.exists(img_path):
        payload = {
            "httpStatus": "OK",
            "success": False,
            "result": None,
            "error": "등록된 얼굴 이미지가 없습니다."
        }
        return Response(
            json.dumps(payload, ensure_ascii=False),
            status=200,
            content_type="application/json; charset=utf-8"
        )

    # 성공
    payload = {
        "httpStatus": "OK",
        "success": True,
        "result": f"http://34.64.210.130:5000/uploads/faces/{user_id}/face.jpg",
        "error": None
    }
    return Response(
        json.dumps(payload, ensure_ascii=False),
        status=200,
        content_type="application/json; charset=utf-8"
    )
