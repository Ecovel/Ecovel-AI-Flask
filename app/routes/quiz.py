from flask import Blueprint, jsonify, request, session
from datetime import datetime
from ..services.quiz_service import generate_quiz

quiz_bp = Blueprint("quiz", __name__)

# 오늘의 퀴즈 제공 (하루에 하나 유지)
@quiz_bp.route("/today", methods=["GET"])
def get_today_quiz():
    today = str(datetime.today().date())

    if session.get("quiz_date") == today:
        quiz = session["quiz"]
    else:
        quiz = generate_quiz()
        session["quiz"] = quiz
        session["quiz_date"] = today
        session["answered"] = False

    # ✅ 정답/해설은 제외하고 question만 반환
    return jsonify({
        "question": quiz["question"]
    })

# 퀴즈 정답 제출
@quiz_bp.route("/submit", methods=["POST"])
def submit_answer():
    if session.get("answered"):
        return jsonify({"message": "Already answered today"}), 400

    data = request.get_json()
    user_answer = data.get("user_answer")
    correct_answer = session.get("quiz", {}).get("answer")

    if not correct_answer:
        return jsonify({"message": "No quiz found"}), 400

    session["answered"] = True
    return jsonify({
        "correct": user_answer == correct_answer,
        "explanation": session["quiz"]["explanation"]
    })

# 오늘 응시 여부 확인
@quiz_bp.route("/answered", methods=["GET"])
def check_answered():
    return jsonify({"answered": session.get("answered", False)})
