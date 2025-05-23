from flask import Blueprint, request, jsonify
import face_recognition
import numpy as np
import base64
import google.generativeai as genai
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

mission_bp = Blueprint("mission", __name__)

@mission_bp.route("/verify-image", methods=["POST"])
def verify():
    try:
        face_file = request.files.get("registered_face")
        mission_file = request.files.get("mission_image")
        place_id = request.form.get("placeId")

        if not face_file or not mission_file or not place_id:
            return jsonify({"result": "fail", "reason": "missing data"})

        # Read mission_image first as it will be used twice
        image_bytes = mission_file.read()
        mission_image = face_recognition.load_image_file(BytesIO(image_bytes))
        face_image = face_recognition.load_image_file(face_file)

        face_encodings = face_recognition.face_encodings(face_image)
        mission_encodings = face_recognition.face_encodings(mission_image)

        if not face_encodings or not mission_encodings:
            return jsonify({
                "result": "fail",
                "reason": "no face detected",
                "face_detected": len(face_encodings) > 0,
                "mission_face_detected": len(mission_encodings) > 0
            })

        distance = np.linalg.norm(face_encodings[0] - mission_encodings[0])
        same_person = distance < 0.4  # threshold

        # Gemini processing
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
        prompt = f"Please determine whether the location '{place_id}' appears in the background of this image. Focus on the background and ignore the person in the foreground."


        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([
            {"text": prompt},
            {
                "inline_data": {
                    "mime_type": "image/png",
                    "data": encoded_image
                }
            }
        ])
        response_text = response.text.strip().lower()
        background_detected = (
            place_id.lower() in response_text or
            "exist" in response_text or
            "present" in response_text
        )

        # Logging
        print("face match distance:", distance)
        print("gemini response:", response_text)

        if same_person and background_detected:
            return jsonify({"result": "success"})
        else:
            return jsonify({
                "result": "fail",
                "reason": "check condition",
                "distance": distance,
                "same_person": same_person,
                "gemini_response": response_text,
                "background_detected": background_detected
            })

    except Exception as e:
        return jsonify({"result": "fail"})
