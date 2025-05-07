from flask import Flask, jsonify
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider
from app.routes.profile import profile_bp
from app.routes.mission import mission_bp  


class CustomJSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        # 한글 깨짐 방지, 키 순서 고정
        kwargs.setdefault("ensure_ascii", False)
        kwargs.setdefault("sort_keys", False)
        return super().dumps(obj, **kwargs)


def create_app():
    app = Flask(__name__)
    # 커스텀 JSON Provider 등록
    app.json = CustomJSONProvider(app)
    app.config["JSON_SORT_KEYS"] = False

    CORS(app)

    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({
            "status":  "OK",
            "message": "Ecovel AI-ML API is running"
        }), 200

    # ─── 프로필 블루프린트 등록 (/users/profile-image) ───
    app.register_blueprint(profile_bp, url_prefix="/users")

    # ─── 미션 블루프린트 ───
    app.register_blueprint(mission_bp, url_prefix="/ai")

    print("등록된 라우터 목록 : ")
    print(app.url_map)
    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=False)
