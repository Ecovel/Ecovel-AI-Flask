from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider

from app.routes.profile import profile_bp
from app.routes.mission import mission_bp
from app.routes.quiz import quiz_bp

# Gemini 인증 관련 import 추가
from google.auth import load_credentials_from_file
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 커스텀 JSON Provider 설정 (한글 깨짐 방지 + 키 순서 유지)
class CustomJSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        kwargs.setdefault("ensure_ascii", False)
        kwargs.setdefault("sort_keys", False)
        return super().dumps(obj, **kwargs)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    app.json = CustomJSONProvider(app)
    app.config["JSON_SORT_KEYS"] = False
    
    CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "https://ecovel-seven.vercel.app"
        ]
    }
})


    # ✅ Gemini 인증 안전하게 분기 처리
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    api_key = os.getenv("GEMINI_API_KEY")

    if cred_path and os.path.exists(cred_path) and not api_key:
        # 서비스 계정만 있는 경우에만 credentials 사용
        creds, _ = load_credentials_from_file(
            cred_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        genai.configure(credentials=creds)
    elif api_key:
        # API 키가 있으면 그걸 우선 사용
        genai.configure(api_key=api_key)
    else:
        raise ValueError("❌ Gemini 인증 정보가 없습니다! .env에 API 키나 서비스 계정 경로를 넣어주세요.")


    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "OK",
            "message": "Ecovel-AI-ML API is running"
        }), 200
    
    # 이미지 정적 서빙 라우터 추가 
    @app.route("/uploads/faces/<user_id>/<filename>")
    def serve_uploaded_image(user_id, filename):
        return send_from_directory(f"uploads/faces/{user_id}", filename)
    
    # 프로필 블루프린트 등록 (/users/profile-image)
    app.register_blueprint(profile_bp, url_prefix="/users")

    # 미션 블루프린트 등록 (/ai/...)
    app.register_blueprint(mission_bp, url_prefix="/ai")

    app.register_blueprint(quiz_bp, url_prefix="/quiz")

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=False)
