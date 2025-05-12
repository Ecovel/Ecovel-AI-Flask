from flask import Blueprint, jsonify, request
from datetime import date
from ..services.quiz_service import get_today_quiz, check_answer

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/today", methods=["GET"])
def get_today():
    quiz = get_today_quiz()
    return jsonify({"question": quiz["question"]})

@quiz_bp.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    user_answer = data.get("user_answer")
    if not user_answer:
        return jsonify({"error": "Missing user_answer"}), 400
    result = check_answer(user_answer)
    return jsonify(result)
