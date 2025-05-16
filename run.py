from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider

from app.routes.profile import profile_bp
from app.routes.mission import mission_bp
from app.routes.quiz import quiz_bp

# Added import for Gemini authentication
from google.auth import load_credentials_from_file
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Custom JSON Provider (to prevent Korean character corruption + preserve key order)
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

    # Secure branching logic for Gemini authentication
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    api_key = os.getenv("GEMINI_API_KEY")

    if cred_path and os.path.exists(cred_path) and not api_key:
        # Use credentials only when a service account is available
        creds, _ = load_credentials_from_file(
            cred_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        genai.configure(credentials=creds)
    elif api_key:
        # If API key is available, use it with priority
        genai.configure(api_key=api_key)
    else:
        raise ValueError("No Gemini credentials found! Please set an API key or service account path in .env.")

    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "OK",
            "message": "Ecovel-AI-ML API is running"
        }), 200
    
    # Add static image serving route
    @app.route("/uploads/faces/<user_id>/<filename>")
    def serve_uploaded_image(user_id, filename):
        return send_from_directory(f"uploads/faces/{user_id}", filename)
    
    # Register profile blueprint (/users/profile-image)
    app.register_blueprint(profile_bp, url_prefix="/users")

    # Register mission blueprint (/ai/...)
    app.register_blueprint(mission_bp, url_prefix="/ai")

    # Register quiz blueprint (/quiz)
    app.register_blueprint(quiz_bp, url_prefix="/quiz")

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=False)
