from flask import Blueprint, jsonify, request
from datetime import date
from ..services.quiz_service import get_today_quiz

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/today", methods=["GET"])
def get_today():
    quiz = get_today_quiz()
    return jsonify(quiz)


