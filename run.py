from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider

from app.routes.profile import profile_bp
from app.routes.mission import mission_bp

# 커스텀 JSON Provider 설정 (한글 깨짐 방지 + 키 순서 유지)
class CustomJSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        kwargs.setdefault("ensure_ascii", False)
        kwargs.setdefault("sort_keys", False)
        return super().dumps(obj, **kwargs)

def create_app():
    app = Flask(__name__)
    app.json = CustomJSONProvider(app)
    app.config["JSON_SORT_KEYS"] = False

    CORS(app)

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

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=False)
